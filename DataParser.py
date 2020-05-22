from datetime import datetime
import time
import datetime as dt
import requests
import pandas as pd

NYT_KEY = "ImIRmI2w1NAioVsDxLkaxiQKXSDXG2Ev" # NYT Key
NYT_ARTICLE_ENDPOINT = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

def timemod(x, time):
    delta = dt.timedelta(hours = time)
    return x + delta


def retrieve(word, date):

    data = []

    for l in date:
        curr = datetime.utcfromtimestamp(l.tolist()/1e9)
        print(l)
        query = {"q":word, "begin_date": curr.strftime("%Y%m%d"), \
        "end_date": curr.strftime("%Y%m%d"), "api-key":NYT_KEY, "facet":False, \
        "page": 0, "sort":"oldest", "fq":"headline:(\""+word+"\") OR body:(\""+word+"\")"}
        try:
            ret = requests.get(NYT_ARTICLE_ENDPOINT, params=query)
            data += [{"title": i["abstract"], "pub_date": i["pub_date"]} for i in \
            ret.json()["response"]["docs"]]
            time.sleep(6) #Rate limit of NYT
        except:
            break
    df = pd.DataFrame(data=data)
    df.to_csv("Formatted-Data/"+word+"-articles.csv", index=False)





symbol = input("Enter Symbol: ")
name = input("Enter company name: ")
df = pd.read_csv("Stock-Data/"+symbol+".csv")
df["Date"] = pd.to_datetime(df["Date"])
open = df[["Date","Open"]].copy()
close = df[["Date","Close"]].copy();

open["Date"] = open["Date"].map(lambda x: timemod(x,9.5))
close["Date"] = close["Date"].map(lambda x: timemod(x,16))
open = open.rename(columns={"Open":"Price"})
close = close.rename(columns={"Close":"Price"})
out = pd.concat([open, close]).sort_values(by=["Date"])
out.to_csv("Formatted-Data/Parsed-"+symbol+".csv", index=False)
print("Stock Data Parsed and Saved")
retrieve(name, list(df[df["Date"] > datetime.utcfromtimestamp(1620000000)]["Date"].unique()))
