import streamlit as st
import requests
import subprocess

# URL do servidor API
API_URL = "http://localhost:5000/data"
GENERATE_DATA_SCRIPT = "server.js"  # Caminho para o script Node.js

# Função para chamar o script Node.js
def run_node_script(script_path):
    try:
        subprocess.run(['node', script_path], check=True)
        st.success("Dados atualizados com sucesso!")
    except subprocess.CalledProcessError as e:
        st.error(f"Erro ao executar o script: {e}")

# Função para obter dados da API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Erro ao buscar dados da API")
        return {}

# Função para exibir os dados
def display_data(data):
    if not data:
        st.write("Nenhum dado para exibir.")
        return

    st.title("Dados da API")

    # Exibindo a estrutura geral dos dados
    st.write("Estrutura dos dados:")
    st.json(data)

    # Aqui você pode mapear os dados conforme necessário
    for item in data:
        st.write(f"Serial: {item['serial']}")
        st.write(f"Name: {item['name']}")
        st.write(f"Location: {item['location']}")
        st.write(f"SubLocation: {item['subLocation']}")
        st.write("---")

# Interface do Streamlit
def main():
    st.header("Aplicação Streamlit para Gerenciar e Exibir Dados")

    # Botão para atualizar dados
    if st.button('Atualizar Dados'):
        run_node_script(GENERATE_DATA_SCRIPT)
        st.experimental_rerun()  # Atualiza a interface após execução

    # Obter dados da API
    data = fetch_data()

    # Exibir os dados
    display_data(data)

if __name__ == "__main__":
    main()
