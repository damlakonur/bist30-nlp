import sys
import re

try:
    nltk.download("stopwords")
except:
    print("Stopwords can't be downloaded.")
    sys.exit()

from nltk.corpus import stopwords

def preprocess_tweets(tweets: "list") -> "list":
    """
    Preprocesses tweets
    :param tweets: List of tweets
    :return: Lists of preprocessed tweets
    """

    preprocessed_tweets = []
    stop_words = set(stopwords.words("turkish"))
    regex_stop_words = re.compile(r"\b(" + "|".join(stop_words) + r")\W", re.I)

    for tweet in tweets:
        tweet = regex_stop_words.sub("", tweet)

        # Punctuations may represent special meanings.
        tweet = re.sub(r"[.|:|,|;|!|?|(|)|{|}|\[|\]|\\|/|~|@|*|=|+|\-|_|]", r" ", tweet)

        # Numbers more that four digits are removed.
        tweet = re.sub(r"\d{4,}", " ", tweet)

        tweet = tweet.replace("\n", " ")
        tweet = tweet.strip()
        preprocessed_tweet = ""

        for word in tweet.split():

            # Lonely chars are removed.
            alpha_word = re.sub(r"\b[a-z]\b", "", word)
            preprocessed_tweet += alpha_word
            preprocessed_tweet += " "

        preprocessed_tweet = preprocessed_tweet.strip()
        preprocessed_tweets.append(preprocessed_tweet)

    return preprocessed_tweets
