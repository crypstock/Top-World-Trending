# modules/amazon_search.py – Amazon Product Advertising API
from amazon_paapi import AmazonApi
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
ASSOCIATE_TAG = os.getenv("AMAZON_ASSOCIATE_TAG")
COUNTRY = os.getenv("AMAZON_COUNTRY", "us")  # "us", "mx", etc.

if not all([ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG]):
    raise RuntimeError("⚠️ Falta configurar claves Amazon en tus variables de entorno.")

amazon = AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, COUNTRY)

def buscar_amazon(keyword, max_items=10):
    resultados = []
    try:
        resp = amazon.search_items(keywords=keyword, search_index="All", item_count=max_items)
        for item in resp.items:
            resultados.append({
                "titulo": item.title,
                "precio": item.price,
                "url": item.detail_page_url,
                "plataforma": "amazon"
            })
    except Exception as e:
        print("Error en Amazon:", e)
    return resultados
