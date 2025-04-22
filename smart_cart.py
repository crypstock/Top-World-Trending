# smart_cart.py – Smart Cart IA helper (carrito animado + chat + filtrado)
# ---------------------------------------------------------------------
# Dependencias (añádelas a requirements.txt):
#   streamlit-lottie
#   streamlit-chat
#   openai  (si usarás GPT‑4 o GPT‑3.5 para respuestas)
# ---------------------------------------------------------------------
import streamlit as st
from streamlit_lottie import st_lottie
import streamlit_chat as stc
import requests
import os
import json

# 1️⃣  Función para cargar animación Lottie -------------------------------------------------

def load_lottie(url: str):
    """Descarga un JSON de Lottie y lo devuelve en formato dict"""
    r = requests.get(url)
    if r.status_code != 200:
        st.warning("❌ No pude cargar la animación Lottie")
        return None
    return r.json()

# 2️⃣  Cargar la animación del carrito ------------------------------------------------------
# Puedes reemplazar la URL por cualquier Lottie de tu agrado
cart_lottie_json = load_lottie(
    "https://lottie.host/0efcb4e4-1080-4ede-825d-6f1ceb8f53d1/ihgVvkXy0c.json"
)

# 3️⃣  Dibujar el carrito en posición fija en la esquina -----------------------------------
# Sólo lo pintamos una vez; luego usamos un botón Streamlit para abrir chat.

def draw_cart():
    """Renderiza el carrito animado fijo en la esquina"""
    cart_container = st.container()
    with cart_container:
        st.markdown(
            """
            <div style="position:fixed; bottom:25px; right:25px; z-index:1000;">
                <div id="smartcart-lottie" style="cursor:pointer;"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st_lottie(cart_lottie_json, height=120, key="smartcart")

# 4️⃣  Crear/leer estado de sesión para chat -----------------------------------------------

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# 5️⃣  Botón emergente para abrir/cerrar chat ----------------------------------------------
# Ponemos un botón flotante. Streamlit no permite botones flotantes fuera del flujo, así que
# mostramos un botón normal (puedes estilizarlo con HTML/CSS si deseas).

with st.sidebar.expander("🤖 Smart Cart Chat"):
    if st.button("💬 Abrir / Cerrar Chat"):
        st.session_state.chat_open = not st.session_state.chat_open

# 6️⃣  Lógica del chat interactivo -----------------------------------------------------------

def process_question(msg: str):
    """Ejemplo de respuesta. Sustitúyelo por llamada a OpenAI o lógica personalizada"""
    msg_lower = msg.lower()
    if "filtra" in msg_lower and "tecnologia" in msg_lower:
        st.session_state.category_filter = "Electrónica"
        return "He aplicado el filtro de categoría: Electrónica ✅"
    elif "exporta" in msg_lower:
        # marca bandera para exportar
        st.session_state.export_table = True
        return "Generando archivo Excel... 📄"
    else:
        return "Lo siento, todavía estoy aprendiendo. ¡Intenta otra pregunta!"

if st.session_state.chat_open:
    st.markdown("---")
    st.header("🤖 Smart Cart Chat")
    if "history" not in st.session_state:
        st.session_state.history = []

    # Mostrar historial
    for entry in st.session_state.history:
        role, text = entry
        stc.chat_message_container(role, text)

    user_input = st.text_input("Escribe tu pregunta y presiona Enter:", key="chat_input")
    if user_input:
        st.session_state.history.append(("user", user_input))
        respuesta = process_question(user_input)
        st.session_state.history.append(("assistant", respuesta))
        st.rerun()

# 7️⃣  Demo de cómo actuar sobre un DataFrame filtrado --------------------------------------

def show_dataframe_demo():
    import pandas as pd
    st.subheader("🗃 Tabla de productos de ejemplo")
    data = {
        "Producto": ["iPhone", "PS5", "Air Fryer", "Laptop Dell"],
        "Categoría": ["Electrónica", "Videojuegos", "Hogar", "Computadoras"],
        "Plataforma": ["Amazon", "eBay", "Mercado Libre", "Amazon"],
        "Precio": [799, 499, 99, 899],
    }
    df = pd.DataFrame(data)

    # Aplicar filtro si lo solicitó el chat
    cat_filter = st.session_state.get("category_filter")
    if cat_filter:
        df = df[df["Categoría"] == cat_filter]
        st.success(f"Filtro activo: {cat_filter}")

    st.dataframe(df, use_container_width=True)

    # Exportar si lo pidió el chat
    if st.session_state.get("export_table"):
        import io
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        st.download_button(
            "Descargar Excel", buffer.getvalue(), file_name="productos.xlsx"
        )
        st.session_state.export_table = False

# Llamar a demo de tabla (en tu app real usarás tus datos)
show_dataframe_demo()

# Renderiza carrito
draw_cart()
