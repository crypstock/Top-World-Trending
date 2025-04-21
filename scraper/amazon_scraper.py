import pandas as pd
import datetime
from .amazon_api_client import AmazonAPIClient

def scrape_amazon(search_term, country='US', max_pages=1):
    client = AmazonAPIClient()
    response = client.search_products(search_term)

    products = []
    if 'ItemsResult' in response and 'Items' in response['ItemsResult']:
        for item in response['ItemsResult']['Items']:
            try:
                title = item['ItemInfo']['Title']['DisplayValue']
                price = item['Offers']['Listings'][0]['Price']['DisplayAmount'] if 'Offers' in item else "N/A"
                link = item['DetailPageURL']
                image = item['Images']['Primary']['Medium']['URL'] if 'Images' in item else "N/A"

                products.append({
                    "Title": title,
                    "Price": price,
                    "Link": link,
                    "Image": image,
                    "Date": str(datetime.date.today())
                })
            except Exception as e:
                continue

    df = pd.DataFrame(products)
    file_path = f"data/amazon_{search_term}_{country}_{datetime.date.today()}.csv"
    df.to_csv(file_path, index=False)
    
    # Save to MongoDB
    from database.mongo_handler import MongoDBHandler
    mongo = MongoDBHandler()
    if mongo.connect():
        mongo.save_products(products, "amazon_products")
        mongo.close()
        print("✅ Products saved to MongoDB!")
    
    return df