import streamlit as st
from analise import view, select2, select3

st.set_page_config(
    page_title="Report Embargos",
    layout="wide"
)

st.title("Report Embargos")

fig = view()
st.pyplot(fig)

df = select2()
df2 = select3()

st.subheader("Detalhamento por Unidade")

utep = st.selectbox(
    "Selecione a UTEP",
    sorted(df["UTEP"].unique())
)

df_filtrado = df[df["UTEP"] == utep]

st.metric(
    "Total da UTEP",
    int(df_filtrado["TOTAL"].sum())
)

st.dataframe(
    df_filtrado,
    use_container_width=True
)

st.subheader("Base Completa")

st.dataframe(
    df,
    use_container_width=True
)
st.markdown(
    """
    <h6 style='text-align: center; color: gray;'>
        Disponível até 14/07/2026
    </h6>
    """,
    unsafe_allow_html=True
)
