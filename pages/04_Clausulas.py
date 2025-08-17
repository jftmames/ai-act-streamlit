import streamlit as st
import yaml
from pathlib import Path

st.title("Generador de cláusulas contractuales (IA/Compliance)")

@st.cache_data
def load_clauses():
    p = Path("data/templates/clauses.yaml")
    return yaml.safe_load(p.read_text(encoding="utf-8"))

cfg = load_clauses()

st.subheader("Selecciona jurisdicción y opciones")
juris = st.selectbox("Jurisdicción", ["eu","es"])
opt_expl = st.checkbox("Explicabilidad (explainability)", True)
opt_bias = st.checkbox("Pruebas de sesgo (bias testing)", True)
opt_inc  = st.checkbox("Notificación de incidentes", True)

parts = []
# básicas de la jurisdicción
for key in cfg["jurisdictions"][juris]:
    parts.append(cfg["jurisdictions"][juris][key])

# opciones
if opt_expl:
    parts.append(cfg["options"]["explainability"]["standard"])
if opt_bias:
    parts.append(cfg["options"]["bias_testing"]["standard"])
if opt_inc:
    parts.append(cfg["options"]["incident_notice"]["standard"])

text = "\n\n".join([f"• {p}" for p in parts])

st.markdown("### Vista previa")
st.write(text)

st.download_button("Descargar cláusulas (Markdown)", text.encode("utf-8"),
                   file_name="clausulas_ia.md", mime="text/markdown")
