# https://www.w3schools.com/python/python_mongodb_getstarted.asp
# https://stackabuse.com/accessing-the-twitter-api-with-python/?fbclid=IwAR3PnBWLlu3o5yCXPLUoO6IyNCxza6HEXkYuOH_65iyYpMcNtpDoVqLoh5o

import pymongo
import tweepy

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)

client = pymongo.MongoClient("mongodb://localhost:27017/")




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
