import pymongo
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]
collection = db["tweets"]
tweets = list(collection.find({}))

# Extract popular users and hashtags for each cluster
cluster_users = {}
cluster_hashtags = {}
clusters = []
for tweet in tweets:
    if(tweet["cluster"] not in cluster_users and tweet["cluster"] not in cluster_hashtags):
        clusters.append(tweet["cluster"])
        cluster_users[tweet["cluster"]] = {}
        cluster_hashtags[tweet["cluster"]] = {}

    if(tweet["user"] in cluster_users[tweet["cluster"]]):
        cluster_users[tweet["cluster"]][tweet["user"]] += 1
    else:
        cluster_users[tweet["cluster"]][tweet["user"]] = 1

    hashtags = re.findall(r"#(\w+)", tweet["text"])
    if(len(hashtags) > 0):
        for hashtag in hashtags:
            if(hashtag in cluster_hashtags[tweet["cluster"]]):
                cluster_hashtags[tweet["cluster"]][hashtag] += 1
            else:
                cluster_hashtags[tweet["cluster"]][hashtag] = 1

# Print popular users and hashtags
for cluster in sorted(clusters):
    power_users = cluster_users[cluster]
    sorted_users = sorted(power_users.items(), key=lambda item: item[1], reverse=True)
    print("\n5 most popular users for cluster %d:" % (cluster))
    for user in list(sorted_users)[:5]:
        print("%s with %d tweets." % (user[0], user[1]))

    power_hashtags = cluster_hashtags[cluster]
    sorted_hashtags = sorted(power_hashtags.items(), key=lambda item: item[1], reverse=True)
    print("\n5 most popular hashtags for cluster %d:" % (cluster))
    for hashtag in list(sorted_hashtags)[:5]:
        print("#%s with %d tweets." % (hashtag[0], hashtag[1]))

# Provide tweet and cluster statistics
# print("Total saved tweets:", len(tweets))
# print("Most popular hashtags")
# for cluster in sorted(clusters):
#     print("Tweets in cluster %d: %d" % (cluster, len(cluster_users[cluster])))
#     print("")
