import os
import requests

ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
ASSOCIATE_TAG = os.getenv("AMAZON_ASSOC_TAG")

def buscar_amazon(query, region="us"):
    # Aquí simulamos una respuesta ya que la PA-API real requiere firma compleja
    # Puedes integrar Amazon API oficial si deseas más realismo
    resultados = [
        {
            'titulo': f'{query} - Producto Amazon Simulado',
            'precio': '29.99',
            'link': f'https://www.amazon.com/s?k={query}',
            'imagen': 'https://via.placeholder.com/150'
        }
    ]
    return resultados
