import streamlit as st

st.set_page_config(page_title="AI Act MVP", layout="centered")

st.title("AI Act MVP — Suite Streamlit (demo)")
st.write("Checklist de riesgo → AIA/DPIA. Sin instalar nada, todo desde GitHub.")

SEGMENTOS = ["Enterprise", "Mid", "Startup", "Público", "Consultoría", "ONG"]

if "segment" not in st.session_state:
    st.session_state.segment = SEGMENTOS[0]

st.selectbox("Selecciona segmento de cliente", SEGMENTOS, key="segment")

st.markdown("### Navegación")
st.page_link("pages/01_Checklist.py", label="1) Checklist de riesgo")
st.page_link("pages/02_AIA_DPIA.py", label="2) Generar AIA/DPIA")
st.info("Consejo: primero completa el Checklist; luego pasa a AIA/DPIA.")

