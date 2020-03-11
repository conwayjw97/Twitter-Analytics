# https://www.w3schools.com/python/python_mongodb_getstarted.asp
# https://stackabuse.com/accessing-the-twitter-api-with-python/?fbclid=IwAR3PnBWLlu3o5yCXPLUoO6IyNCxza6HEXkYuOH_65iyYpMcNtpDoVqLoh5o
# https://tweepy.readthedocs.io/en/latest/api.html#API.search
# https://gist.github.com/jaymcgrath/367c521f1dd786bc5a05ec3eeeb1cb04

import pymongo
import tweepy
import time
import sys
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation

def parse_tweet(tweet):
    if hasattr(tweet, "retweeted_status"):  # Check if Retweet
        try:
            text = tweet.retweeted_status.extended_tweet["full_text"]
        except AttributeError:
            text = tweet.retweeted_status.text
    else:
        try:
            text = tweet.extended_tweet["full_text"]
        except AttributeError:
            text = tweet.text
    return text

class RestCrawler():
    def __init__(self, auth, power_users, scrape_max):
        self.auth = auth
        self.power_users = power_users
        self.scrape_max = scrape_max

    def scrape(self):
        api = tweepy.API(auth, wait_on_rate_limit=True)
        rest_tweets = []
        tweet_count = 0
        try:
            print("Scraping with the REST API...")
            for tweet in api.search(q=self.keyword, lang="en", result_type="recent", count=self.scrape_max, full_text=True, tweet_mode="extended"):
                # Try to get the extended tweet if it's long enough
                tweet_text = parse_tweet(tweet)
                # print("Tweet by %s at %s in %s: %s" % (tweet.user.screen_name, tweet.created_at, tweet.geo, tweet.text))
                rest_tweets.append({"id":tweet.id,"data":{"time":tweet.created_at,"user":tweet.user.screen_name,"text":tweet_text}})
                # rest_tweets.append((tweet.created_at,tweet.id,tweet.text))
                tweet_count += 1
        except BaseException as e:
            print("Failed, on_status:", str(e))
        print ("Number of tweets scraped through REST:", tweet_count, "\n")
        return rest_tweets

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit):
        self.api = tweepy.API()
        self.tweet_count = 0
        self.tweets = []
        self.time_limit = time_limit
        self.start_time = time.time()

    def on_status(self, status):
        if (time.time() - self.start_time) < self.time_limit:
            # Try to get the extended tweet if it's long enough
            tweet_text = parse_tweet(status)
            # print("Tweet by %s at %s in %s: %s" % (status.user.screen_name, status.created_at, status.geo, tweet_text))
            self.tweets.append({"id":status.id,"data":{"time":status.created_at,"user":status.user.screen_name,"text":tweet_text}})
            # self.tweets.append((status.created_at, status.id, tweet_text))
            self.tweet_count += 1
            return True
        else:
            return False

    def get_tweets(self):
        return self.tweets

class StreamCrawler():
    def __init__(self, auth, keyword, time_limit):
        self.auth = auth
        self.keyword = keyword
        self.time_limit = time_limit

    def scrape(self):
        listener = MyStreamListener(self.time_limit)
        stream = tweepy.Stream(self.auth, listener)
        try:
            print("Scraping with the Streaming API... \nPress Ctrl+C in order to stop streaming or wait for the", self.time_limit, "second time limit")
            # stream.filter(track=[self.keyword], languages=["en"])
            stream.sample(languages=["en"])
        except KeyboardInterrupt:
            pass
        except BaseException as e:
            print("Failed, on_status:", str(e))
        print("Number of tweets fetched through streaming:", listener.tweet_count, "\n")
        return listener.get_tweets()

def find_power_users(tweets):
    power_users = {}
    for tweet in tweets:
        tweet = tweet["data"]
        if(tweet["user"] in power_users):
            power_users[tweet["user"]] += 1
        else:
            power_users[tweet["user"]] = 1

    sorted_power_users = sorted(power_users, key=power_users.get, reverse=True)
    print("\n5 users with the most tweets:")
    for i in range(5):
        print("%s with %d tweets." % (sorted_power_users[i], power_users[sorted_power_users[i]]))

    return(sorted_power_users)

def clean_up_tweets(tweets):
    print("Cleaning up tweets.")
    tweets_to_remove = []
    for i in range(len(tweets)):
        tweet = tweets[i]["data"]
        # Remove URLs
        tweet["text"] = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet["text"], flags=re.MULTILINE)
        # Remove very short tweets
        if(len(tweet["text"]) < 10):
            tweets_to_remove.append(tweets[i])
    for tweet in tweets_to_remove:
        tweets.remove(tweet)
    return tweets

def print_tweets(tweets):
    for tweet in tweets:
        tweet = tweet["data"]
        print("Tweet by %s at %s: %s" % (tweet["user"], tweet["time"], tweet["text"]))

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        # print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        indexing = topic.argsort()[:-no_top_words - 1:-1]
        print(indexing)
        print(feature_names)
        print(feature_names[indexing[0]])
        print(feature_names[indexing[1]])
        print(feature_names[indexing[2]])

def find_topics(tweets):
    print("Extracting topics.")

    tweet_text = []
    for tweet in tweets:
        tweet_text.append(tweet["data"]["text"])

    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000, stop_words='english')
    tf = tf_vectorizer.fit_transform(tweet_text)
    tf_feature_names = tf_vectorizer.get_feature_names()

    no_topics = 20

    # Run LDA
    lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

    no_top_words = 5
    display_topics(lda, tf_feature_names, no_top_words)

if(len(sys.argv) - 1 < 2):
    print("Please run this program with arguments: Crawler.py <REST_Tweets> <Stream_Time>")
else:
    # Scraping parameters
    KEYWORD = "Coronavirus"
    REST_TWEET_MAX = int(sys.argv[1])
    STREAM_TIME_LIMIT = int(sys.argv[2])

    # Set keys and configure Twitter app authorisation
    consumer_key = "8CRA9cjpku4BtfK1vuJ5QAPLg"
    consumer_secret = "uAGmC5CpJY5vjTom2l8AhXAtKeu3aFCm69Atxl19YXlUIvwN0F"
    access_token = "1072253339113611266-3Th0tGTF5hlAluASFHW9QmlCowQgsa"
    access_token_secret = "P9G1QCQfgFDV55P2coN6tR2L19DbRolhm65SpVDY6C1Kr"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Scrape with Streaming
    stream_crawler = StreamCrawler(auth, KEYWORD, STREAM_TIME_LIMIT)
    stream_tweets = stream_crawler.scrape()
    stream_tweets = clean_up_tweets(stream_tweets)
    find_topics(stream_tweets)


    # power_users = find_power_users(stream_tweets)
    #
    # # Scrape with the REST API
    # rest_crawler = RestCrawler(auth, power_users, KEYWORD, REST_TWEET_MAX)
    # rest_tweets = rest_crawler.scrape()
    # print(rest_tweets)
    #
    # # Save tweets to MongoDB
    # print("Saving scraped tweets to MongoDB...\n")
    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    # db = client["WebScienceAssessment"]
    #
    # collection = db["tweets"]
    # for tweet in rest_tweets:
    #     collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)
    # for tweet in stream_tweets:
    #     collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)
    #
    # print("Done.")
    # print("Total number of tweets stored:", collection.count())
