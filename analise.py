import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurações  iniciais
st.set_page_config(page_title="Dashboard - Despesas e Orçamentos", page_icon="📊", layout="wide")

df_despesas = pd.read_excel('despesas.xlsx')
df_orcamento = pd.read_excel('orcamento.xlsx')

# SIDEBAR
st.sidebar.header("Selecione os Filtros")

setores_disponiveis = df_orcamento['setor'].unique()  # Obtém todos os setores únicos
setores_selecionados = st.sidebar.multiselect('Selecione os setores', setores_disponiveis, default=setores_disponiveis)

# Filtrando os dados com base na seleção do setor
df_orcamento_filtrado = df_orcamento[df_orcamento['setor'].isin(setores_selecionados)]

# selecao_df_despesas = df_despesas.query('')

def Home():
    st.title('Análise de Despesas e Orçamentos da Empresa')

    st.markdown('- - -')

    # grafico de despesas por área
    df_despesas['mes_ano'] = df_despesas['data'].dt.month.astype(str)
    gasto_por_area = df_despesas.groupby(['mes_ano', 'setor'])['valor'].sum().reset_index()

    barras_gasto_por_area = px.bar(
        gasto_por_area,
        x='mes_ano',
        y='valor',
        color='setor',
        title='Gastos mensais por área',
        barmode='stack',
    )

    custo_por_area = df_despesas.groupby(['setor', 'tipo'])['valor'].sum().reset_index()
    barras_custo_por_area = px.bar(
        custo_por_area,
        x='setor',
        y='valor',
        color='setor',
        title='Custos por Setor',
        barmode='stack',
    )

    graf1, graf2 = st.columns(2)
    with graf1:
        st.plotly_chart(barras_gasto_por_area, use_container_width=True)
    with graf2:
        st.plotly_chart(barras_custo_por_area, use_container_width=True)

    df_orcamento['data'] = pd.to_datetime(df_orcamento['data'], format='%d/%m/%Y')

    # Criar coluna 'mes_ano' para facilitar o agrupamento
    df_orcamento['mes_ano'] = df_orcamento['data'].dt.to_period('M').astype(str)

    # Agrupar os dados por mes_ano para calcular o total previsto e realizado
    gasto_por_mes = df_orcamento.groupby(['mes_ano'])[['valor_realizado', 'valor_previsto']].sum().reset_index()

    # Gráfico de barras para comparar valor realizado vs valor previsto por mês
    barras_comparacao = px.bar(
        gasto_por_mes,
        x='mes_ano',
        y=['valor_realizado', 'valor_previsto'],
        barmode='group',
        title='Valor Realizado vs Valor Previsto por Mês',
        labels={'mes_ano': 'Mês/Ano', 'valor_realizado': 'Valor Realizado (R$)', 'valor_previsto': 'Valor Previsto (R$)'}
    )

    # Exibindo o gráfico
    st.plotly_chart(barras_comparacao, use_container_width=True)

    selecao_custo_outliers = df_despesas.groupby(['fornecedor', 'setor'])['valor'].sum().reset_index()

    # Calcular os quartis e o IQR para a coluna 'valor'
    Q1 = selecao_custo_outliers['valor'].quantile(0.25)
    Q3 = selecao_custo_outliers['valor'].quantile(0.75)

    IQR = Q3 - Q1

    # Definir os limites inferior e superior para detectar outliers
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    # Filtrar os outliers com base nos limites
    outliers = selecao_custo_outliers[(selecao_custo_outliers['valor'] < limite_inferior) | (selecao_custo_outliers['valor'] > limite_superior)]

    # Exibir os outliers
    st.write(outliers)

Home()