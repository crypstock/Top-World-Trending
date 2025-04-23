import os, json, datetime
from collections import defaultdict
from dotenv import load_dotenv
from openai import OpenAI

# Scrapers
from modules.mercado_libre import buscar_mercado_libre
from modules.ebay_search import buscar_ebay
from modules.amazon_search import buscar_amazon

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EBAY_APP_ID = os.getenv("EBAY_APP_ID")

def generar_keywords(max_palabras=8):
    prompt = (
        f"You are a product-research expert. "
        f"Give me a concise comma-separated list (no numbering) of {max_palabras} trending product niches "
        f"for Amazon, eBay, and Mercado Libre. Prioritize growth and profitability, avoid saturated items."
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    texto = completion.choices[0].message.content
    return [w.strip().lower() for w in texto.split(',') if w.strip()]

def recolectar_productos(keywords):
    resultados = []
    for kw in keywords:
        resultados += [dict(**p, plataforma="mercadolibre", keyword=kw)
                       for p in buscar_mercado_libre("MLM", kw, 20)]
        resultados += [dict(**p, plataforma="ebay", keyword=kw)
                       for p in buscar_ebay(kw, EBAY_APP_ID)]
        resultados += [dict(**p, plataforma="amazon", keyword=kw)
                       for p in buscar_amazon(kw, 20)]
    return resultados

def mvp_score(p):
    try:
        price = float(str(p.get("precio")).replace("$", "").replace(",", ""))
    except:
        price = 0.0
    factor = 1.15 if p["plataforma"] == "mercadolibre" else 1.0
    return price * factor

def guardar_tendencias(productos):
    fecha = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    out_path = f"data/tendencias_{fecha}.json"
    agrupados = defaultdict(list)
    for p in productos:
        agrupados[p["keyword"]].append(p)
    top_dict = {}
    for kw, lista in agrupados.items():
        lista_ordenada = sorted(lista, key=mvp_score, reverse=True)[:10]
        top_dict[kw] = lista_ordenada
    os.makedirs("data", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(top_dict, f, indent=2, ensure_ascii=False)
    print(f"✅ Tendencias guardadas en {out_path}")

if __name__ == "__main__":
    print("🤖 Generando keywords con GPT-4o…")
    kws = generar_keywords()
    print("Palabras clave:", kws)
    print("🔍 Recolectando productos…")
    productos = recolectar_productos(kws)
    print(f"🔹 Se recolectaron {len(productos)} productos.")
    print("📊 Analizando y guardando tendencias…")
    guardar_tendencias(productos)
    print("🎉 Proceso completado.")
