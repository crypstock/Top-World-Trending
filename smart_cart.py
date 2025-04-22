from streamlit_lottie import st_lottie
import json
import os
import streamlit as st

# Ruta local al JSON
json_path = os.path.join("assets", "cart.json")
with open(json_path, "r", encoding="utf-8") as f:
    cart_lottie_json = json.load(f)

def draw_cart():
    with st.container():
        st.markdown(
            """
            <div style="position:fixed; bottom:25px; right:25px; z-index:1000;">
                <div id="smartcart-lottie"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st_lottie(cart_lottie_json, height=110, key="smartcart")