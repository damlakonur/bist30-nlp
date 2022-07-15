import snscrape.modules.twitter as twitter
import pandas as pd
from tqdm import tqdm


query = (
    "(#BIST30 OR #XU030 OR #AKBNK OR #ARCLK OR #ASELS OR #BIMAS OR"
    " #EKGYO OR #EREGL OR #FROTO OR #GUBRF OR #SAHOL OR #HEKTS OR #KRDMD OR"
    " #KCHOL OR #KOZAL OR #KOZAA OR #PGSUS OR #SASA OR #PETKM OR #TAVHL OR"
    " #TKFEN OR #TOASO OR #TCELL OR #TUPRS OR #THYAO OR #TTKOM OR #GARAN OR"
    " #HALKB OR #ISCTR OR #SISE OR #VESTL OR #YKBNK) lang:tr until:2022-07-12"
    " since:2021-01-01 -filter:links -filter:replies"
)


query = (
    "(#BIST30 OR #XU030 OR #AKBNK OR #ARCLK OR #ASELS OR #BIMAS OR"
    " #EKGYO OR #EREGL OR #FROTO OR #GUBRF OR #SAHOL OR #HEKTS OR #KRDMD OR"
    " #KCHOL OR #KOZAL OR #KOZAA OR #PGSUS OR #SASA OR #PETKM OR #TAVHL OR"
    " #TKFEN OR #TOASO OR #TCELL OR #TUPRS OR #THYAO OR #TTKOM OR #GARAN OR"
    " #HALKB OR #ISCTR OR #SISE OR #VESTL OR #YKBNK) until:2021-01-01"
    " since:2019-01-01 -filter:replies"
)
tweets = []
limit = 1000000

for tweet in tqdm(twitter.TwitterSearchScraper(query).get_items()):
    if len(tweets) < limit:
        tweets.append(
            [
                tweet.date,
                tweet.user.username,
                tweet.content,
                tweet.retweetCount,
                tweet.likeCount,
                tweet.user.followersCount,
                tweet.user.verified,
            ]
        )
    else:
        break

df = pd.DataFrame(
    tweets, columns=["date", "user", "tweet", "rt", "fav", "followers", "verified"]
)

# csv
# df.to_csv('s.csv', index=False)
# print(df.head(5))
