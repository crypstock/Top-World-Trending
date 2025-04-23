"""
auto_trend_collector.py
Recolector automático de productos en tendencia (Amazon + eBay + Mercado Libre) con IA GPT-4o
────────────────────────────────────────────────────────────────────────
• Genera dinámicamente las palabras clave con GPT-4o
• Extrae productos reales de los 3 marketplaces
• Calcula un MVP_SCORE (precio × factor plataforma) para priorizar oportunidades
• Agrupa el top-10 por keyword y lo guarda en /data/tendencias_YYYY-MM-DD.json
• Diseñado para ejecutarse por cron (@daily) o manual
"""

import os, json, datetime, requests
from collections import defaultdict
from dotenv import load_dotenv
import openai

# ─── Módulos de scraping ───
from modules.mercado_libre import buscar_mercado_libre
from modules.ebay_search      import buscar_ebay
from modules.amazon_search    import buscar_amazon   # ⬅️ nuevo

load_dotenv()

# ─── Credenciales ───
openai.api_key = os.getenv("OPENAI_API_KEY")
EBAY_APP_ID    = os.getenv("EBAY_APP_ID")

# ──────────────────────────────────────────────────────────
# 1. Generar keywords con GPT-4o
# ──────────────────────────────────────────────────────────
def generar_keywords(max_palabras=8):
    prompt = (
        "You are a product-research expert. "
        "Give me a concise comma-separated list (no numbers) of the highest-potential "
        "product niches right now for Amazon, eBay and Mercado Libre. "
        "Mix evergreen + rising trends, skip oversaturated items, prefer ASP>$20. "
        f"Limit to {max_palabras} keywords."
    )
    rsp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return [kw.strip().lower() for kw in rsp.choices[0].message.content.split(",") if kw.strip()]

# ──────────────────────────────────────────────────────────
# 2. Recolectar productos reales
# ──────────────────────────────────────────────────────────
def recolectar_productos(keywords):
    resultados = []
    for kw in keywords:
        # Mercado Libre MX
        resultados += [dict(**p, plataforma="mercadolibre", keyword=kw)
                       for p in buscar_mercado_libre("MLM", kw, 20)]

        # eBay US
        resultados += [dict(**p, plataforma="ebay", keyword=kw)
                       for p in buscar_ebay(kw, EBAY_APP_ID)]

        # Amazon (USA o MX según AMAZON_COUNTRY de tus variables)
        resultados += [dict(**p, plataforma="amazon", keyword=kw)
                       for p in buscar_amazon(kw, 20)]
    return resultados

# ──────────────────────────────────────────────────────────
# 3. Métrica simple MVP_SCORE
# ──────────────────────────────────────────────────────────
def mvp_score(p):
    try:
        price = float(str(p.get("precio")).replace("$", "").replace(",", ""))
    except:
        price = 0.0
    factor = 1.15 if p["plataforma"] == "mercadolibre" else 1.0
    return price * factor

# ──────────────────────────────────────────────────────────
# 4. Guardar resultados agrupados
# ──────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────
# 5. Punto de entrada
# ──────────────────────────────────────────────────────────
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
