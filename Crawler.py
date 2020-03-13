# https://www.w3schools.com/python/python_mongodb_getstarted.asp
# https://stackabuse.com/accessing-the-twitter-api-with-python/?fbclid=IwAR3PnBWLlu3o5yCXPLUoO6IyNCxza6HEXkYuOH_65iyYpMcNtpDoVqLoh5o
# https://tweepy.readthedocs.io/en/latest/api.html#API.search
# https://gist.github.com/jaymcgrath/367c521f1dd786bc5a05ec3eeeb1cb04

import pymongo
import tweepy
import time
import sys
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

class RestCrawler():
    def __init__(self, auth, scrape_max):
        self.auth = auth
        self.scrape_max = scrape_max

    def scrape(self, keyword):
        api = tweepy.API(auth, wait_on_rate_limit=True)
        rest_tweets = []
        tweet_count = 0
        try:
            print("Scraping keyword '%s' with the REST API..." % keyword)
            for tweet in api.search(q=keyword, lang="en", result_type="recent", count=self.scrape_max, full_text=True, tweet_mode="extended"):
                # Try to get the extended tweet if it's long enough
                try:
                    tweet_text = tweet.retweeted_status.full_text
                except AttributeError:  # Not a Retweet
                    tweet_text = tweet.full_text
                rest_tweets.append({"id":tweet.id,"data":{"time":tweet.created_at,"user":tweet.user.screen_name,"text":tweet_text}})
                tweet_count += 1
        except BaseException as e:
            print("Failed, on_status:", str(e))
        print ("Number of tweets scraped through REST:", tweet_count)
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
            if hasattr(status, "retweeted_status"):  # Check if Retweet
                try:
                    tweet_text = status.retweeted_status.extended_tweet["full_text"]
                except AttributeError:
                    tweet_text = status.retweeted_status.text
            else:
                try:
                    tweet_text = status.extended_tweet["full_text"]
                except AttributeError:
                    tweet_text = status.text
            self.tweets.append({"id":status.id,"data":{"time":status.created_at,"user":status.user.screen_name,"text":tweet_text}})
            self.tweet_count += 1
            return True
        else:
            return False

    def get_tweets(self):
        return self.tweets

class StreamCrawler():
    def __init__(self, auth, keywords, time_limit):
        self.auth = auth
        self.keywords = keywords
        self.time_limit = time_limit

    def scrape(self):
        listener = MyStreamListener(self.time_limit)
        stream = tweepy.Stream(self.auth, listener, tweet_mode="extended")
        try:
            print("Scraping with the Streaming API... \nPress Ctrl+C in order to stop streaming or wait for the", self.time_limit, "second time limit")
            stream.filter(track=self.keywords, languages=["en"])
        except KeyboardInterrupt:
            pass
        except BaseException as e:
            print("Failed, on_status:", str(e))
        print("Number of tweets fetched through streaming:", listener.tweet_count)
        return listener.get_tweets()

def find_power_users(tweets, no_users):
    power_users = {}
    for tweet in tweets:
        tweet = tweet["data"]
        if(tweet["user"] in power_users):
            power_users[tweet["user"]] += 1
        else:
            power_users[tweet["user"]] = 1

    sorted_power_users = sorted(power_users, key=power_users.get, reverse=True)
    print("\n%d users with the most tweets:" % no_users)
    for i in range(no_users):
        print("%s with %d tweets." % (sorted_power_users[i], power_users[sorted_power_users[i]]))

    return(sorted_power_users[:no_users])

def clean_up_tweets(tweets):
    print("Cleaning up tweets.")
    tweets_to_remove = []
    for i in range(len(tweets)):
        tweet = tweets[i]["data"]
        # Remove URLs
        tweet["text"] = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', tweet["text"], flags=re.MULTILINE)
        # Remove new lines
        tweet["text"] = re.sub(r'/\r?\n|\r/', '', tweet["text"], flags=re.MULTILINE)
        # Remove broken symbols
        tweet["text"] = re.sub(r'&amp;', '', tweet["text"], flags=re.MULTILINE)
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

def scrape_trends(auth):
    api = tweepy.API(auth)

    # WOE ID for UK is 12723
    # WOE ID for US is 2352824
    trends = api.trends_place(2352824)[0]["trends"]

    trend_keywords = []
    for trend in trends:
        trend_keywords.append(trend["name"])

    print("Trending keywords:", trend_keywords)

    return trend_keywords

if(len(sys.argv) - 1 < 3):
    print("Please run this program with arguments: Crawler.py <No_Power_Users> <Stream_Time> <Max_REST_Tweets>")
else:
    # Scraping parameters
    NO_POWER_USERS = int(sys.argv[1])
    STREAM_TIME_LIMIT = int(sys.argv[2])
    REST_TWEET_MAX = int(sys.argv[3])

    # Set keys and configure Twitter app authorisation
    consumer_key = "8CRA9cjpku4BtfK1vuJ5QAPLg"
    consumer_secret = "uAGmC5CpJY5vjTom2l8AhXAtKeu3aFCm69Atxl19YXlUIvwN0F"
    access_token = "1072253339113611266-3Th0tGTF5hlAluASFHW9QmlCowQgsa"
    access_token_secret = "P9G1QCQfgFDV55P2coN6tR2L19DbRolhm65SpVDY6C1Kr"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Find trending words
    trend_keywords = scrape_trends(auth)

    # Scrape with Streaming filtering by trending words
    stream_crawler = StreamCrawler(auth, trend_keywords, STREAM_TIME_LIMIT)
    stream_tweets = clean_up_tweets(stream_crawler.scrape())

    # Find power users
    power_users = find_power_users(stream_tweets, NO_POWER_USERS)

    # Scrape with the REST API
    rest_crawler = RestCrawler(auth, REST_TWEET_MAX)
    rest_tweets = []
    for user in power_users:
        rest_tweets += clean_up_tweets(rest_crawler.scrape(user))

    # Save tweets to MongoDB
    print("Saving scraped tweets to MongoDB...\n")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["WebScienceAssessment"]
    collection = db["tweets"]
    for tweet in rest_tweets:
        collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)
    for tweet in stream_tweets:
        collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)

    print("Done.")
    print("Total number of tweets stored:", collection.count())
