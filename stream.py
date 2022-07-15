from config import *
import tweepy
import datetime
from tweepy import OAuthHandler
import sys
import pandas as pd

# Function for Twitter API authorization
def getAuth():
    try:
        auth = OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        if api.verify_credentials():
            print("Authentication OK")
        else:
            print("Error during authentication")
    except tweepy.TweepyException as e:
        print("Error : " + str(e))
        sys.exit()
    return api

# Function for scraping tweets containing specific hashtags
def getTweetsFromHashtag(api, query, since = None, until = None, lang = 'tr'):
    """
    Get tweets from a specific hashtag
    :param api: Twitter API
    :param query: Hashtag
    :param since: Start date
    :param until: End date
    :param lang: Language
    :return: Dataframe that contains specific tweets
    """
    df = pd.DataFrame(columns = ['id', 'created_at',
                                 'username', 'favorite_count',
                                 'retweet_count', 'followers_count',
                                 'text', 'lang', 'hashtags', 'location'])
    try:
        tweets = tweepy.Cursor(api.search_full_archive, label='dev',query=query,
                            fromDate=since, toDate=until).items()
        for tweet in tweets:
            df = df.append(pd.Series([tweet.id_str, tweet.created_at,
                                    tweet.user.screen_name,
                                    tweet.favorite_count,
                                    tweet.retweet_count,
                                    tweet.user.followers_count,
                                    tweet.text,
                                    tweet.lang,
                                    tweet.entities['hashtags'],
                                    tweet.user.location],
                                    index=df.columns),
                                    ignore_index=True)
            df.to_csv('tweets.csv', index=False)
    except tweepy.TweepyException as e:
        print("Error : " + str(e))
        sys.exit()
    return df

# Function for scraping tweets from a specific user
def getTweetsFromUser(api, user, since = None, until = None, lang = 'tr'):
    df = pd.DataFrame(columns = ['id', 'created_at',
                                 'username', 'favorite_count',
                                 'retweet_count', 'followers_count',
                                 'text', 'hashtags', 'location'])
    try:
        tweets = tweepy.Cursor(api.user_timeline, screen_name=user,
                            since=since, until=until, lang=lang).items(20000)
        for tweet in tweets:
            df = df.append(pd.Series([tweet.id_str, tweet.created_at,
                                    tweet.user.screen_name,
                                    tweet.favorite_count,
                                    tweet.retweet_count,
                                    tweet.user.followers_count,
                                    tweet.text,
                                    tweet.entities['hashtags'],
                                    tweet.user.location],
                                    index=df.columns),
                                    ignore_index=True)
            df.to_csv('tweets.csv', index=False)
    except tweepy.TweepyException as e:
        print("Error : " + str(e))
        sys.exit()
    return df

def main():
    api = getAuth()
    hastags = """#BIST30 OR #XU030 OR #AKBNK OR #ARCLK OR #ASELS OR #BIMAS OR #EKGYO OR #EREGL OR #FROTO OR #GUBRF OR #SAHOL OR #HEKTS OR #KRDMD""" 
    # Query length limit is 128 characters for search_full_archive, 256 for search_30day
    a = """OR #KCHOL OR #KOZAL OR #KOZAA 
                OR #PGSUS OR #SASA OR #PETKM OR #TAVHL OR #TKFEN OR #TOASO 
                OR #TCELL OR #TUPRS OR #THYAO OR #TTKOM OR #GARAN OR #HALKB 
                OR #ISCTR OR #SISE OR #VESTL OR #YKBNK"""
    today = datetime.date.today()
    lastYear = today - datetime.timedelta(days=365)
    outDf = getTweetsFromHashtag(api, hastags, '202104090000', '202204090000')
    

if __name__ == '__main__':
    main()
    
