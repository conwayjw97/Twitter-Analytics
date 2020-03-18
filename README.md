# Twitter-Analytics
Undergraduate Year 4 Web Science Project - Twitter crawler for data collection and analytics

### MongoDB Setup

To import the MongoDB collection, open a terminal and run:
```mongorestore -d WebScienceAssessment mongodb_dump```

### Crawling
To collect your own tweets run: ```python3 collect_tweets.py <No_Power_Users> <Stream_Time> <Max_REST_Tweets> <Cluster_Only>```

The arguments refer to:

```<No_Power_Users>```: Number of power users to be used in REST tweet crawling.

```<Stream_Time>```: Amount of time in seconds to perform 1% Stream crawling.

```<Max_REST_Tweets>```: Max number of tweets to try to retrieve for each REST tweet crawling request.

```<Cluster_Only>```: If 1, only clusterise saved tweets instead of crawling.

### Cluster Statistics

To calculate and output cluster statistics run: ```python3 cluster_analytics.py```

### Network Analysis

To calculate and output network analyses run: ``` python3 network_analytics.py <Network_Type> <Save_Network> <Save_Graphs>```

```<Network_Type>``` choices:

1 - General Reply Interaction Graph

2 - Cluster Reply Interaction Graphs

3 - General Mention Interaction Graph

4 - Cluster Mention Interaction Graphs

5 - General Retweet Interaction Graph

6 - Cluster Retweet Interaction Graphs

7 - General Hashtag Co-occurence Graph

8 - Cluster Hashtag Co-occurence Graphs

```<Save_Network>``` choices:

0 - Don't save networks

1 - Save networks as .pdf files in /graphs (WARNING: VERY TIME CONSUMING)

```<Save_Graphs>``` choices:

0 - Don't save graphs

1 - Save graphs as .png files in /graphs

### Folders

/db - MongoDB helper scripts

/graphs - Graph and network output folder

/mongodb_dump - Crawled tweets 

/report - PDF report

/utils - Utility functions
