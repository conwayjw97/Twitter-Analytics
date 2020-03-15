import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]
collection = db["tweets"]
tweets = list(collection.find({}))

for tweet in tweets:
    print("Tweet by %s at %s: %s" % (tweet["user"], tweet["time"], tweet["text"]))
    print("------------------------------------")
