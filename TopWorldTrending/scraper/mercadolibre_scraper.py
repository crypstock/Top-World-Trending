
import requests
import pandas as pd
import datetime

def buscar_mercado_libre(pais='MLM', query='laptop', limite=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    base_url = f"https://api.mercadolibre.com/sites/{pais}/search"
    params = {
        'q': query,
        'limit': limite
    }
    
    try:
        respuesta = requests.get(base_url, params=params, headers=headers)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            productos = datos['results']
            resultados = []
            for producto in productos:
                resultados.append({
                    'Title': producto['title'],
                    'Price': producto['price'],
                    'Link': producto['permalink'],
                    'Image': producto['thumbnail'],
                    'Date': str(datetime.date.today())
                })
            df = pd.DataFrame(resultados)
            if not df.empty:
                file_path = f"data/mercadolibre_{query}_{pais}_{datetime.date.today()}.csv"
                df.to_csv(file_path, index=False)
            return df
        else:
            print(f"Error en la búsqueda: {respuesta.status_code}")
            print(f"Mensaje: {respuesta.text}")
            return pd.DataFrame({'Title': [], 'Price': [], 'Link': [], 'Image': [], 'Date': []})
    except Exception as e:
        print(f"Error al realizar la búsqueda: {str(e)}")
        return pd.DataFrame({'Title': [], 'Price': [], 'Link': [], 'Image': [], 'Date': []})

class MercadoLibreScraper:
    def __init__(self, region="MLM"):
        self.region = region
        
    def scrape_products(self, query, limit=10):
        return buscar_mercado_libre(self.region, query, limit)
