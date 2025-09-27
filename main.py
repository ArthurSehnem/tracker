import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# -------------------------
# Configuração inicial
# -------------------------
st.set_page_config(page_title="Tracker de Alimentação", page_icon="🥗")

# Conexão Supabase
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase = create_client(url, key)

st.title("🥗 Tracker de Alimentação")

# -------------------------
# Registro do dia
# -------------------------
st.subheader("Novo registro")

parecer = st.selectbox(
    "Parecer do dia",
    [
        "Segui corretamente",
        "Mudando pouquíssimo ou com responsabilidade",
        "Completamente fora"
    ]
)

descricao = st.text_area("Como você se sentiu hoje?")

if st.button("Salvar"):
    supabase.table("tracker").insert({
        "data": datetime.now().isoformat(),
        "parecer": parecer,
        "descricao": descricao
    }).execute()
    st.success("Registro salvo com sucesso!")

# -------------------------
# Histórico do mês
# -------------------------
st.subheader("Histórico do mês")

dados = supabase.table("tracker").select("*").execute().data

if dados:
    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["data"]).dt.date

    # Filtra registros do mês atual
    hoje = date.today()
    df_mes = df[df["data"].apply(lambda x: x.month == hoje.month and x.year == hoje.year)]

    if not df_mes.empty:
        # Gráfico de contagem por parecer
        fig = px.histogram(
            df_mes,
            x="data",
            color="parecer",
            title="Distribuição dos pareceres no mês",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(df_mes.sort_values("data", ascending=False))
    else:
        st.info("Ainda não há registros para este mês.")
else:
    st.info("Nenhum registro encontrado.")