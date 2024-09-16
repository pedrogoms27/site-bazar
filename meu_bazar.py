import streamlit as st
import pandas as pd
import altair as alt

CSV_FILE = "dados_bazar.csv"

def carregar_dados():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Mês", "Ganho", "Peças Vendidas"])

def salvar_dados(df):
    df.to_csv(CSV_FILE, index=False)

# Carregar e preparar os dados
df = carregar_dados()

# Ordem dos meses e mapeamento
ordem_meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
               "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
numeros_meses = range(1, 13)
mes_para_numero = dict(zip(ordem_meses, numeros_meses))

df["Número do Mês"] = df["Mês"].map(mes_para_numero)
df["Mês"] = pd.Categorical(df["Mês"], categories=ordem_meses, ordered=True)
df = df.sort_values("Número do Mês")

st.title("Controle de Ganhos e Peças Vendidas Mensais do Bazar")

# Adicionar ou Atualizar Ganhos e Peças Vendidas
st.header("Adicionar ou Atualizar Ganhos e Peças Vendidas")
mes = st.selectbox("Selecione o mês:", df["Mês"].cat.categories)
ganho = st.number_input("Valor dos Ganhos do Mês:", min_value=0.0, format="%.2f")
pecas_vendidas = st.number_input("Quantidade de Peças Vendidas:", min_value=0)

if st.button("Adicionar/Atualizar Registro"):
    if ganho > 0 and pecas_vendidas > 0:
        if mes in df["Mês"].values:
            df.loc[df["Mês"] == mes, ["Ganho", "Peças Vendidas"]] = [ganho, pecas_vendidas]
        else:
            novo_registro = {"Mês": mes, "Ganho": ganho, "Peças Vendidas": pecas_vendidas}
            df = pd.concat([df, pd.DataFrame([novo_registro])], ignore_index=True)
        st.success(f"Registro de {mes} atualizado com R${ganho:.2f} e {pecas_vendidas} peças vendidas.")
        df["Número do Mês"] = df["Mês"].map(mes_para_numero)
        df = df.sort_values("Número do Mês")
        salvar_dados(df)
    else:
        st.error("Por favor, insira valores válidos para ganho e peças vendidas.")

# Exibir Dados Acumulados
st.header("Dados Acumulados")
# Exibir a coluna "Número do Mês" para verificar a ordenação
df_exibicao = df[["Número do Mês", "Mês", "Ganho", "Peças Vendidas"]]
st.dataframe(df_exibicao)

total_ganhos = df["Ganho"].sum()
total_pecas = df["Peças Vendidas"].sum()
st.subheader(f"Total Acumulado: R${total_ganhos:.2f}")
st.subheader(f"Total de Peças Vendidas: {total_pecas}")

# Exibir Gráficos
st.header("Gráficos")
opcao_grafico = st.selectbox("Selecione o gráfico:", ["Ganhos Mensais", "Peças Vendidas Mensais"])

mes_inicio = st.selectbox("Selecione o mês de início:", df["Mês"].cat.categories, index=0)
mes_fim = st.selectbox("Selecione o mês de fim:", df["Mês"].cat.categories, index=len(df["Mês"].cat.categories) - 1)

df_filtrado = df[df["Mês"].between(mes_inicio, mes_fim)]

if opcao_grafico == "Ganhos Mensais":
    grafico = alt.Chart(df_filtrado).mark_line(point=True).encode(
        x=alt.X('Mês', sort=ordem_meses),
        y='Ganho',
        tooltip=['Mês', 'Ganho']
    ).properties(title='Ganhos Mensais')
else:
    grafico = alt.Chart(df_filtrado).mark_bar().encode(
        x=alt.X('Mês', sort=ordem_meses),
        y='Peças Vendidas',
        tooltip=['Mês', 'Peças Vendidas']
    ).properties(title='Peças Vendidas Mensais')

st.altair_chart(grafico, use_container_width=True)