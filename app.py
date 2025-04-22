# app.py – Versión “Neo‑UI” profesional para TopWorldTrending 🌐📈
# ---------------------------------------------------------------
# Diseño basado en Streamlit + Tailwind‑like CSS inline + Plotly
# Pantalla de bienvenida con animación, login simple y panel visual.
# ---------------------------------------------------------------
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import os, json
from glob import glob
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="TopWorldTrending", layout="wide")

# ---------- CSS GLOBAL ---------- #
st.markdown(
    """
    <style>
    @keyframes fadeIn {
        0% {opacity:0; transform: translateY(20px);} 
        100% {opacity:1; transform: translateY(0);}
    }
    .hero {
        animation: fadeIn 1.6s ease-in-out forwards;
        font-family: 'Segoe UI', sans-serif;
        color: #f1f1f1;
    }
    .gradient-bg {
        background: radial-gradient(circle at top left, #203a79, #121212 70%);
        height: 100vh; display:flex; flex-direction:column; justify-content:center; align-items:center;
    }
    .btn-start {
        background:#004bff;border:none;padding:14px 30px;border-radius:8px;color:#fff;font-size:18px;cursor:pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Splash screen control ---------- #
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if not st.session_state.splash_done:
    st.markdown("""
        <div class="gradient-bg">
            <div class="hero" style="text‑align:center;">
                <h1 style="font‑size:4rem;margin-bottom:0.4em;">TopWorldTrending</h1>
                <p style="font‑size:1.4rem;">Smarter product analysis. More marketplaces. One powerful tool.</p>
                <img src="https://cdn-icons-png.flaticon.com/512/726/726814.png" width="120"/>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 👉  BOTÓN STREAMLIT
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Enter Dashboard"):
        st.session_state.splash_done = True
        st.experimental_rerun()

    st.stop()


# ---------- Login (demo) ---------- #
if "user" not in st.session_state:
    with st.sidebar:
        st.markdown("## 🔐 Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login") and user and pwd:
            st.session_state.user = user
            st.experimental_rerun()
        st.stop()

# ---------- UI Main ---------- #
st.sidebar.success(f"Logged as **{st.session_state.user}**")
menu = st.sidebar.radio("Navigate", ["Dashboard","AI Trends","Settings"])

# Dummy selector for date range
hoy = datetime.now().strftime("%Y-%m-%d")

if menu == "Dashboard":
    st.title("📊 Dashboard – Quick View")
    st.markdown("Métricas resumidas de las últimas 24 h.")
    col1,col2 = st.columns(2)
    col1.metric("Productos procesados", "1 240", "+8%")
    col2.metric("Palabras clave", "350", "+2.3%")

elif menu == "AI Trends":
    st.title("🧠 IA – Productos en Tendencia")
    archivos = sorted(glob("data/auto_trends_*.json"), reverse=True)
    if archivos:
        archivo = st.selectbox("📅 Fecha de análisis", archivos, format_func=lambda x: x.replace("data/auto_trends_",""))
        with open(archivo, "r", encoding="utf-8") as f:
            data = json.load(f)
        top = list(data.items())[:20]
        df = {"Producto":[k.split(" ("   )[0] for k,_ in top],
              "Plataforma":[k.split(" ("   )[1].replace(")","") for k,_ in top],
              "Frecuencia":[v for _,v in top]}
        fig = px.bar(df, x="Frecuencia", y="Producto", color="Plataforma", orientation="h", height=650, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos aún. Ejecuta auto_trend_collector.py o espera la próxima recolección.")

elif menu == "Settings":
    st.title("⚙️ Configuración")
    st.write("Aquí irán opciones de usuario y preferencias (pendiente de implementación).")
