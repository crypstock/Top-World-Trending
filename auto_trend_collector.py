import os
import json
import requests
from openai import OpenAI
from modules.amazon_search import buscar_amazon
from modules.ebay_search import buscar_ebay
from modules.mercado_libre import buscar_mercado_libre
from datetime import datetime

# Configurar tu OpenAI API Key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Función para generar keywords usando IA
def generar_keywords():
    prompts = [
        "Dame una lista de 10 palabras clave de productos populares este mes para Amazon, eBay y Mercado Libre."
    ]
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompts[0]}]
    )
    texto = respuesta.choices[0].message.content
    keywords = [line.strip("- ").strip() for line in texto.split("\n") if line]
    return keywords

# Función principal para recolectar tendencias
def recolectar_tendencias():
    tendencias = []
    keywords = generar_keywords()

    for palabra in keywords:
        productos_amazon = buscar_amazon(palabra)
        productos_ebay = buscar_ebay(palabra)
        productos_ml = buscar_mercado_libre(palabra)

        tendencias.append({
            "nombre_categoria": palabra,
            "productos": productos_amazon + productos_ebay + productos_ml
        })

    guardar_resultados(tendencias)

# Guardar los resultados en JSON
def guardar_resultados(tendencias):
    if not os.path.exists('data'):
        os.makedirs('data')

    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    resultados = {
        "fecha": fecha_actual,
        "tendencias": tendencias
    }

    with open('data/ai_trends.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("✅ Tendencias guardadas exitosamente.")

# Ejecutar
if __name__ == "__main__":
    recolectar_tendencias()
