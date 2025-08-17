import streamlit as st

st.set_page_config(page_title="AI Act MVP", layout="centered")

st.title("AI Act MVP — Suite Streamlit (demo)")
st.write("Checklist de riesgo → AIA/DPIA → Rúbrica de sesgo → Cláusulas → Auditoría Express → Model Card.")

SEGMENTOS = ["Enterprise", "Mid", "Startup", "Público", "Consultoría", "ONG"]
if "segment" not in st.session_state:
    st.session_state.segment = SEGMENTOS[0]

st.selectbox("Selecciona segmento de cliente", SEGMENTOS, key="segment")

st.markdown("### Navegación")
st.page_link("pages/01_Checklist.py", label="1) Checklist de riesgo")
st.page_link("pages/02_AIA_DPIA.py", label="2) Generar AIA/DPIA")
st.page_link("pages/03_Rubrica_Sesgo.py", label="3) Rúbrica de sesgo")
st.page_link("pages/04_Clausulas.py", label="4) Cláusulas contractuales")
st.page_link("pages/05_Auditoria_Express.py", label="5) Auditoría Express")
st.page_link("pages/06_ModelCard.py", label="6) Model Card")
st.info("Consejo: recorre el flujo en orden y descarga los informes en cada paso.")


st.markdown("---")
st.caption("Demo pública. Usa datos ficticios. Si necesitas almacenar datos reales en la UE, conéctalo a Supabase EU y no publiques la app.")

