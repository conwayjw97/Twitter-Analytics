import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]
collection = db["tweets"]
tweets = list(collection.find({}))

for tweet in tweets:
    print(tweet)
