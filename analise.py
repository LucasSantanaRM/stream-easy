import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Título do aplicativo
st.title("Análise Dinâmica de Desempenho de Atendentes")

# Upload da planilha
uploaded_file = st.file_uploader("Escolha a planilha do Excel para análise", type=["xlsx"])

def process_data(file):
    df = pd.read_excel(file)
    df['Data da abertura'] = pd.to_datetime(df['Data da abertura'])
    df['Início do atendimento'] = pd.to_datetime(df['Início do atendimento'])
    df['Fim do atendimento'] = pd.to_datetime(df['Fim do atendimento'])
    
    for col in ['Tempo total em atendimento', 'Tempo total em fila', 'Tempo na última fila']:
        df[col] = pd.to_timedelta(df[col].str.replace(' min.', ' minutes'))
        df[f'{col}_minutos'] = df[col].dt.total_seconds() / 60
    
    return df

if uploaded_file:
    df = process_data(uploaded_file)

    # Sidebar para seleção de visualizações
    st.sidebar.header("Configurações de Visualização")
    
    # Seleção de métricas
    metricas = st.sidebar.multiselect(
        "Escolha as métricas para visualizar",
        ["Quantidade de Atendimentos", "Tempo total em atendimento", "Tempo total em fila", "Tempo na última fila"],
        default=["Quantidade de Atendimentos"]
    )

    # Seleção de tipo de gráfico
    tipo_grafico = st.sidebar.selectbox(
        "Escolha o tipo de gráfico",
        ["Barras", "Linha", "Dispersão", "Boxplot", "Rosca"]
    )

    # Seleção de atendentes (opcional)
    atendentes = st.sidebar.multiselect(
        "Filtrar por atendentes (opcional)",
        options=df['Atendente'].unique(),
        default=df['Atendente'].unique()
    )

    # Filtrar DataFrame
    df_filtrado = df[df['Atendente'].isin(atendentes)]

    # Função para criar gráficos
    def criar_grafico(dados, x, y, tipo):
        if tipo == "Barras":
            fig = px.bar(dados, x=x, y=y, color='Atendente', barmode='group')
        elif tipo == "Linha":
            fig = px.line(dados, x=x, y=y, color='Atendente')
        elif tipo == "Dispersão":
            fig = px.scatter(dados, x=x, y=y, color='Atendente')
        elif tipo == "Boxplot":
            fig = px.box(dados, x='Atendente', y=y)
        elif tipo == "Rosca":
            fig = px.pie(dados, values=y, names=x, hole=0.3)
        return fig

    # Visualizações dinâmicas
    for metrica in metricas:
        st.header(f"Análise de {metrica}")
        
        if metrica == "Quantidade de Atendimentos":
            dados_agrupados = df_filtrado['Atendente'].value_counts().reset_index()
            dados_agrupados.columns = ['Atendente', 'Quantidade']
            fig = criar_grafico(dados_agrupados, 'Atendente', 'Quantidade', tipo_grafico)
        else:
            coluna = f"{metrica}_minutos"
            dados_agrupados = df_filtrado.groupby('Atendente')[coluna].mean().reset_index()
            fig = criar_grafico(dados_agrupados, 'Atendente', coluna, tipo_grafico)
        
        st.plotly_chart(fig)

    # Análise temporal
    st.header("Análise Temporal")
    metrica_temporal = st.selectbox("Escolha a métrica para análise temporal", 
                                    ["Tempo total em atendimento_minutos", "Tempo total em fila_minutos", "Tempo na última fila_minutos"])
    
    df_filtrado['Data'] = df_filtrado['Data da abertura'].dt.date
    dados_temporais = df_filtrado.groupby('Data')[metrica_temporal].mean().reset_index()
    
    fig_temporal = px.line(dados_temporais, x='Data', y=metrica_temporal, title=f"Evolução de {metrica_temporal} ao longo do tempo")
    st.plotly_chart(fig_temporal)

    # Correlações
    st.header("Matriz de Correlação")
    colunas_correlacao = [col for col in df_filtrado.columns if col.endswith('_minutos')]
    matriz_correlacao = df_filtrado[colunas_correlacao].corr()
    
    fig_correlacao = px.imshow(matriz_correlacao, text_auto=True, aspect="auto")
    st.plotly_chart(fig_correlacao)

    # Resumo dos dados
    st.header("Resumo dos Dados")
    
    # Estatísticas gerais
    total_atendimentos = df_filtrado.shape[0]
    media_tempo_atendimento = df_filtrado['Tempo total em atendimento_minutos'].mean()
    media_tempo_fila = df_filtrado['Tempo total em fila_minutos'].mean()
    
    st.write(f"Total de atendimentos: {total_atendimentos}")
    st.write(f"Tempo médio de atendimento: {media_tempo_atendimento:.2f} minutos")
    st.write(f"Tempo médio em fila: {media_tempo_fila:.2f} minutos")
    
    # Top 5 atendentes por quantidade de atendimentos
    top_atendentes = df_filtrado['Atendente'].value_counts().head()
    st.subheader("Top 5 Atendentes por Quantidade de Atendimentos")
    st.write(top_atendentes)
    
    # Estatísticas por atendente
    st.subheader("Estatísticas por Atendente")
    estatisticas_atendente = df_filtrado.groupby('Atendente').agg({
        'Tempo total em atendimento_minutos': 'mean',
        'Tempo total em fila_minutos': 'mean',
        'Atendente': 'count'
    }).rename(columns={
        'Tempo total em atendimento_minutos': 'Tempo Médio de Atendimento (min)',
        'Tempo total em fila_minutos': 'Tempo Médio em Fila (min)',
        'Atendente': 'Quantidade de Atendimentos'
    }).round(2)
    
    st.write(estatisticas_atendente)

else:
    st.write("Por favor, envie uma planilha do Excel para continuar.")