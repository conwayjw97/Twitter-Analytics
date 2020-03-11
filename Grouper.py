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

# Extract most common usernames and hashtags from each sentiment group
positive_tweets = list(collection.find({"sentiment":"positive"}))
positive_users = {}
positive_hashtags = {}
for tweet in positive_tweets:
    if(tweet["user"] in positive_users):
        positive_users[tweet["user"]] += 1
    else:
        positive_users[tweet["user"]] = 1

    hashtags = [word for word in tweet["text"].replace(',','').split() if word[0] == '#']
    if(len(hashtags) > 0):
        for hashtag in hashtags:
            if(hashtag in positive_hashtags):
                positive_hashtags[hashtag] += 1
            else:
                positive_hashtags[hashtag] = 1

sorted_positive_users = sorted(positive_users, key=positive_users.get, reverse=True)
sorted_positive_hashtags = sorted(positive_hashtags, key=positive_hashtags.get, reverse=True)
print("\n5 users with the most positive tweets:")
for i in range(5):
    print("%s with %d tweets." % (sorted_positive_users[i], positive_users[sorted_positive_users[i]]))
print("\n5 most popular hashtags in the positive tweets:")
for i in range(5):
    print("%s with %d tweets." % (sorted_positive_hashtags[i], positive_hashtags[sorted_positive_hashtags[i]]))


neutral_tweets = list(collection.find({"sentiment":"neutral"}))
neutral_users = {}
neutral_hashtags = {}
for tweet in neutral_tweets:
    if(tweet["user"] in neutral_users):
        neutral_users[tweet["user"]] += 1
    else:
        neutral_users[tweet["user"]] = 1

    hashtags = [word for word in tweet["text"].replace(',','').split() if word[0] == '#']
    if(len(hashtags) > 0):
        for hashtag in hashtags:
            if(hashtag in neutral_hashtags):
                neutral_hashtags[hashtag] += 1
            else:
                neutral_hashtags[hashtag] = 1

sorted_neutral_users = sorted(neutral_users, key=neutral_users.get, reverse=True)
sorted_neutral_hashtags = sorted(neutral_hashtags, key=neutral_hashtags.get, reverse=True)
print("\n5 users with the most neutral tweets:")
for i in range(5):
    print("%s with %d tweets." % (sorted_neutral_users[i], neutral_users[sorted_neutral_users[i]]))
print("\n5 most popular hashtags in the neutral tweets:")
for i in range(5):
    print("%s with %d tweets." % (sorted_neutral_hashtags[i], neutral_hashtags[sorted_neutral_hashtags[i]]))


negative_tweets = list(collection.find({"sentiment":"negative"}))
negative_users = {}
negative_hashtags = {}
for tweet in negative_tweets:
    if(tweet["user"] in negative_tweets):
        negative_users[tweet["user"]] += 1
    else:
        negative_users[tweet["user"]] = 1

    hashtags = [word for word in tweet["text"].replace(',','').split() if word[0] == '#']
    if(len(hashtags) > 0):
        for hashtag in hashtags:
            if(hashtag in negative_hashtags):
                negative_hashtags[hashtag] += 1
            else:
                negative_hashtags[hashtag] = 1

sorted_negative_users = sorted(negative_users, key=negative_users.get, reverse=True)
sorted_negative_hashtags = sorted(negative_hashtags, key=negative_hashtags.get, reverse=True)
print("\n5 users with the most negative tweets:")
for i in range(5):
    print("%s with %d tweets." % (sorted_negative_users[i], negative_users[sorted_negative_users[i]]))
print("\n5 most popular hashtags in the negative tweets:")
for i in range(5):
    print("%s with %d tweets." % (sorted_negative_hashtags[i], negative_hashtags[sorted_negative_hashtags[i]]))
