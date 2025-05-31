import streamlit as st
import oracledb
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configurações de conexão com o Oracle
dsn = "localhost:1521/financas_db"
username = "SYS"
password = "masterkey"
sysdba = True

try:
    connection = oracledb.connect(
        user=username,
        password=password,
        dsn=dsn,
        mode=oracledb.SYSDBA if sysdba else None
    )
    st.success("Banco de dados conectado!")

    receitas = """
            SELECT 
                fr.data_emissao AS Data_Emissao,
                to_char(fr.data_emissao, 'MON') as Mes,
                fr.valor AS Valor,
                fr.recebedor AS Recebedor,
                r.descricao AS Descricao_Receita,
                rg.descricao AS Descricao_Grupo
            FROM
                faturas_receber fr
                LEFT JOIN receitas r ON fr.receita_id = r.receita_id
                LEFT JOIN receitas_grupo rg ON r.grupo = rg.grupo_id
    """

    despesas = """ 
            SELECT 
                fp.data_emissao AS Data_Emissao,
                to_char(fp.data_emissao, 'MON') as Mes,
                extract(month from fp.data_emissao) as mes_num,
                fp.valor AS Valor,
                d.descricao AS Descricao_despesa,
                dg.descricao AS Descricao_Grupo
            FROM
                faturas_pagar fp
                LEFT JOIN despesas d on fp.despesa_id = d.despesa_id
                LEFT JOIN despesas_grupo dg ON d.grupo_id = dg.grupo_id
            WHERE 
                fp.valor > 0
    """

    df_receitas = pd.read_sql(receitas, connection)
    df_despesas = pd.read_sql(despesas, connection)

    connection.close()

except oracledb.Error as error:
    st.error(f"Erro ao conectar ao Oracle: {error}")

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
    title='Receitas por tipo e mês',
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
st.write("### Receitas por Mês e Tipo")
grafico6_fig = px.bar(
    grafico6,
    x='DATA_EMISSAO',
    y='VALOR',
    text_auto='.2s',
    color='DESCRICAO_GRUPO',
    barmode='group',
    title='Receitas por tipo e mês',
    labels={
        'VALOR':'Valor Total (R$)',
        'DATA_EMISSAO': 'Mês',
        'DESCRICAO_GRUPO': 'Tipo Receita'},
    hover_data={'VALOR': ':.2f'}
)
st.plotly_chart(grafico6_fig,use_container_width=True)

#grafico 7 - soma despesa por mes e tipo (barras tripas)
grafico6 = df_despesas.groupby(['MES', 'DATA_EMISSAO', 'DESCRICAO_GRUPO'])['VALOR'].sum().reset_index().sort_values(by="DATA_EMISSAO")
st.write("### Receitas por Mês e Tipo")
grafico6_fig = px.bar(
    grafico6,
    x='DATA_EMISSAO',
    y='VALOR',
    text_auto='.2s',
    color='DESCRICAO_GRUPO',
    barmode='group',
    title='Despesas por tipo e mês',
    labels={
        'VALOR':'Valor Total (R$)',
        'DATA_EMISSAO': 'Mês',
        'DESCRICAO_GRUPO': 'Tipo Despesa'},
    hover_data={'VALOR': ':.2f'}
)
st.plotly_chart(grafico6_fig,use_container_width=True)