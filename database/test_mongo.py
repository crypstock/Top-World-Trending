
from mongo_handler import MongoDBHandler
import os

def test_connection():
    # Create handler instance
    mongo = MongoDBHandler()
    
    # Test connection
    if mongo.connect():
        # Test product insertion
        test_product = {
            "nombre": "Camiseta Nike",
            "precio": 29.99,
            "plataforma": "Amazon",
            "pais": "Estados Unidos"
        }
        
        products = [test_product]
        inserted = mongo.save_products(products, "products")
        
        if inserted > 0:
            print("✅ Test product saved successfully!")
            
            # Verify product in database
            collection = mongo.db["products"]
            saved_products = list(collection.find({"nombre": "Camiseta Nike"}))
            print("\nRetrieved products:")
            for prod in saved_products:
                print(f"- {prod['nombre']}: ${prod['precio']}")
        
        mongo.close()
    else:
        print("❌ Connection test failed")

if __name__ == "__main__":
    test_connection()
