import streamlit as st
import json
from datetime import datetime

st.title("Model Card Builder")

with st.form("mc"):
    model_name = st.text_input("Nombre del modelo", "Clasificador X")
    version = st.text_input("Versión", "1.0")
    owner = st.text_input("Owner / Equipo", "Equipo IA")
    intended_use = st.text_area("Uso previsto", "Scoring de crédito en banca minorista.")
    training_data = st.text_area("Datos de entrenamiento", "Dataset interno + público. Sin datos sensibles.")
    metrics = st.text_area("Métricas", "Accuracy 0.89; F1 0.86; por grupos: ...")
    limitations = st.text_area("Limitaciones", "Rendimiento inferior en datos escasos; no usar para...")
    ethical = st.text_area("Consideraciones éticas", "Revisión humana; transparencia; canales de reclamación.")
    contact = st.text_input("Contacto", "compliance@acme.com")
    submitted = st.form_submit_button("Generar Model Card")

if submitted:
    obj = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "model_name": model_name,
        "version": version,
        "owner": owner,
        "intended_use": intended_use,
        "training_data": training_data,
        "metrics": metrics,
        "limitations": limitations,
        "ethical_considerations": ethical,
        "contact": contact
    }
    js = json.dumps(obj, ensure_ascii=False, indent=2)
    st.success("Model Card generada.")
    st.download_button("Descargar JSON", js.encode("utf-8"),
                       file_name="model_card.json", mime="application/json")

    md = f"""# Model Card
**Modelo:** {model_name} (v{version})  
**Owner:** {owner}  
**Creado:** {obj['created_at']}

## Uso previsto
{intended_use}

## Datos de entrenamiento
{training_data}

## Métricas
{metrics}

## Limitaciones
{limitations}

## Consideraciones éticas
{ethical}

## Contacto
{contact}
"""
    st.download_button("Descargar Markdown", md.encode("utf-8"),
                       file_name="model_card.md", mime="text/markdown")
