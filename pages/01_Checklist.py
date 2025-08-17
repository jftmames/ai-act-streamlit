import streamlit as st
import yaml
from pathlib import Path

st.title("Checklist de riesgo")

segmento = st.session_state.get("segment", "Enterprise")

@st.cache_data
def load_rules():
    p = Path("data/rules/risk_rules.yaml")
    return yaml.safe_load(p.read_text(encoding="utf-8"))

cfg = load_rules()
rules = cfg["rules"]
seg_key = {
    "Enterprise":"enterprise","Mid":"mid_market","Startup":"startup",
    "Público":"publico","Consultoría":"consultoria","ONG":"ong"
}[segmento]
seg_cfg = cfg["segment_overrides"][seg_key]
base_weights = {r["id"]: r["weight"] for r in rules}
weights = base_weights.copy()
for k,v in (seg_cfg.get("weight_adjustments") or {}).items():
    if k in weights:
        weights[k] += int(str(v))  # "+1" -> 1

answers = {}
st.subheader(f"Segmento: {segmento}")
with st.form("checklist"):
    for r in rules:
        answers[r["id"]] = st.radio(r["text"], ["No","Sí"], horizontal=True, index=0)
    submitted = st.form_submit_button("Calcular riesgo")

def score_and_label(answers):
    score = sum(weights[qid] for qid,val in answers.items() if val=="Sí")
    thr = seg_cfg.get("thresholds", {"high":6,"medium":4})
    if score >= thr["high"]:
        risk = "ALTO"
    elif score >= thr["medium"]:
        risk = "MEDIO"
    else:
        risk = "BAJO"
    return score, risk, thr

if submitted:
    score, risk, thr = score_and_label(answers)
    st.success(f"Riesgo: **{risk}** (puntuación {score}) — umbrales: alto≥{thr['high']} / medio≥{thr['medium']}")
    st.session_state["checklist_answers"] = answers
    st.session_state["checklist_score"] = score
    st.session_state["checklist_risk"]  = risk

    # resumen de “Sí”
    yes_items = [rid for rid,v in answers.items() if v=="Sí"]
    st.write("**Respuestas afirmativas:**", ", ".join(yes_items) if yes_items else "Ninguna.")
    st.page_link("pages/02_AIA_DPIA.py", label="➡ Ir a generar AIA/DPIA")
