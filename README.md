Perfeito! Aqui está um README.md completo para o seu projeto de estacionamento motofrete, já formatado para GitHub:

# 🏍️ Estacionamento Motofrete - Belo Horizonte

Este projeto é um **app web interativo** criado com **Streamlit**, que permite aos motofretistas de Belo Horizonte localizar o **estacionamento mais próximo** com base na rua e número informado. Além disso, o app fornece uma **análise detalhada da IA do Google Gemini** com dicas sobre o local, horários, vagas e rota recomendada.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Streamlit** – interface web interativa
- **Pandas** – manipulação de dados
- **Google Generative AI (gemini-2.5-flash)** – análise inteligente
- **python-dotenv** – carregar variáveis de ambiente
- **.streamlit/secrets.toml** – para proteger a API key

---

## ⚡ Funcionalidades

1. Autocomplete de ruas baseado nos dados CSV.
2. Busca por número opcional para encontrar o estacionamento mais próximo.
3. Visualização detalhada do estacionamento:
   - Rua e referência
   - Vagas físicas
   - Dias e horários de funcionamento
4. Link direto para **rota no Google Maps**.
5. Análise detalhada da IA com dicas rápidas para motofretistas.

---

## 📂 Estrutura do Projeto


estacionamento_motofrete/
│
├─ app.py # Arquivo principal do Streamlit
├─ requirements.txt # Dependências do projeto
├─ data/ # CSVs com os dados de estacionamentos
├─ .streamlit/
│ └─ secrets.toml # API key protegida (NÃO enviar para o GitHub)
├─ .gitignore # Arquivos/pastas ignoradas pelo Git
└─ README.md # Este arquivo


---

## 🔑 Proteção da API Key

Para proteger sua chave de API do Google Gemini, o projeto utiliza:

- `.streamlit/secrets.toml`  
  ```toml
  GOOGLE_API_KEY = "SUA_CHAVE_AQUI"
Adicione .streamlit/secrets.toml no .gitignore para não enviar para o GitHub.
Alternativamente, você pode usar .env com python-dotenv para ambientes locais.
🚀 Como Rodar Localmente
Clone o repositório:
git clone https://github.com/seu-usuario/estacionamento_motofrete.git
cd estacionamento_motofrete
Instale as dependências:
pip install -r requirements.txt
Crie o arquivo .streamlit/secrets.toml com sua chave de API:
GOOGLE_API_KEY = "SUA_CHAVE_AQUI"
Execute o app:
streamlit run app.py
Abra o navegador no link mostrado pelo Streamlit.
⚠️ Observações
Certifique-se de não vazar sua API key no GitHub.
O limite de requisições gratuitas da API Gemini é restrito. Confira a documentação de quotas
.
📝 Licença

Este projeto é open source e pode ser usado e modificado livremente.