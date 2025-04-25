# 🚀 TopWorldTrending

**La herramienta definitiva para encontrar productos en tendencia** en Amazon, eBay y Mercado Libre, impulsada por inteligencia artificial (IA) y scraping automatizado.

> “Smarter product analysis. More marketplaces. One powerful tool.”

---

## 🧠 ¿Qué es TopWorldTrending?

TopWorldTrending es una app moderna, visual e inteligente que:
- Recolecta productos en tendencia **automáticamente cada día** con GPT-4o
- Utiliza datos reales desde:
  - 🟣 **Amazon Product Advertising API**
  - 🔵 **eBay Browse API**
  - 🟡 **Mercado Libre Search API**
- Muestra estadísticas y análisis con una **interfaz profesional en Streamlit**
- Se ejecuta en la nube usando **Render.com** o como app local

---

## 🛠️ Tecnologías Utilizadas

- `Python`
- `Streamlit` (para la interfaz)
- `OpenAI GPT-4o` (para generar keywords)
- `requests`, `dotenv`, `amazon-paapi`, `pymongo` (dependencias clave)
- APIs oficiales de Amazon, eBay y Mercado Libre

---

## 🗂️ Estructura del proyecto

TopWorldTrending/ ├── app.py # Interfaz visual principal ├── auto_trend_collector.py # Script de IA recolectora automática ├── modules/ │ ├── amazon_search.py │ ├── ebay_search.py │ └── mercado_libre.py ├── data/ # Tendencias almacenadas (JSONs) ├── requirements.txt # Dependencias ├── .env.example # Variables necesarias para funcionamiento └── README.md # Este documento
