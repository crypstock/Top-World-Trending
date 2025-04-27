
from zipfile import ZipFile
import os
import shutil

def setup_project_structure():
    # Define base directories
    base_dirs = [
        'scraper',
        'ai',
        'data',
        'utils'
    ]
    
    # Create base directories
    for dir_name in base_dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    # Clean and copy files to the correct locations
    shutil.copy('scraper/amazon_scraper.py', 'scraper/amazon_scraper.py.bak')
    shutil.copy('scraper/ebay_scraper.py', 'scraper/ebay_scraper.py.bak')
    shutil.copy('scraper/mercadolibre_scraper.py', 'scraper/mercadolibre_scraper.py.bak')
    
    print("✅ Project structure has been set up successfully!")

if __name__ == "__main__":
    setup_project_structure()
