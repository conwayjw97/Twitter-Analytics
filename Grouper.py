import pymongo
import tweepy

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WebScienceAssessment"]
collection = db["tweets"]
tweets = list(collection.find({}))

# Clusterise tweets
no_clusters = 10

tweet_text = []
for tweet in tweets:
    tweet_text.append(tweet["text"])

vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(tweet_text)

model = KMeans(n_clusters=no_clusters, init='k-means++', max_iter=100, n_init=10)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(no_clusters):
    print ("Cluster %d:" % i)
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind])
    print()

# Update database entry with clustering
clustering_count = {}
for tweet in tweets:
    if("cluster" not in tweet):
        update_query = {"id":tweet["id"]}
        cluster = model.predict(vectorizer.transform([tweet["text"]]))[0]
        if(cluster in clustering_count):
            clustering_count[cluster] += 1
        else:
            clustering_count[cluster] = 1
        new_cluster = {"$set":{"cluster":int(cluster)}}
        collection.update_one(update_query, new_cluster)

for cluster in sorted(clustering_count.keys()):
    print("New tweets for cluster %d: %d" % (cluster, clustering_count[cluster]))
