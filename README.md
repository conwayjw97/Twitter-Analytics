# Twitter-Analytics
Undergraduate Year 4 Web Science Project - Twitter crawler for data collection and analytics

## Install dependencies

Open a terminal and run:
```
pip3 install pymongo tweepy sklearn networkx matplotlib
```

## Run with collected Tweets and clusterings

#### Setup MongoDB

All the tweets and their respective clustering present in report are packaged into the provided MongoDB collection. To load this onto your own MongoDB, open a terminal and run:
```mongorestore -d WebScienceAssessment mongodb_dump```

## Collect and cluster your own Tweets 

#### Setup keys
To set up the necessary API keys, go to utils/crawling.py, then insert your API keys in the appropriate variables present from line 7 onwards:
```
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
```

#### Crawling
After the keys have been added, you can collect your own by executing: ```python3 collect_tweets.py <No_Power_Users> <Stream_Time> <Max_REST_Tweets> <Cluster_Only>```

Runtime arguments refer to:

	<No_Power_Users>: Number of power users to be used in REST tweet crawling.

	<Stream_Time>: Amount of time in seconds to perform 1% Stream crawling.

	<Max_REST_Tweets>: Max number of tweets to try to retrieve for each REST tweet crawling request.

	<Cluster_Only>: If 1, only clusterise saved tweets instead of crawling.

## See Tweet Statistics

#### Cluster Statistics

To calculate and see cluster statistics run: ```python3 cluster_analytics.py```

#### Network Analysis

To calculate and output network analyses, run: ``` python3 network_analytics.py <Network_Type> <Save_Network> <Save_Graphs>```

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
	
#### Save output to file

There will probably be a large number of clusters that both analysis scripts will return results for. If you'd like to save these statistics to a text file for easier reading or searching, simply append ``` > Output.txt``` to the end of the run command.

```python3 cluster_analytics.py > Output.txt```

``` python3 network_analytics.py <Network_Type> <Save_Network> <Save_Graphs> > Output.txt```

## Folders

/db - MongoDB helper scripts

/graphs - Graph and network output folder

/mongodb_dump - Crawled tweets 

/report - PDF report

/utils - Utility functions
