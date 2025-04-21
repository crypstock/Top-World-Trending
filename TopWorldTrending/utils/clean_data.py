
import pandas as pd
import re

def clean_product_data(raw_data):
    df = pd.DataFrame(raw_data)
    
    # Clean price data
    if 'Price' in df.columns:
        df['Price'] = df['Price'].replace('N/A', np.nan)
        df['Price'] = df['Price'].str.extract(r'(\d+\.?\d*)').astype(float)
    
    # Clean text data
    if 'Title' in df.columns:
        df['Title'] = df['Title'].str.strip()
        df['Title'] = df['Title'].str.replace(r'\s+', ' ')
    
    return df

def format_for_analysis(data):
    df = pd.DataFrame(data)
    
    # Format dates
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Ensure consistent column types
    if 'Rating' in df.columns:
        df['Rating'] = pd.to_numeric(df['Rating'].str.extract(r'([\d.]+)')[0], errors='coerce')
    
    return df
