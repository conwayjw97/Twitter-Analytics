# https://www.w3schools.com/python/python_mongodb_getstarted.asp
# https://stackabuse.com/accessing-the-twitter-api-with-python/?fbclid=IwAR3PnBWLlu3o5yCXPLUoO6IyNCxza6HEXkYuOH_65iyYpMcNtpDoVqLoh5o
# https://tweepy.readthedocs.io/en/latest/api.html#API.search
# https://gist.github.com/jaymcgrath/367c521f1dd786bc5a05ec3eeeb1cb04

import pymongo
import tweepy

class RestCrawler():
    def __init__(self, auth, keyword, tweet_count):
        self.auth = auth
        self.keyword = keyword
        self.tweet_count = tweet_count

    def scrape():
        api = tweepy.API(auth, wait_on_rate_limit=True)
        rest_tweets = []
        tweet_count = 0
        try:
            print("Scraping with the REST API...")
            for tweet in api.search(q=keyword, lang="en", result_type="recent", count=tweet_count, full_text=True):
                rest_tweets.append((tweet.created_at,tweet.id,tweet.text))
                tweet_count += 1
        except BaseException as e:
            print("Failed on_status,", str(e))

class StreamCrawler():
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
                # print("Tweet by %s at %s: %s" % (status.id, status.created_at, tweet_text))
                self.tweets.append((status.created_at, status.id, tweet_text))
                self.tweet_count += 1
                return True
            else:
                return False

    def __init__(self, auth, keyword, time_limit):
        self.auth = auth
        self.keyword = keyword
        self.time_limit = time_limit

    def scrape():
        listener = MyStreamListener(time_limit)
        stream = tweepy.Stream(self.auth, listener)
        stream_tweets = []
        try:
            print("Scraping with the Streaming API... \nPress Ctrl+C in order to stop execution \n")
            stream.filter(track=[keyword], languages=["en"])
        except(KeyboardInterrupt):
            print ("# of tweets fetched: ", listener.tweet_count)

consumer_key = "8CRA9cjpku4BtfK1vuJ5QAPLg"
consumer_secret = "uAGmC5CpJY5vjTom2l8AhXAtKeu3aFCm69Atxl19YXlUIvwN0F"
access_token = "1072253339113611266-3Th0tGTF5hlAluASFHW9QmlCowQgsa"
access_token_secret = "P9G1QCQfgFDV55P2coN6tR2L19DbRolhm65SpVDY6C1Kr"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

keyword = "assange"

# Scrape with the REST API
rest_crawler = RestCrawler(auth, keyword, 1000000)
rest_crawler.scrape()

# Scrape with Streaming
stream_crawler = StreamCrawler(auth, keyword, 100)
stream_crawler.scrape()

# client = pymongo.MongoClient("mongodb://localhost:27017/")
#
# db = client["WebScienceAssessment"]
#
# print(client.list_database_names())
#
# dblist = client.list_database_names()
# if "WebScienceAssessment" in dblist:
#   print("Your database exists.")
#
# col = db["test"]
# mydict = { "name": "John", "address": "Highway 37" }
# x = col.insert_one(mydict)
# print(x.inserted_id)
# print(db.list_collection_names())
