import snscrape.modules.twitter as twitter
import pandas as pd
from tqdm import tqdm

stocks = ["BIST30", "XU030", "AKBNK", "ARCLK", "ASELS", "BIMAS",
                          "EKGYO", "EREGL", "FROTO", "GUBRF", "SAHOL", "HEKTS",
                          "KRDMD", "KCHOL", "KOZAL", "KOZAA", "PGSUS", "SASA",
                          "PETKM", "TAVHL", "TKFEN", "TOASO", "TCELL", "TUPRS",
                          "THYAO","TTKOM", "GARAN", "HALKB", "ISCTR", "SISE",
                          "VESTL", "YKBNK"]
for stock in stocks:
    query = (f"{stock}(#{stock} OR #${stock}) lang:tr")
    tweets = []
    limit = 1000
    for tweet in tqdm(twitter.TwitterSearchScraper(query).get_items()):
        if(len(tweets) < limit):
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
                    tweet.retweetedTweet,
                    tweet.quotedTweet,
                    tweet.media
                ]
            )
        else:
            break

    df = pd.DataFrame(
        tweets, columns=["date", "user", "tweet", "rt", "fav", "followers", "verified",
                         "hashtags", "cashtags", "retweetedTweet", "quotedTweet", "media"]
    )

    # csv
    df.to_csv(f'./data/stock_tweets/{stock}.csv', index=False)
