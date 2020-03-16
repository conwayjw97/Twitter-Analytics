import pymongo
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]
collection = db["tweets"]
tweets = list(collection.find({}))

# Extract statistics from each cluster
clusters = []
cluster_users = {}
cluster_hashtags = {}
cluster_replied_users = {}
cluster_mentioned_users = {}
cluster_retweeted_users = {}
cluster_keywords = {}
excluded_keywords = ("RT")

for tweet in tweets:
    if(tweet["cluster"] not in clusters):
        clusters.append(tweet["cluster"])
        cluster_users[tweet["cluster"]] = {}
        cluster_hashtags[tweet["cluster"]] = {}
        cluster_replied_users[tweet["cluster"]] = {}
        cluster_mentioned_users[tweet["cluster"]] = {}
        cluster_retweeted_users[tweet["cluster"]] = {}
        cluster_keywords[tweet["cluster"]] = {}

    if(tweet["user"] in cluster_users[tweet["cluster"]]):
        cluster_users[tweet["cluster"]][tweet["user"]] += 1
    else:
        cluster_users[tweet["cluster"]][tweet["user"]] = 1

    if(("hashtags" in tweet) and len(tweet["hashtags"]) > 0):
        for hashtag in tweet["hashtags"]:
            if(hashtag in cluster_hashtags[tweet["cluster"]]):
                cluster_hashtags[tweet["cluster"]][hashtag] += 1
            else:
                cluster_hashtags[tweet["cluster"]][hashtag] = 1

    if("replying_to_user" in tweet):
        if(tweet["replying_to_user"] in cluster_replied_users[tweet["cluster"]]):
            cluster_replied_users[tweet["cluster"]][tweet["replying_to_user"]] += 1
        else:
            cluster_replied_users[tweet["cluster"]][tweet["replying_to_user"]] = 1

    if(("mentioned_users" in tweet) and len(tweet["mentioned_users"]) > 0):
        for user in tweet["mentioned_users"]:
            if(user in cluster_mentioned_users[tweet["cluster"]]):
                cluster_mentioned_users[tweet["cluster"]][user] += 1
            else:
                cluster_mentioned_users[tweet["cluster"]][user] = 1

    if(("retweeted_user" in tweet) and len(tweet["retweeted_user"]) > 0):
        if(tweet["retweeted_user"] in cluster_retweeted_users[tweet["cluster"]]):
            cluster_retweeted_users[tweet["cluster"]][tweet["retweeted_user"]] += 1
        else:
            cluster_retweeted_users[tweet["cluster"]][tweet["retweeted_user"]] = 1

    for word in tweet["text"].split():
        if(word not in excluded_keywords and not word.startswith("#") and not word.startswith("@")):
            if(word in cluster_keywords[tweet["cluster"]]):
                cluster_keywords[tweet["cluster"]][word] += 1
            else:
                cluster_keywords[tweet["cluster"]][word] = 1


# Print popular users and hashtags
for cluster in sorted(clusters):
    print("\n\nStatistics for cluster %d." % cluster)
    print("-------------------------------------------")

    sorted_users = sorted(cluster_users[cluster].items(), key=lambda item: item[1], reverse=True)
    print("\n5 most active users for cluster %d:" % (cluster))
    for user in list(sorted_users)[:5]:
        print("%s with %d tweets." % (user[0], user[1]))

    sorted_hashtags = sorted(cluster_hashtags[cluster].items(), key=lambda item: item[1], reverse=True)
    print("\n5 most popular hashtags for cluster %d:" % (cluster))
    for hashtag in list(sorted_hashtags)[:5]:
        print("#%s with %d tweets." % (hashtag[0], hashtag[1]))

    sorted_replied = sorted(cluster_replied_users[cluster].items(), key=lambda item: item[1], reverse=True)
    print("\n5 most replied to users for cluster %d:" % (cluster))
    for user in list(sorted_replied)[:5]:
        print("%s with %d replies." % (user[0], user[1]))

    sorted_mentioned = sorted(cluster_mentioned_users[cluster].items(), key=lambda item: item[1], reverse=True)
    print("\n5 most mentioned users for cluster %d:" % (cluster))
    for user in list(sorted_mentioned)[:5]:
        print("%s with %d mentions." % (user[0], user[1]))

    sorted_retweeted = sorted(cluster_retweeted_users[cluster].items(), key=lambda item: item[1], reverse=True)
    print("\n5 most retweeted users for cluster %d:" % (cluster))
    for user in list(sorted_retweeted)[:5]:
        print("%s with %d retweets." % (user[0], user[1]))

    sorted_keywords = sorted(cluster_keywords[cluster].items(), key=lambda item: item[1], reverse=True)
    print("\n5 most common keywords for cluster %d:" % (cluster))
    for word in list(sorted_keywords)[:5]:
        print("'%s' appearing in %d tweets." % (word[0], word[1]))
