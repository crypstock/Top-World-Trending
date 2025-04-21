# modules/ebay_search.py
import requests
import os

def buscar_ebay(query, app_id):
    url = "https://svcs.ebay.com/services/search/FindingService/v1"
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": app_id,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": query
    }

    response = requests.get(url, params=params)
    resultados = []

    if response.status_code == 200:
        data = response.json()
        for item in data['findItemsByKeywordsResponse'][0]['searchResult'][0].get('item', []):
            resultados.append({
                "titulo": item['title'][0],
                "precio": item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                "url": item['viewItemURL'][0]
            })
    return resultados