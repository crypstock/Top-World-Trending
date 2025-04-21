
import requests

def buscar_mercado_libre(pais, keyword, limit=10):
    base_url = f"https://api.mercadolibre.com/sites/{pais}/search"
    params = {
        'q': keyword,
        'limit': limit
    }
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            results.append({
                'titulo': item['title'],
                'precio': item['price'],
                'imagen': item['thumbnail'],
                'url': item['permalink']
            })
        return results
    except Exception as e:
        print(f"Error buscando en Mercado Libre: {e}")
        return []
