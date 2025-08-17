import streamlit as st
from datetime import datetime

st.title("Auditoría Express (preliminar)")

segmento = st.session_state.get("segment", "Enterprise")
st.subheader(f"Segmento: {segmento}")

with st.form("auditoria"):
    st.markdown("**1) Contexto de uso**")
    ctx_sector = st.selectbox("Sector", ["Banca","Salud","Educación","Público","Retail","Otro"])
    ctx_decision = st.selectbox("Impacto en decisiones", ["Bajo","Medio","Alto"])

    st.markdown("**2) Datos**")
    datos_sens = st.radio("¿Hay datos sensibles/biometría?", ["No","Sí"], horizontal=True)
    datos_men  = st.radio("¿Hay menores/colectivos vulnerables?", ["No","Sí"], horizontal=True)

    st.markdown("**3) Controles actuales**")
    ctrl_rev   = st.radio("¿Revisión humana obligatoria?", ["No","Sí"], horizontal=True)
    ctrl_logs  = st.radio("¿Trazabilidad (logs) de decisiones?", ["No","Sí"], horizontal=True)
    ctrl_trans = st.radio("¿Transparencia/explicabilidad previstas?", ["No","Sí"], horizontal=True)

    submitted = st.form_submit_button("Calcular y generar informe")

def score_val():
    score = 0
    if ctx_decision=="Alto": score += 2
    if datos_sens=="Sí": score += 2
    if datos_men=="Sí": score += 2
    if ctrl_rev=="Sí": score -= 1
    if ctrl_logs=="Sí": score -= 1
    if ctrl_trans=="Sí": score -= 1
    label = "ALTO" if score>=3 else ("MEDIO" if score>=1 else "BAJO")
    return score, label

if submitted:
    score, label = score_val()
    st.success(f"Resultado preliminar: **{label}** (score {score})")

    md = f"""# Auditoría Express — Resumen
**Fecha:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Segmento:** {segmento}
**Sector:** {ctx_sector}
**Impacto en decisiones:** {ctx_decision}

## Riesgo preliminar
**{label}** (score {score})

## Datos
- Sensibles/biometría: {datos_sens}
- Menores/vulnerables: {datos_men}

## Controles declarados
- Revisión humana: {ctrl_rev}
- Logs/trazabilidad: {ctrl_logs}
- Transparencia/explicabilidad: {ctrl_trans}

## Recomendaciones
- Ajustar controles en función del impacto y datos.
- Completar AIA/DPIA si el riesgo es MEDIO/ALTO.
- Definir cláusulas contractuales y pruebas de sesgo periódicas.
"""

    st.markdown("### Vista previa (Markdown)")
    st.code(md, language="markdown")
    st.download_button("Descargar informe (Markdown)", md.encode("utf-8"),
                       file_name="auditoria_express.md", mime="text/markdown")
