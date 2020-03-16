import sys

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

    return(sorted_power_users[:no_users])

if(len(sys.argv) - 1 < 3):
    print("Please run this program with arguments: collect_tweets.py <No_Power_Users> <Stream_Time> <Max_REST_Tweets>")
    print("\n<No_Power_Users>: Number of power users to be used in REST tweet crawling.")
    print("<Stream_Time>: Amount of time in seconds to perform 1% Stream crawling.")
    print("<Max_REST_Tweets>: Max number of tweets to try to retrieve for each REST tweet crawling request.")
else:
    # Scraping parameters
    NO_POWER_USERS = int(sys.argv[1])
    STREAM_TIME_LIMIT = int(sys.argv[2])
    REST_TWEET_MAX = int(sys.argv[3])

    # Set keys and configure Twitter app authorisation
    consumer_key = "8CRA9cjpku4BtfK1vuJ5QAPLg"
    consumer_secret = "uAGmC5CpJY5vjTom2l8AhXAtKeu3aFCm69Atxl19YXlUIvwN0F"
    access_token = "1072253339113611266-3Th0tGTF5hlAluASFHW9QmlCowQgsa"
    access_token_secret = "P9G1QCQfgFDV55P2coN6tR2L19DbRolhm65SpVDY6C1Kr"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Find trending words
    trend_keywords = crawling.scrape_trends(auth)

    # Scrape with Streaming filtering by trending words
    stream_crawler = crawling.StreamCrawler(auth, trend_keywords, STREAM_TIME_LIMIT)
    stream_tweets = stream_crawler.scrape()

    # Find power users
    power_users = find_power_users(stream_tweets, NO_POWER_USERS)

    # Scrape with the REST API
    rest_crawler = crawling.RestCrawler(auth, REST_TWEET_MAX)
    rest_tweets = []
    for user in power_users:
        rest_tweets += rest_crawler.scrape(user)

    # Save tweets to MongoDB
    print("Saving scraped tweets to MongoDB...\n")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["WebScienceAssessment"]
    collection = db["tweets"]
    for tweet in rest_tweets:
        collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)
    for tweet in stream_tweets:
        collection.update({"id":tweet["id"]}, {"$set" : tweet["data"]}, upsert=True)

    print("Done.")
    print("Total number of tweets stored:", collection.count())

    # Clusterise tweets
    clustering.clusterise_tweets(collection)
