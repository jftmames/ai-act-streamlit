import streamlit as st
from pathlib import Path

st.title("Generador AIA/DPIA")

segmento = st.session_state.get("segment", "Enterprise")
answers = st.session_state.get("checklist_answers")
score   = st.session_state.get("checklist_score")
risk    = st.session_state.get("checklist_risk")

if answers is None:
    st.warning("Primero completa el Checklist de riesgo.")
    st.page_link("pages/01_Checklist.py", label="Ir al Checklist")
    st.stop()

yes_items = [rid for rid,v in answers.items() if v=="Sí"]
yes_str = ", ".join(yes_items) if yes_items else "Ninguna respuesta afirmativa."

st.subheader("Datos para el informe")
sistema = st.text_input("Sistema evaluado", "Scoring de crédito (ejemplo)")
datos_contexto = st.text_area("Datos y contexto", "Identificación, ingresos, historial de pagos. Impacto: acceso a crédito.")
siguientes = st.text_area("Próximos pasos", "Revisión humana en rechazos; explicación al usuario; registrar logs.")

template = Path("data/templates/aia_template.md").read_text(encoding="utf-8")
md = (template
      .replace("{{segmento}}", segmento)
      .replace("{{riesgo}}", risk or "?")
      .replace("{{score}}", str(score or ""))
      .replace("{{sistema}}", sistema)
      .replace("{{checklist_yes}}", yes_str)
      .replace("{{datos_contexto}}", datos_contexto)
      .replace("{{siguientes_pasos}}", siguientes)
)

st.markdown("### Vista previa (Markdown)")
st.code(md, language="markdown")

st.download_button("Descargar informe (Markdown)", md.encode("utf-8"),
                   file_name="informe_aia_borrador.md", mime="text/markdown")

