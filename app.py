import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


df_receitas = pd.read_excel('D:/PROJETO FINANCAS/PYTHON/dados/receitas.xlsx', sheet_name='receitas')
df_despesas = pd.read_excel('D:/PROJETO FINANCAS/PYTHON/dados/despesas.xlsx', sheet_name='despesas')

df_receitas['DATA_EMISSAO'] = df_receitas['DATA_EMISSAO'].dt.month
soma_receitas = df_receitas.groupby(['MES','DATA_EMISSAO','DESCRICAO_RECEITA','DESCRICAO_GRUPO'])['VALOR'].sum().reset_index().sort_values(by="DATA_EMISSAO")


# Título do app
st.title("Dashboard Finanças Pessoais")

#grafico 1 card soma_receitastório por tipo de receita
total = df_receitas.groupby("DESCRICAO_GRUPO")["VALOR"].sum()

a,b = st.columns(2)

a.metric(label='Receitas Tributadas',value= f'R$ {total["TRIBUTADA"]:,.2f}',border=True)
b.metric(label='Receitas Não Tributadas',value= f'R$ {total["NAO TRIBUTADA"]:,.2f}',border=True)

#grafico 2 - Tabela receitas
st.write("### Receitas detalhadas")
st.dataframe(soma_receitas)


#grafico 3 - soma_receitas receita por mes e tipo (barras duplas)
grafico3 = df_receitas.groupby(['MES', 'DATA_EMISSAO', 'DESCRICAO_GRUPO'])['VALOR'].sum().reset_index().sort_values(by="DATA_EMISSAO")
st.write("### Receitas por Mês e Tipo")
grafico3_fig = px.bar(
    grafico3,
    x='DATA_EMISSAO',
    y='VALOR',
    text_auto='.2s',
    color='DESCRICAO_GRUPO',
    barmode='group',
    labels={
        'VALOR':'Valor Total (R$)',
        'DATA_EMISSAO': 'Mês',
        'DESCRICAO_GRUPO': 'Tipo Receita'},
    hover_data={'VALOR': ':.2f'}
)
st.plotly_chart(grafico3_fig,use_container_width=True)

#despesas
df_despesas['DATA_EMISSAO'] = df_despesas['DATA_EMISSAO'].dt.month
soma_despesas = df_despesas.groupby(['MES','DATA_EMISSAO','DESCRICAO_DESPESA','DESCRICAO_GRUPO'])['VALOR'].sum().reset_index().sort_values(by="DATA_EMISSAO")


#grafico 4 card somatório por tipo de despesa
total_despesas = df_despesas.groupby("DESCRICAO_GRUPO")["VALOR"].sum()

c,d,e = st.columns(3)

c.metric(label='Despesas Fixas',value= f'R$ {total_despesas["FIXAS"]:,.2f}',border=True)
d.metric(label='Despesas Variáveis',value= f'R$ {total_despesas["VARIAVEIS"]:,.2f}',border=True)
e.metric(label='Deus',value= f'R$ {total_despesas["DEUS"]:,.2f}',border=True)


#grafico 5 - Tabela despesas
st.write("### Despesas detalhadas")
st.dataframe(soma_despesas)


#grafico 6 - soma despesa por mes e tipo (barras tripas)
grafico6 = df_despesas.groupby(['MES', 'DATA_EMISSAO', 'DESCRICAO_GRUPO'])['VALOR'].sum().reset_index().sort_values(by="DATA_EMISSAO")
st.write("### Despesas por Mês e Tipo")
grafico6_fig = px.bar(
    grafico6,
    x='DATA_EMISSAO',
    y='VALOR',
    text_auto='.2s',
    color='DESCRICAO_GRUPO',
    barmode='group',
    labels={
        'VALOR':'Valor Total (R$)',
        'DATA_EMISSAO': 'Mês',
        'DESCRICAO_GRUPO': 'Tipo Receita'},
    hover_data={'VALOR': ':.2f'}
)
st.plotly_chart(grafico6_fig,use_container_width=True)

#grafico 7 - receitas vs despesas
st.write("### Comparativo Receitas vs Despesas")

soma_despesas_mes = df_despesas.groupby(['DATA_EMISSAO'])['VALOR'].sum().reset_index().sort_values(by="DATA_EMISSAO")
soma_despesas_mes['TIPO'] = 'Despesa'

soma_receitas_mes = df_receitas[df_receitas["DESCRICAO_GRUPO"]=="TRIBUTADA"].groupby(['DATA_EMISSAO'])['VALOR'].sum().reset_index().sort_values(by="DATA_EMISSAO")
soma_receitas_mes['TIPO'] = 'Receita'

grafico7 = pd.concat([soma_receitas_mes, soma_despesas_mes])

grafico7_fig = px.bar(
    grafico7,
    x='DATA_EMISSAO',
    y='VALOR',
    text_auto='.2s',
    color='TIPO',
    color_discrete_map={'Receita': 'green', 'Despesa': 'red'},
    barmode='group',
    labels={
        'VALOR':'Valor Total (R$)',
        'DATA_EMISSAO': 'Mês',
        'TIPO': 'Tipo'},
    hover_data={'VALOR': ':.2f'}
)
st.plotly_chart(grafico7_fig,use_container_width=True)