import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer


sid = SentimentIntensityAnalyzer()
name = input("Enter company name: ")
df = pd.read_csv("Formatted-Data/"+name+"-articles.csv")
df["Sentiment Score"] = df["title"].apply(lambda x: sid.polarity_scores(x)["compound"])
df.to_csv("Formatted-Data/"+name+"-articles.csv")
