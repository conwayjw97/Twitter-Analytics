# https://www.w3schools.com/python/python_mongodb_getstarted.asp
# https://stackabuse.com/accessing-the-twitter-api-with-python/?fbclid=IwAR3PnBWLlu3o5yCXPLUoO6IyNCxza6HEXkYuOH_65iyYpMcNtpDoVqLoh5o
# https://tweepy.readthedocs.io/en/latest/api.html#API.search
# https://gist.github.com/jaymcgrath/367c521f1dd786bc5a05ec3eeeb1cb04

import pymongo
import tweepy

consumer_key = "8CRA9cjpku4BtfK1vuJ5QAPLg"
consumer_secret = "uAGmC5CpJY5vjTom2l8AhXAtKeu3aFCm69Atxl19YXlUIvwN0F"
access_token = "1072253339113611266-3Th0tGTF5hlAluASFHW9QmlCowQgsa"
access_token_secret = "P9G1QCQfgFDV55P2coN6tR2L19DbRolhm65SpVDY6C1Kr"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

keyword = "assange"

# Gather snowden tweets with the REST API
api = tweepy.API(auth, wait_on_rate_limit=True)
RestTweets = []
try:
    print("Scraping with the REST API...")
    for tweet in api.search(q=keyword, lang="en", result_type="recent", count=1, full_text=True):
        print("Tweet by %s at %s: %s" % (tweet.id, tweet.created_at, tweet.text))
        RestTweets.append((tweet.created_at,tweet.id,tweet.text))
except BaseException as e:
    print('failed on_status,',str(e))
    # time.sleep(3)

# Gather snowden tweets with Streaming
class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.api = tweepy.API()
        self.tweet_count = 0
        self.tweets = []

    def on_status(self, status):
        # Try to get the extended tweet if it's long enough
        try:
            tweet_text = status.extended_tweet['full_text']
        except Exception as e:
            tweet_text = status.text
        print("Tweet by %s at %s: %s" % (status.id, status.created_at, tweet_text))
        self.tweets.append((status.created_at, status.id, tweet_text))
        self.tweet_count += 1

listener = MyStreamListener()
stream = tweepy.Stream(auth, listener)
StreamTweets = []
try:
    print('Scraping with the Streaming API... \nPress Ctrl+C in order to stop execution \n')
    stream.filter(track=[keyword], languages=["en"])
except(KeyboardInterrupt):
    print ('# of tweets fetched: ', listener.tweet_count)


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
