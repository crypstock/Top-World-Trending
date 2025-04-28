from zipfile import ZipFile
import os
import shutil
from datetime import datetime

def setup_project_structure():
    # Define base directories
    base_dirs = [
        'scraper',
        'ai',
        'data',
        'utils',
        'database',
        'backup'
    ]
    
    # Create base directories
    for dir_name in base_dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    # Define scraper files to back up
    scraper_files = [
        'amazon_scraper.py',
        'ebay_scraper.py',
        'mercado_libre_scraper.py'
    ]
    
    # Backup existing scraper files
    for file_name in scraper_files:
        src_path = os.path.join('scraper', file_name)
        backup_dir = 'backup'
        if os.path.exists(src_path):
            # Add timestamp to backup file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dest_path = os.path.join(backup_dir, f"{file_name}.{timestamp}.bak")
            shutil.copy(src_path, dest_path)
            print(f"✅ Backed up {file_name} to {dest_path}")
        else:
            print(f"⚠️ File {src_path} does not exist. Skipping backup.")

    print("✅ Project structure has been set up successfully!")

def archive_project():
    # Archive the project structure into a zip file
    archive_name = f"project_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    with ZipFile(archive_name, 'w') as archive:
        for folder_name, subfolders, filenames in os.walk('.'):
            for filename in filenames:
                # Avoid archiving the archive itself
                if not filename.endswith('.zip'):
                    file_path = os.path.join(folder_name, filename)
                    archive.write(file_path, os.path.relpath(file_path, '.'))
    print(f"✅ Project archived successfully as {archive_name}")

if __name__ == "__main__":
    setup_project_structure()
    archive_project()
