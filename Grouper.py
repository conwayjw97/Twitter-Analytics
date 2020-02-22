import pymongo
import tweepy
from textblob import TextBlob

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]
collection = db["tweets"]


# Calculate tweet sentiment and update database entry with grouping
tweets = list(collection.find({}))
positive_count = neutral_count = negative_count = 0
for tweet in tweets:
    if("sentiment" not in tweet):
        update_query = {"id":tweet["id"]}

        if(TextBlob(tweet["text"]).sentiment.polarity < 0):
            new_group = {"$set":{"sentiment":"negative"}}
            negative_count += 1
        elif(TextBlob(tweet["text"]).sentiment.polarity == 0):
            new_group = {"$set":{"sentiment":"neutral"}}
            neutral_count += 1
        elif(TextBlob(tweet["text"]).sentiment.polarity > 0):
            new_group = {"$set":{"sentiment":"positive"}}
            positive_count += 1

        collection.update_one(update_query, new_group)

print("New Negative tweets:", negative_count)
print("New Neutral tweets:", neutral_count)
print("New Positive tweets:", positive_count)
