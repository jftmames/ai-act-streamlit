import streamlit as st
import yaml
import pandas as pd
from pathlib import Path

st.title("Rúbrica de sesgo y cumplimiento (0–100)")

@st.cache_data
def load_rubric():
    p = Path("data/rules/bias_rubric.yaml")
    return yaml.safe_load(p.read_text(encoding="utf-8"))

cfg = load_rubric()
segmento = st.session_state.get("segment", "Enterprise")

st.subheader(f"Segmento: {segmento}")
st.write("Valora cada criterio: 0 (no cumple) · 1 (parcial) · 2 (cumple).")

scores = {}
weights = {}
for c in cfg["criteria"]:
    val = st.radio(c["label"], [0,1,2], horizontal=True, index=0, key=c["id"])
    scores[c["id"]] = int(val)
    weights[c["id"]] = int(c["weight"])

raw = sum(scores[k]*weights[k] for k in scores)
max_raw = sum(2*weights[k] for k in scores)
pct = int(round(100*raw/max_raw)) if max_raw else 0

st.success(f"Puntuación total: **{pct}/100**")

# mini gráfico
df = pd.DataFrame({
    "criterio": [c["label"] for c in cfg["criteria"]],
    "puntos": [scores[c["id"]]*weights[c["id"]] for c in cfg["criteria"]]
}).set_index("criterio")
st.bar_chart(df)

# exportar markdown
md = f"""# Rúbrica de sesgo — Resultado
**Segmento:** {segmento}  
**Puntuación:** {pct}/100

## Detalle por criterio
""" + "\n".join([f"- {c['label']}: {scores[c['id']]} (peso {weights[c['id']]})" for c in cfg["criteria"]])

st.download_button("Descargar resultado (Markdown)", md.encode("utf-8"),
                   file_name="rubrica_sesgo.md", mime="text/markdown")
