# app.py
import os
from dotenv import load_dotenv
import streamlit as st
import glob
import pandas as pd
from google import genai
from dotenv import load_dotenv

# ==============================
# CARREGAR VARIÁVEIS DO .ENV
# ==============================
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("❌ API Key não encontrada. Verifique seu arquivo .env")

# ==============================
# CONFIGURAÇÃO INICIAL
# ==============================
st.set_page_config(page_title="Motofrete BH", layout="wide")
st.title("🏍️ Estacionamento Motofrete - Belo Horizonte")
st.write("Digite sua rua e número para encontrar o estacionamento mais próximo e receber dicas da IA.")

# ==============================
# CONFIGURAR GOOGLE GENAI
# ==============================
client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

# ==============================
# CARREGAR DADOS
# ==============================
@st.cache_data
def carregar_dados():
    arquivos = glob.glob("data/*.csv")
    lista = []
    for arquivo in arquivos:
        df = pd.read_csv(arquivo, sep=";", encoding="utf-8", low_memory=False)
        lista.append(df)
    dados = pd.concat(lista, ignore_index=True)
    dados["LOGRADOURO"] = dados["LOGRADOURO"].astype(str)
    dados["REFERENCIA_LOGRADOURO"] = dados["REFERENCIA_LOGRADOURO"].astype(str)
    if "NUMERO_LOGRADOURO" not in dados.columns:
        dados["NUMERO_LOGRADOURO"] = None
    return dados

dados = carregar_dados()

# ==============================
# AUTOCOMPLETE DE RUAS
# ==============================
ruas = sorted(dados["LOGRADOURO"].dropna().unique())
rua_usuario = st.selectbox("📍 Onde você está? (Digite a rua)", ruas)
numero_usuario = st.text_input("🏠 Número (opcional)")
buscar_btn = st.button("🔍 Buscar estacionamento mais próximo")

# ==============================
# FUNÇÃO DE ANÁLISE COM IA
# ==============================
def analisar_com_ia(df_resultado, endereco):
    if df_resultado.empty:
        return "Não encontrei estacionamentos próximos para analisar."
    
    contexto = df_resultado.head(5).to_string()
    prompt = f"""
Você é um assistente urbano especializado em motofrete em Belo Horizonte.

O usuário está em: {endereco}

Estacionamentos próximos encontrados:
{contexto}

Forneça:
- O melhor local para estacionar
- Horário de funcionamento
- Dicas rápidas para o motofretista
- Rota recomendada (Google Maps)
- Caso haja mais opções, liste resumidamente
"""
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar análise de IA: {e}"

# ==============================
# PROCESSAR BUSCA
# ==============================
if buscar_btn and rua_usuario.strip() != "":
    resultado = dados[dados["LOGRADOURO"].str.contains(rua_usuario, case=False, na=False)].copy()

    if resultado.empty:
        st.warning(f"❌ Nenhum estacionamento encontrado para '{rua_usuario}'")
    else:
        # Se o usuário forneceu número, calcular proximidade
        if numero_usuario.strip() != "":
            try:
                numero_usuario_int = int(numero_usuario)
                # Converter coluna para número inteiro quando possível
                resultado["NUMERO_INT"] = pd.to_numeric(resultado["NUMERO_LOGRADOURO"], errors="coerce")
                # Calcular diferença absoluta
                resultado["DISTANCIA_NUMERO"] = resultado["NUMERO_INT"].apply(
                    lambda x: abs(x - numero_usuario_int) if pd.notna(x) else float('inf')
                )
                # Ordenar pelo número mais próximo
                resultado = resultado.sort_values("DISTANCIA_NUMERO")
            except ValueError:
                st.warning("Número informado inválido. Buscando somente por rua.")

        # Pegar o mais próximo
        estacionamento_proximo = resultado.iloc[0]

        st.success(f"✅ Estacionamento mais próximo encontrado: {estacionamento_proximo['LOGRADOURO']}")
        st.markdown("### 📍 Detalhes do Estacionamento")
        st.write(f"**Rua:** {estacionamento_proximo['LOGRADOURO']}")
        st.write(f"**Referência:** {estacionamento_proximo['REFERENCIA_LOGRADOURO']}")
        st.write(f"**Vagas físicas:** {estacionamento_proximo.get('NUMERO_VAGAS_FISICAS', 'N/A')}")
        st.write(f"**Dias:** {estacionamento_proximo.get('DIA_REGRA_OPERACAO', 'N/A')}")
        st.write(f"**Horário:** {estacionamento_proximo.get('PERIODO_VALIDO_REGRA_OPERACAO', 'N/A')}")

        endereco_maps = f"{estacionamento_proximo['LOGRADOURO']} Belo Horizonte MG"
        maps_url = f"https://www.google.com/maps/dir/?api=1&destination={endereco_maps.replace(' ', '+')}"
        st.markdown(f"[🗺️ Ver rota no Google Maps]({maps_url})", unsafe_allow_html=True)

        # ==============================
        # CHAMAR IA
        # ==============================
        st.divider()
        st.subheader("🤖 Análise Inteligente da IA")
        endereco_usuario = f"{rua_usuario} {numero_usuario}".strip()
        resposta_ia = analisar_com_ia(resultado, endereco_usuario)
        st.write(resposta_ia)