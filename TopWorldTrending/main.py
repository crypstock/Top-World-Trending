
from scraper.amazon_scraper import scrape_amazon
from scraper.ebay_scraper import EbayScraper
from scraper.mercadolibre_scraper import MercadoLibreScraper
from ai.review_analyzer import analyze_reviews
from ai.trend_detector import TrendDetector
from ai.ai_analyzer import analizar_productos, guardar_tendencias
from utils import logger
import os

def main():
    logger.setup_logging()
    
    if not os.path.exists("data"):
        os.makedirs("data")

    print("\n🚀 Bienvenido a TopWorldTrending – Buscador de Productos en Tendencia!\n")
    print("Selecciona una plataforma para buscar productos:")
    print("1. Amazon\n2. eBay\n3. Mercado Libre")
    choice = input("Elige una opción (1/2/3): ")

    search = input("\n🔍 ¿Qué producto deseas buscar?: ")
    
    trend_detector = TrendDetector()

    if choice == '1':
        df = scrape_amazon(search, country="US")
        file_path = f"data/amazon_{search}_US_{df['Date'].iloc[0]}.csv"
        analyze_reviews(file_path)
        trend_detector.analyze_file(file_path)
    elif choice == '2':
        scraper = EbayScraper(region="US")
        df = scraper.scrape_products(search)
        file_path = f"data/ebay_{search}_US_{df['Date'].iloc[0]}.csv"
        analyze_reviews(file_path)
        trend_detector.analyze_file(file_path)
    elif choice == '3':
        scraper = MercadoLibreScraper()
        df = scraper.scrape_products(search)
        if not df.empty:
            file_path = f"data/mercadolibre_{search}_MX_{df['Date'].iloc[0]}.csv"
            analyze_reviews(file_path)
            trend_detector.analyze_file(file_path)
        else:
            print("No se encontraron resultados.")
    else:
        print("Opción inválida. Por favor intenta de nuevo.")

if __name__ == "__main__":
    main()
