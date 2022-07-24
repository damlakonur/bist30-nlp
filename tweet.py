import snscrape.modules.twitter as twitter
import pandas as pd
from tqdm import tqdm
import os

stocks = [
    "BIST30",
    "XU030",
    "AKBNK",
    "ARCLK",
    "ASELS",
    "BIMAS",
    "EKGYO",
    "EREGL",
    "FROTO",
    "GUBRF",
    "SAHOL",
    "HEKTS",
    "KRDMD",
    "KCHOL",
    "KOZAL",
    "KOZAA",
    "PGSUS",
    "SASA",
    "PETKM",
    "TAVHL",
    "TKFEN",
    "TOASO",
    "TCELL",
    "TUPRS",
    "THYAO",
    "TTKOM",
    "GARAN",
    "HALKB",
    "ISCTR",
    "SISE",
    "VESTL",
    "YKBNK",
]

for stock in stocks:
    query = f"{stock}(#{stock} OR #${stock}) lang:tr -filter:links -filter:replies"
    tweets = []
    limit = 10000

    for tweet in tqdm(twitter.TwitterSearchScraper(query).get_items()):
        if tweet.media == None and len(tweets) < limit:
            tweets.append(
                [
                    tweet.date,
                    tweet.user.username,
                    tweet.content,
                    tweet.retweetCount,
                    tweet.likeCount,
                    tweet.user.followersCount,
                    tweet.user.verified,
                    tweet.hashtags,
                    tweet.cashtags,
                ]
            )
        else:
            break

    df = pd.DataFrame(
        tweets,
        columns=[
            "date",
            "user",
            "tweet",
            "rt",
            "fav",
            "followers",
            "verified",
            "hashtags",
            "cashtags",
        ],
    )

    # csv
    df.to_csv(f"./data/stock_tweets/{stock}.csv", index=False)

os.chdir(r".\data\stock_tweets")
all_csv_files = os.listdir()

all_df = pd.DataFrame()
for file in all_csv_files:
    temp_df = pd.read_csv(file)
    all_df = pd.concat([all_df, temp_df], axis=0)

df.to_csv("all_stock.csv")

sampled_df = all_df.sample(frac=0.01, random_state=1)

df.to_csv("sampled_stocks.csv")
