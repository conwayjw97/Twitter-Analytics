# https://www.w3schools.com/python/python_mongodb_getstarted.asp
# https://stackabuse.com/accessing-the-twitter-api-with-python/?fbclid=IwAR3PnBWLlu3o5yCXPLUoO6IyNCxza6HEXkYuOH_65iyYpMcNtpDoVqLoh5o
# https://tweepy.readthedocs.io/en/latest/api.html#API.search
# https://gist.github.com/jaymcgrath/367c521f1dd786bc5a05ec3eeeb1cb04

import pymongo
import tweepy
import time

class RestCrawler():
    def __init__(self, auth, keyword, scrape_max):
        self.auth = auth
        self.keyword = keyword
        self.scrape_max = scrape_max

    def scrape(self):
        api = tweepy.API(auth, wait_on_rate_limit=True)
        rest_tweets = []
        tweet_count = 0
        try:
            print("Scraping with the REST API...")
            for tweet in api.search(q=self.keyword, lang="en", result_type="recent", count=self.scrape_max, full_text=True):
                # Try to get the extended tweet if it's long enough
                try:
                    tweet_text = tweet.extended_tweet["full_text"]
                except Exception as e:
                    tweet_text = tweet.text
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
            try:
                tweet_text = status.extended_tweet["full_text"]
            except Exception as e:
                tweet_text = status.text
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
            stream.filter(track=[self.keyword], languages=["en"])
        except KeyboardInterrupt:
            pass
        except BaseException as e:
            print("Failed, on_status:", str(e))
        print("Number of tweets fetched through streaming:", listener.tweet_count, "\n")
        return listener.get_tweets()

# Set keys and configure Twitter app authorisation
consumer_key = "8CRA9cjpku4BtfK1vuJ5QAPLg"
consumer_secret = "uAGmC5CpJY5vjTom2l8AhXAtKeu3aFCm69Atxl19YXlUIvwN0F"
access_token = "1072253339113611266-3Th0tGTF5hlAluASFHW9QmlCowQgsa"
access_token_secret = "P9G1QCQfgFDV55P2coN6tR2L19DbRolhm65SpVDY6C1Kr"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Scraping parameters
KEYWORD = "assange"
REST_TWEET_MAX = 1
STREAM_TIME_LIMIT = 1

# Scrape with the REST API
rest_crawler = RestCrawler(auth, KEYWORD, REST_TWEET_MAX)
rest_tweets = rest_crawler.scrape()

# Scrape with Streaming
stream_crawler = StreamCrawler(auth, KEYWORD, STREAM_TIME_LIMIT)
stream_tweets = stream_crawler.scrape()

# Save tweets to MongoDB
print("Saving scraped tweets to MongoDB...\n")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]

# print(client.list_database_names())
# dblist = client.list_database_names()
# if "WebScienceAssessment" in dblist:
#   print("Your database exists.")

collection = db["tweets"]
for tweet in rest_tweets:
    collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)
for tweet in stream_tweets:
    collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)

print("Done.")
print("Total number of tweets stored:", collection.count())
