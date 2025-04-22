# ia_trends_panel.py – Panel visual moderno con gráficos reales por IA
import os
import json
import streamlit as st
from glob import glob
from datetime import datetime
import plotly.express as px

st.subheader("📊 Tendencias Automáticas Detectadas por IA")

# Cargar archivos generados por IA
archivos = sorted(glob("data/auto_trends_*.json"), reverse=True)

if not archivos:
    st.warning("Aún no hay datos generados por la IA.")
else:
    opciones = [os.path.basename(f).replace("auto_trends_", "").replace(".json", "") for f in archivos]
    seleccionado = st.selectbox("Selecciona un rango de análisis:", opciones)
    archivo = f"data/auto_trends_{seleccionado}.json"

    with open(archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)

    # Preparar data para gráfico
    productos = []
    plataformas = []
    apariciones = []

    for nombre, veces in list(datos.items())[:30]:
        productos.append(nombre.split(" (")[0])
        plataformas.append(nombre.split(" (")[1].replace(")", ""))
        apariciones.append(veces)

    df = {
        "Producto": productos,
        "Plataforma": plataformas,
        "Frecuencia": apariciones
    }

    fig = px.bar(
        df,
        x="Frecuencia",
        y="Producto",
        color="Plataforma",
        orientation="h",
        title=f"Productos más detectados por IA ({seleccionado})",
        template="plotly_dark",
        height=700
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.info("Estos resultados son generados automáticamente por la IA, sin intervención manual.")

# --- Smart Cart always on ---
import smart_cart
