import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]
collection = db["tweets"]
tweets = list(collection.find({}))

for tweet in tweets:
    print("Tweet by %s at %s: %s" % (tweet["user"], tweet["time"], tweet["text"]))
    if(("hashtags" in tweet) and len(tweet["hashtags"]) > 0):
        print("Hashtags:", tweet["hashtags"])
    if("replying_to_user" in tweet and tweet["replying_to_user"] is not None):
        print("Replying to user:", tweet["replying_to_user"])
        print("Replying to tweet:", tweet["replying_to_tweet"])
    if(("mentioned_users" in tweet) and len(tweet["mentioned_users"]) > 0):
        print("Users mentioned:", tweet["mentioned_users"])
    if(("retweeted_user" in tweet) and tweet["retweeted_user"] is not None):
        print("Retweeted user:", tweet["retweeted_user"])
        print("Retweeted tweet:", tweet["retweeted_text"])
    print("------------------------------------")
