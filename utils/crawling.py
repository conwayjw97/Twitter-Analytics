import tweepy
import time
import re
import json

# Set keys and configure Twitter app authorisation
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

def clean_up_tweet(tweet):
    # Remove URLs
    tweet = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', str(tweet), flags=re.MULTILINE)
    # Remove new lines
    tweet = re.sub(r'/\r?\n|\r/', '', str(tweet), flags=re.MULTILINE)
    # Remove broken symbols
    tweet = re.sub(r'&amp;', '', str(tweet), flags=re.MULTILINE)
    return tweet

def scrape_trends():
    api = tweepy.API(auth)

    # WOE ID for UK is 12723
    # WOE ID for US is 2352824
    trends = api.trends_place(2352824)[0]["trends"]

    trend_keywords = []
    for trend in trends:
        trend_keywords.append(trend["name"])

    print("Trending keywords:", trend_keywords, "\n")

    return trend_keywords

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, time_limit):
        self.api = tweepy.API()
        self.tweet_count = 0
        self.tweets = []
        self.time_limit = time_limit
        self.start_time = time.time()

    def on_status(self, status):
        if (time.time() - self.start_time) < self.time_limit:
            data = {}
            data["time"] = status.created_at
            data["user"] = status.user.screen_name

            try:
                tweet_text = status.extended_tweet["full_text"]
            except AttributeError:
                tweet_text = status.text
            data["text"] = clean_up_tweet(tweet_text)

            # Check if Retweet
            if hasattr(status, "retweeted_status"):
                data["retweeted_user"] = status.retweeted_status.user.screen_name
                data["retweeted_id"] = status.retweeted_status.id
                try:
                    retweeted_text = status.retweeted_status.extended_tweet["full_text"]
                except AttributeError:
                    retweeted_text = status.retweeted_status.text
                data["retweeted_text"] = clean_up_tweet(retweeted_text)

            # Check if a reply
            if hasattr(status, "in_reply_to_screen_name"):
                data["replying_to_tweet"] = status.in_reply_to_status_id
                data["replying_to_user"] = status.in_reply_to_screen_name

            # Check for user mentions or hashtags
            if hasattr(status, "entities"):
                entities = status.entities
                if(("user_mentions" in entities) and len(entities["user_mentions"]) > 0):
                    data["mentioned_users"] = []
                    for mention in entities["user_mentions"]:
                        data["mentioned_users"].append(mention["screen_name"])

                if(("hashtags" in entities) and len(entities["hashtags"]) > 0):
                    data["hashtags"] = []
                    for hashtag in entities["hashtags"]:
                        data["hashtags"].append(hashtag["text"])

            self.tweets.append({"id":status.id, "data":data})
            self.tweet_count += 1
            return True
        else:
            return False

    def get_tweets(self):
        return self.tweets

class StreamCrawler():
    def __init__(self, keywords, time_limit):
        self.keywords = keywords
        self.time_limit = time_limit

    def scrape(self):
        listener = MyStreamListener(self.time_limit)
        stream = tweepy.Stream(auth, listener, tweet_mode="extended")
        try:
            print("Scraping with the Streaming API... \nPress Ctrl+C in order to stop streaming or wait for the", self.time_limit, "second time limit")
            stream.filter(track=self.keywords, languages=["en"])
        except KeyboardInterrupt:
            pass
        except BaseException as e:
            print("Failed, on_status:", str(e))
        print("Number of tweets fetched through streaming:", listener.tweet_count)
        return listener.get_tweets()

class RestCrawler():
    def __init__(self, scrape_max):
        self.scrape_max = scrape_max

    def scrape(self, keyword):
        api = tweepy.API(auth, wait_on_rate_limit=True)
        rest_tweets = []
        tweet_count = 0
        try:
            print("Scraping user '%s' with the REST API..." % keyword)
            for status in api.search(q=keyword, lang="en", result_type="recent", count=self.scrape_max, full_text=True, tweet_mode="extended"):
                data = {}
                data["time"] = status.created_at
                data["user"] = status.user.screen_name

                try:
                    tweet_text = status.extended_tweet["full_text"]
                except AttributeError:
                    tweet_text = status.full_text
                data["text"] = clean_up_tweet(tweet_text)

                if hasattr(status, "retweeted_status"):  # Check if Retweet
                    # print("retweeted status:", status.retweeted_status)
                    data["retweeted_user"] = status.retweeted_status.user.screen_name
                    data["retweeted_id"] = status.retweeted_status.id
                    try:
                        retweeted_text = status.retweeted_status.extended_tweet["full_text"]
                    except AttributeError:
                        retweeted_text = status.retweeted_status.full_text
                    data["retweeted_text"] = clean_up_tweet(retweeted_text)

                if hasattr(status, "in_reply_to_screen_name"): # Check if a reply
                    data["replying_to_tweet"] = status.in_reply_to_status_id
                    data["replying_to_user"] = status.in_reply_to_screen_name

                # Check for user mentions or hashtags
                if hasattr(status, "entities"):
                    entities = status.entities
                    if(("user_mentions" in entities) and len(entities["user_mentions"]) > 0):
                        data["mentioned_users"] = []
                        for mention in entities["user_mentions"]:
                            data["mentioned_users"].append(mention["screen_name"])

                    if(("hashtags" in entities) and len(entities["hashtags"]) > 0):
                        data["hashtags"] = []
                        for hashtag in entities["hashtags"]:
                            data["hashtags"].append(hashtag["text"])

                rest_tweets.append({"id":status.id, "data":data})

                tweet_count += 1
        except BaseException as e:
            print("Failed, on_status:", str(e))
        print ("Number of tweets scraped through REST:", tweet_count)
        return rest_tweets
