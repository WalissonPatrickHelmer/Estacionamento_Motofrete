import streamlit as st
import glob
import pandas as pd

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Motofrete BH", layout="wide")

st.title("🏍️ Estacionamento Motofrete - Belo Horizonte")
st.write("Digite ou selecione a rua para encontrar estacionamento motofrete.")

# ==============================
# CARREGAR DADOS
# ==============================
@st.cache_data
def carregar_dados():

    arquivos = glob.glob("data/*.csv")

    lista = []
    for arquivo in arquivos:
        df = pd.read_csv(
            arquivo,
            sep=";",
            encoding="utf-8",
            low_memory=False
        )
        lista.append(df)

    dados = pd.concat(lista, ignore_index=True)

    dados["LOGRADOURO"] = dados["LOGRADOURO"].astype(str)
    dados["REFERENCIA_LOGRADOURO"] = dados["REFERENCIA_LOGRADOURO"].astype(str)

    return dados


dados = carregar_dados()

# ==============================
# LISTA DE RUAS (AUTOCOMPLETE)
# ==============================
ruas = sorted(dados["LOGRADOURO"].dropna().unique())

st.subheader("📍 Onde você está?")

rua_escolhida = st.selectbox(
    "Comece digitando o nome da rua:",
    ruas
)

# ==============================
# BUSCA
# ==============================
if rua_escolhida:

    resultado = dados[dados["LOGRADOURO"] == rua_escolhida]

    if not resultado.empty:

        local_proximo = resultado.iloc[0]

        st.success("✅ Estacionamento encontrado")

        st.markdown("### 📍 Local recomendado")

        st.write(f"**Rua:** {local_proximo['LOGRADOURO']}")
        st.write(f"**Referência:** {local_proximo['REFERENCIA_LOGRADOURO']}")
        st.write(f"**Vagas físicas:** {local_proximo['NUMERO_VAGAS_FISICAS']}")
        st.write(f"**Dias:** {local_proximo['DIA_REGRA_OPERACAO']}")
        st.write(f"**Horário:** {local_proximo['PERIODO_VALIDO_REGRA_OPERACAO']}")

        # GOOGLE MAPS
        endereco = f"{local_proximo['LOGRADOURO']}, Belo Horizonte MG"
        maps_url = f"https://www.google.com/maps/search/?api=1&query={endereco.replace(' ', '+')}"

        st.link_button(
            "🗺️ Ir até o estacionamento (Google Maps)",
            maps_url
        )