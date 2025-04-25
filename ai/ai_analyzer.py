
import json
from collections import Counter, defaultdict
import datetime
import os

def analizar_productos(productos):
    categorias = defaultdict(list)

    for producto in productos:
        categoria = producto.get("categoria", "otros")
        titulo = producto.get("titulo")
        categorias[categoria].append(titulo)

    tendencias = {}
    for cat, titulos in categorias.items():
        conteo = Counter(titulos).most_common(10)
        tendencias[cat] = [{"producto": t[0], "veces": t[1]} for t in conteo]

    return tendencias

def guardar_tendencias(tendencias):
    if not os.path.exists("data"):
        os.makedirs("data")
    
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"data/tendencias_{fecha}.json"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(tendencias, f, indent=4, ensure_ascii=False)
    print(f"Tendencias guardadas en: {nombre_archivo}")

if __name__ == "__main__":
    ejemplo = [
        {"titulo": "iPhone 14", "categoria": "Electrónica"},
        {"titulo": "iPhone 14", "categoria": "Electrónica"},
        {"titulo": "PlayStation 5", "categoria": "Videojuegos"},
        {"titulo": "Echo Dot", "categoria": "Hogar"},
        {"titulo": "iPhone 14", "categoria": "Electrónica"},
        {"titulo": "Nintendo Switch", "categoria": "Videojuegos"},
    ]
    tendencias = analizar_productos(ejemplo)
    guardar_tendencias(tendencias)
