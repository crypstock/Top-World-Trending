# 📈 TopWorldTrending

**Smarter product analysis. More marketplaces. One powerful tool.**

TopWorldTrending es una aplicación inteligente que analiza productos en tendencia en Amazon, eBay y Mercado Libre utilizando Inteligencia Artificial.  
Te permite descubrir los productos más rentables y prometedores automáticamente, sin necesidad de hacer búsquedas manuales.

---

## 🚀 Características Principales

- 🔍 Buscador de productos en Amazon, eBay y Mercado Libre.
- 🧠 Inteligencia Artificial GPT-4o para sugerir tendencias de productos.
- 📊 Panel de visualización de tendencias automáticas recolectadas.
- 🌐 Integración directa con APIs reales.
- 💻 Despliegue rápido en Render y GitHub.

---

## 🛠️ Tecnologías Usadas

- **Python 3.11+**
- **Streamlit** (interfaz web dinámica)
- **OpenAI GPT-4o** (generación de palabras clave inteligentes)
- **Amazon PA-API** (Product Advertising API)
- **eBay Browse API** (búsqueda de productos)
- **Mercado Libre Public API**
- **MongoDB Atlas** (opcional para guardar tendencias)

---

## 📂 Estructura del Proyecto

```plaintext
TopWorldTrending/
│
├── app.py                    # Aplicación principal Streamlit
├── auto_trend_collector.py    # Recolector de tendencias AI
├── requirements.txt           # Dependencias
├── .env.example               # Variables de entorno necesarias
├── README.md                  # Documentación del proyecto
│
├── modules/                   # Motores de búsqueda
│    ├── amazon_search.py
│    ├── ebay_search.py
│    └── mercado_libre.py
│
├── utils/                     # Funciones auxiliares (opcional)
│    └── helpers.py
│
├── assets/                    # Imágenes, estilos
│    └── background.jpg (opcional)
│
└── data/                      # Tendencias recolectadas (se crea automáticamente)
