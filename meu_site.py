import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Controle de Ganhos e Peças Vendidas Mensais do Bazar")

if 'dados' not in st.session_state:
    st.session_state['dados'] = [
        {"Mês": "Janeiro", "Ganho": 1500.00, "Peças Vendidas": 50},
        {"Mês": "Fevereiro", "Ganho": 2300.50, "Peças Vendidas": 60},
        {"Mês": "Março", "Ganho": 1800.75, "Peças Vendidas": 45},
        {"Mês": "Abril", "Ganho": 2100.00, "Peças Vendidas": 55},
        {"Mês": "Maio", "Ganho": 1750.30, "Peças Vendidas": 40},
        {"Mês": "Junho", "Ganho": 2200.00, "Peças Vendidas": 65},
        {"Mês": "Julho", "Ganho": 1950.80, "Peças Vendidas": 48},
        {"Mês": "Agosto", "Ganho": 2000.40, "Peças Vendidas": 52},
        {"Mês": "Setembro", "Ganho": 2150.20, "Peças Vendidas": 58},
        {"Mês": "Outubro", "Ganho": 1980.75, "Peças Vendidas": 47},
        {"Mês": "Novembro", "Ganho": 2500.50, "Peças Vendidas": 70},
        {"Mês": "Dezembro", "Ganho": 2750.00, "Peças Vendidas": 80}
    ]

df = pd.DataFrame(st.session_state['dados'])
df["Mês"] = pd.Categorical(df["Mês"], categories=[
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], ordered=True)
df = df.sort_values("Mês")

st.header("Adicionar ou Atualizar Ganhos e Peças Vendidas")

mes = st.selectbox("Selecione o mês:", df["Mês"].cat.categories)
ganho = st.number_input("Valor dos Ganhos do Mês:", min_value=0.0, format="%.2f")
pecas_vendidas = st.number_input("Quantidade de Peças Vendidas:", min_value=0)

if st.button("Adicionar/Atualizar Registro"):
    if ganho > 0 and pecas_vendidas > 0:
        # Verifica se o mês já existe e atualiza os valores
        mes_encontrado = False
        for registro in st.session_state['dados']:
            if registro['Mês'] == mes:
                registro['Ganho'] = ganho
                registro['Peças Vendidas'] = pecas_vendidas
                mes_encontrado = True
                break
        # Se o mês não for encontrado, adiciona um novo registro
        if not mes_encontrado:
            st.session_state['dados'].append({"Mês": mes, "Ganho": ganho, "Peças Vendidas": pecas_vendidas})
        st.success(f"Registro de {mes} atualizado com R${ganho:.2f} e {pecas_vendidas} peças vendidas.")
        df = pd.DataFrame(st.session_state['dados'])
        df["Mês"] = pd.Categorical(df["Mês"], categories=[
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], ordered=True)
        df = df.sort_values("Mês")
    else:
        st.error("Por favor, insira valores válidos para ganho e peças vendidas.")

st.header("Dados Acumulados")
st.dataframe(df)

total_ganhos = df["Ganho"].sum()
total_pecas = df["Peças Vendidas"].sum()
st.subheader(f"Total Acumulado: R${total_ganhos:.2f}")
st.subheader(f"Total de Peças Vendidas: {total_pecas}")

st.header("Gráficos")

opcao_grafico = st.selectbox("Selecione o gráfico:", ["Ganhos Mensais", "Peças Vendidas Mensais"])

mes_inicio = st.selectbox("Selecione o mês de início:", df["Mês"].cat.categories, index=0)
mes_fim = st.selectbox("Selecione o mês de fim:", df["Mês"].cat.categories, index=len(df["Mês"].cat.categories) - 1)

df_filtrado = df[df["Mês"].between(mes_inicio, mes_fim)]

if opcao_grafico == "Ganhos Mensais":
    fig = px.line(df_filtrado, x="Mês", y="Ganho", title="Ganhos Mensais",
                  labels={"Mês": "Mês", "Ganho": "Ganho (R$)"}, markers=True)
else:
    fig = px.bar(df_filtrado, x="Mês", y="Peças Vendidas", title="Peças Vendidas Mensais",
                 labels={"Mês": "Mês", "Peças Vendidas": "Peças Vendidas"})

st.plotly_chart(fig)