import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]

col = db["tweets"]
col.drop()

print("Tweet collection dropped.")
