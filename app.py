
import streamlit as st
import time
import json
import os
from datetime import datetime
from modules.ebay_search import buscar_ebay
from modules.mercado_libre import buscar_mercado_libre
from scraper.amazon_scraper import scrape_amazon
from ai.trend_detector import TrendDetector
from ai.review_analyzer import analyze_reviews
from database.mongo_handler import MongoDBHandler

# Visual configuration
st.set_page_config(page_title="TopWorldTrending", layout="wide")

# Initialize MongoDB
mongo = MongoDBHandler()

# Welcome screen
if "pantalla_bienvenida" not in st.session_state:
    st.session_state.pantalla_bienvenida = True

if st.session_state.pantalla_bienvenida:
    st.markdown("""
        <div style='text-align:center; padding-top: 80px;'>
            <h1 style='font-size:3.5em;'>TopWorldTrending</h1>
            <p style='font-size:1.4em; color:gray;'>Multi-Marketplace Product Analysis Tool</p>
            <img src='https://cdn-icons-png.flaticon.com/512/1170/1170576.png' width='150'/>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(2.5)
    st.session_state.pantalla_bienvenida = False
    st.rerun()

# Side menu
menu = st.sidebar.selectbox("Navigation Menu:", [
    "Dashboard",
    "Search Products",
    "AI Analysis",
    "Market Statistics",
    "Export Results"
])

# DASHBOARD
if menu == "Dashboard":
    st.title("Dashboard")
    st.markdown("### Welcome to TopWorldTrending")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🔍 Search across multiple marketplaces")
    with col2:
        st.info("🤖 AI-powered trend analysis")
    with col3:
        st.info("📊 Real-time market statistics")

# SEARCH
elif menu == "Search Products":
    st.title("Multi-Marketplace Search")
    
    col1, col2 = st.columns(2)
    with col1:
        product = st.text_input("Enter product to search:")
        platform = st.selectbox("Select platform", ["Amazon", "eBay", "Mercado Libre"])
    with col2:
        max_results = st.slider("Maximum results", 5, 50, 10)
        country = st.selectbox("Select country", ["US", "MX", "UK"])

    if st.button("Search products") and product:
        with st.spinner("Searching products..."):
            results = []
            if platform == "Amazon":
                results = scrape_amazon(product, country=country, max_pages=1)
            elif platform == "eBay":
                results = buscar_ebay(product, os.getenv("EBAY_APP_ID"))
            elif platform == "Mercado Libre":
                results = buscar_mercado_libre('MLM', product, max_results)

            if not results.empty:
                st.success(f"Found {len(results)} products!")
                for _, row in results.iterrows():
                    with st.expander(f"{row['Title'][:100]}..."):
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.image(row.get('Image', ''), width=150)
                        with col2:
                            st.write(f"**Price:** ${row['Price']}")
                            st.write(f"[View product]({row.get('Link', row.get('url', '#'))})")

# AI ANALYSIS
elif menu == "IA - Tendencias":
    from ia_trends_panel import *


# STATISTICS
elif menu == "Market Statistics":
    st.title("Market Statistics")
    files = [f for f in os.listdir("data") if f.endswith(".csv")]
    
    if files:
        file = st.selectbox("Select dataset:", files)
        if st.button("Generate statistics"):
            import pandas as pd
            import matplotlib.pyplot as plt
            
            df = pd.read_csv(f"data/{file}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Price Distribution")
                fig, ax = plt.subplots()
                df['Price'].hist(ax=ax)
                st.pyplot(fig)
            
            with col2:
                st.subheader("Summary Statistics")
                st.write(df.describe())
    else:
        st.info("No data available. Start by searching for products.")

# Footer
st.markdown("""
---
<div style='text-align: center; color: gray;'>
    Made with ❤️ by TopWorldTrending | Powered by Multiple Marketplaces
</div>
""", unsafe_allow_html=True)
