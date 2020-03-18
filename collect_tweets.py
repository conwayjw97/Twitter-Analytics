import sys
import pymongo

from utils import clustering, crawling

def find_power_users(tweets, no_users):
    power_users = {}
    for tweet in tweets:
        tweet = tweet["data"]
        if(tweet["user"] in power_users):
            power_users[tweet["user"]] += 1
        else:
            power_users[tweet["user"]] = 1

    sorted_power_users = sorted(power_users, key=power_users.get, reverse=True)
    print("\n%d users with the most tweets:" % no_users)
    for i in range(no_users):
        print("%s with %d tweets." % (sorted_power_users[i], power_users[sorted_power_users[i]]))
    print()

    return(sorted_power_users[:no_users])

if(len(sys.argv) - 1 < 4):
    print("Please run this program with arguments: collect_tweets.py <No_Power_Users> <Stream_Time> <Max_REST_Tweets> <Cluster_Only>")
    print("\n<No_Power_Users>: Number of power users to be used in REST tweet crawling.")
    print("<Stream_Time>: Amount of time in seconds to perform 1% Stream crawling.")
    print("<Max_REST_Tweets>: Max number of tweets to try to retrieve for each REST tweet crawling request.")
    print("<Cluster_Only>: If 1, only clusterise saved tweets instead of crawling.")
else:
    # Scraping parameters
    NO_POWER_USERS = int(sys.argv[1])
    STREAM_TIME_LIMIT = int(sys.argv[2])
    REST_TWEET_MAX = int(sys.argv[3])
    CLUSTER_ONLY = int(sys.argv[4])

    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["WebScienceAssessment"]
    collection = db["tweets"]

    if(CLUSTER_ONLY != 1):
        # Find trending words
        trend_keywords = crawling.scrape_trends()

        # Scrape with Streaming filtering by trending words
        stream_crawler = crawling.StreamCrawler(trend_keywords, STREAM_TIME_LIMIT)
        stream_tweets = stream_crawler.scrape()

        # Find power users
        power_users = find_power_users(stream_tweets, NO_POWER_USERS)

        # Scrape with the REST API
        rest_crawler = crawling.RestCrawler(REST_TWEET_MAX)
        rest_tweets = []
        for user in power_users:
            rest_tweets += rest_crawler.scrape(user)

        # Save tweets to MongoDB
        print("Saving scraped tweets to MongoDB...\n")
        for tweet in rest_tweets:
            collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)
        for tweet in stream_tweets:
            collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)

        print("Done.")
        print("Total number of tweets stored:", collection.count())

    # Clusterise tweets
    clustering.clusterise_tweets(collection)
