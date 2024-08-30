import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import plotly.express as px
from groq import Groq

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do cliente Groq
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Função para gerar insights e gráficos com Groq
def generate_insights_and_graphs(dataframe):
    # Ajustar o prompt para indicar que a planilha já foi carregada
    prompt = (
        "Você recebeu uma planilha com os seguintes dados: {data_description}. "
        "A análise deve ser feita com base nesses dados já carregados. "
        "Crie um resumo detalhado dos dados e sugira gráficos apropriados para visualizar as informações. "
        "Inclua tendências, outliers e estatísticas resumidas."
    ).format(data_description=", ".join(dataframe.columns))

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    insights = response.choices[0].message.content
    return insights

# Título do aplicativo
st.title("Análise Dinâmica de Desempenho de Atendentes com Groq")

# Upload da planilha
uploaded_file = st.file_uploader("Escolha o arquivo para análise", type=["xlsx", "xls", "csv"])

if uploaded_file:
    # Determinar o tipo de arquivo e carregar os dados
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file, engine='openpyxl')  # Especificar engine para .xlsx
    elif uploaded_file.name.endswith(".xls"):
        df = pd.read_excel(uploaded_file, engine='xlrd')  # Especificar engine para .xls
    else:
        st.error("Formato de arquivo não suportado.")
        df = None

    if df is not None:
        # Gerar insights e gráficos usando a API da Groq
        insights = generate_insights_and_graphs(df)
        
        # Exibir insights
        st.subheader("Insights Gerados pela Groq")
        st.write(insights)

        # Adicionar uma opção para o usuário escolher como visualizar os dados
        st.write("Escolha como visualizar os dados:")
        grafico_selecionado = st.selectbox("Escolha o gráfico", ["Nenhum", "Gráfico Sugerido 1", "Gráfico Sugerido 2"])

        # Exibir o gráfico sugerido com base na análise da Groq (exemplo)
        if grafico_selecionado == "Gráfico Sugerido 1":
            fig = px.bar(df, x=df.columns[0], y=df.columns[1])  # Exemplo de gráfico sugerido
            st.plotly_chart(fig)
        elif grafico_selecionado == "Gráfico Sugerido 2":
            fig = px.line(df, x=df.columns[0], y=df.columns[1])  # Exemplo de gráfico sugerido
            st.plotly_chart(fig)

else:
    st.write("Por favor, envie um arquivo para continuar.")
