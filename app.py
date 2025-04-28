import streamlit as st
from modules.amazon_search import buscar_amazon
from modules.ebay_search import buscar_ebay
from modules.mercado_libre import buscar_mercado_libre
import json
import os

# Configuración inicial de la app
st.set_page_config(
    page_title="TopWorldTrending",
    page_icon="🛒",
    layout="wide"
)

# Pantalla de bienvenida
def pantalla_bienvenida():
    st.markdown("<h1 style='text-align: center;'>TopWorldTrending</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: grey;'>Smarter product analysis. More marketplaces. One powerful tool.</h3>", unsafe_allow_html=True)
    st.image('assets/background.jpg', use_column_width=True)
    st.markdown("---")

# Login de usuario básico (modo de prueba)
def login_usuario():
    st.sidebar.subheader("Iniciar Sesión")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if username == "admin" and password == "admin123":
            st.session_state['logueado'] = True
            st.success("¡Inicio de sesión exitoso!")
        else:
            st.error("Credenciales inválidas")

# Selector de plataforma
def buscar_productos():
    st.header("🔎 Buscar Productos en Tendencia")
    plataforma = st.selectbox("Selecciona plataforma", ["Amazon", "eBay", "Mercado Libre"])
    query = st.text_input("¿Qué producto deseas buscar?")
    
    if st.button("Buscar"):
        if query:
            with st.spinner('Buscando productos...'):
                if plataforma == "Amazon":
                    resultados = buscar_amazon(query)
                elif plataforma == "eBay":
                    resultados = buscar_ebay(query)
                else:
                    resultados = buscar_mercado_libre(query)

            if resultados:
                for producto in resultados:
                    st.write(f"### {producto['titulo']}")
                    st.image(producto['imagen'], width=150)
                    st.write(f"Precio: ${producto['precio']}")
                    st.markdown(f"[Ver producto]({producto['link']})")
                    st.markdown("---")
            else:
                st.warning("No se encontraron resultados para esta búsqueda.")
        else:
            st.warning("Por favor ingresa un término de búsqueda.")

# Panel de IA - Productos en tendencia
def panel_ai_trends():
    st.header("🧠 Tendencias de Productos AI")
    if os.path.exists('data/ai_trends.json'):
        with open('data/ai_trends.json', 'r', encoding='utf-8') as f:
            datos = json.load(f)
        for tendencia in datos.get('tendencias', []):
            st.subheader(tendencia['nombre_categoria'])
            for producto in tendencia['productos']:
                st.write(f"**{producto['titulo']}** - ${producto['precio']}")
                st.markdown(f"[Ver más]({producto['link']})")
                st.markdown("---")
    else:
        st.info("No hay tendencias todavía. Ejecuta el recolector o espera la próxima actualización automática.")

# Main
def main():
    if 'logueado' not in st.session_state:
        st.session_state['logueado'] = False

    pantalla_bienvenida()

    if not st.session_state['logueado']:
        login_usuario()
    else:
        menu = st.sidebar.selectbox("Menú", ["Buscar Productos", "Tendencias AI", "Cerrar Sesión"])

        if menu == "Buscar Productos":
            buscar_productos()
        elif menu == "Tendencias AI":
            panel_ai_trends()
        elif menu == "Cerrar Sesión":
            st.session_state['logueado'] = False
            st.experimental_rerun()

if __name__ == "__main__":
    main()
