import requests

def buscar_mercado_libre(query, pais='MLM'):
    url = f"https://api.mercadolibre.com/sites/{pais}/search?q={query}&limit=5"
    try:
        response = requests.get(url)
        productos = response.json().get('results', [])
        resultados = []
        for prod in productos:
            resultados.append({
                'titulo': prod['title'],
                'precio': prod['price'],
                'link': prod['permalink'],
                'imagen': prod['thumbnail']
            })
        return resultados
    except:
        return []
