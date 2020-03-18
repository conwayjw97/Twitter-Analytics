# Twitter-Analytics
Undergraduate Year 4 Web Science Project - Twitter crawler for data collection and analytics

To import the MongoDB collection, open a terminal and run:
```mongorestore -d WebScienceAssessment mongodb_dump```

To collect your own tweets run ```python3 collect_tweets.py <No_Power_Users> <Stream_Time> <Max_REST_Tweets> <Cluster_Only>```
The arguments refer to:
```<No_Power_Users>```: Number of power users to be used in REST tweet crawling.
```<Stream_Time>```: Amount of time in seconds to perform 1% Stream crawling.
```<Max_REST_Tweets>```: Max number of tweets to try to retrieve for each REST tweet crawling request.
```<Cluster_Only>```: If 1, only clusterise saved tweets instead of crawling.
