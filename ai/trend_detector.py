
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime, timedelta

class TrendDetector:
    def detect_trends(self, product_data):
        df = pd.DataFrame(product_data)
        
        # Calculate price trends
        df['Price'] = pd.to_numeric(df['Price'].str.replace('$', '').str.replace(',', ''), errors='coerce')
        price_trend = df.groupby('Date')['Price'].agg(['mean', 'count']).reset_index()
        
        # Calculate popular keywords
        vectorizer = CountVectorizer(stop_words='english')
        title_matrix = vectorizer.fit_transform(df['Title'].astype(str))
        keywords = pd.DataFrame({
            'keyword': vectorizer.get_feature_names_out(),
            'frequency': title_matrix.sum(axis=0).A1
        })
        top_keywords = keywords.nlargest(10, 'frequency')
        
        # Get top rated products
        if 'Rating' in df.columns:
            df_sorted = df.sort_values(by='Rating', ascending=False).head(10)
            print("🔍 Top 10 Productos con mejor puntuación:")
            print(df_sorted[['Title', 'Price', 'Rating']])
            
            # Save top products to a separate file
            output_file = f"data/top10_products_{datetime.date.today()}.csv"
            df_sorted.to_csv(output_file, index=False)
        
        return {
            'price_trends': price_trend.to_dict('records'),
            'popular_keywords': top_keywords.to_dict('records'),
            'top_rated': df_sorted.to_dict('records') if 'Rating' in df.columns else None
        }

    @staticmethod
    def analyze_file(file_path):
        df = pd.read_csv(file_path)
        df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float, errors='ignore')
        df_sorted = df.sort_values(by='Rating', ascending=False).head(10)
        
        print("🔍 Top 10 Productos con mejor puntuación:")
        print(df_sorted[['Title', 'Price', 'Rating']])
        
        df_sorted.to_csv(file_path.replace(".csv", "_top10.csv"), index=False)
        return df_sorted
