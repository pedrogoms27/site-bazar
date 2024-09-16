import streamlit as st
import pandas as pd
import altair as alt

# Título do site
st.title("Controle de Ganhos e Peças Vendidas Mensais do Bazar")

# Dados iniciais
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

# Carregar os dados
df = pd.DataFrame(st.session_state['dados'])
df["Mês"] = pd.Categorical(df["Mês"], categories=[
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], ordered=True)
df = df.sort_values("Mês")

# Seção de Adição/Atualização de Dados
st.header("Adicionar ou Atualizar Ganhos e Peças Vendidas")
mes = st.selectbox("Selecione o mês:", df["Mês"].cat.categories)
ganho = st.number_input("Valor dos Ganhos do Mês:", min_value=0.0, format="%.2f")
pecas_vendidas = st.number_input("Quantidade de Peças Vendidas:", min_value=0)

if st.button("Adicionar/Atualizar Registro"):
    if ganho > 0 and pecas_vendidas > 0:
        mes_encontrado = False
        for registro in st.session_state['dados']:
            if registro['Mês'] == mes:
                registro['Ganho'] = ganho
                registro['Peças Vendidas'] = pecas_vendidas
                mes_encontrado = True
                break
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

# Exibir dados acumulados
st.header("Dados Acumulados")
st.dataframe(df)

total_ganhos = df["Ganho"].sum()
total_pecas = df["Peças Vendidas"].sum()
st.subheader(f"Total Acumulado: R${total_ganhos:.2f}")
st.subheader(f"Total de Peças Vendidas: {total_pecas}")

# Seção de gráficos
st.header("Gráficos")
opcao_grafico = st.selectbox("Selecione o gráfico:", ["Ganhos Mensais", "Peças Vendidas Mensais"])

# Filtrar dados com base no mês selecionado
mes_inicio = st.selectbox("Selecione o mês de início:", df["Mês"].cat.categories, index=0)
mes_fim = st.selectbox("Selecione o mês de fim:", df["Mês"].cat.categories, index=len(df["Mês"].cat.categories) - 1)
df_filtrado = df[df["Mês"].between(mes_inicio, mes_fim)]

# Gráficos com Altair
if opcao_grafico == "Ganhos Mensais":
    grafico = alt.Chart(df_filtrado).mark_line(point=True).encode(
        x='Mês', y='Ganho'
    ).properties(
        title="Ganhos Mensais"
    )
else:
    grafico = alt.Chart(df_filtrado).mark_bar().encode(
        x='Mês', y='Peças Vendidas'
    ).properties(
        title="Peças Vendidas Mensais"
    )

st.altair_chart(grafico, use_container_width=True)