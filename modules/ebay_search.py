import os
import requests

EBAY_APP_ID = os.getenv("EBAY_APP_ID")

def buscar_ebay(query):
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={query}&limit=5"
    headers = {
        "Authorization": f"Bearer {EBAY_APP_ID}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        items = response.json().get('itemSummaries', [])
        resultados = []
        for item in items:
            resultados.append({
                'titulo': item.get('title', 'Producto eBay'),
                'precio': item.get('price', {}).get('value', '0'),
                'link': item.get('itemWebUrl', '#'),
                'imagen': item.get('image', {}).get('imageUrl', '')
            })
        return resultados
    except:
        return []
