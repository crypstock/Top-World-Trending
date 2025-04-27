
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv

class EbayScraper:
    def __init__(self, region="US"):
        self.region = region
        self.base_url = "https://www.ebay.com" if region == "US" else "https://www.ebay.com.mx"
        
    def scrape_products(self, query, max_pages=1):
        url = f"{self.base_url}/sch/i.html?_nkw={query.replace(' ', '+')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select("li.s-item")
        products = []
        
        for item in results[:10]:
            try:
                title_tag = item.select_one("h3.s-item__title")
                link_tag = item.select_one("a.s-item__link")
                price_tag = item.select_one('.s-item__price')
                
                if title_tag and link_tag:
                    products.append({
                        "Title": title_tag.text.strip(),
                        "Price": price_tag.text.strip() if price_tag else "N/A",
                        "Link": link_tag["href"],
                        "Date": datetime.date.today()
                    })
            except Exception:
                continue
                    
        df = pd.DataFrame(products)
        file_path = f"data/ebay_{query}_{self.region}_{datetime.date.today()}.csv"
        df.to_csv(file_path, index=False)
        return df
