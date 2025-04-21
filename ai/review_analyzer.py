
import pandas as pd
from textblob import TextBlob

def analyze_reviews(csv_file):
    df = pd.read_csv(csv_file)
    
    def extract_sentiment(text):
        return TextBlob(text).sentiment.polarity

    if "Review" in df.columns:
        df["Sentiment"] = df["Review"].astype(str).apply(extract_sentiment)
        df["Feedback"] = df["Sentiment"].apply(lambda x: "Negative" if x < -0.1 else ("Positive" if x > 0.1 else "Neutral"))
        df.to_csv(csv_file.replace(".csv", "_analyzed.csv"), index=False)
        return df
    else:
        print("No review data found.")
        return None
