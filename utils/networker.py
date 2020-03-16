import pymongo
import networkx as nx
import sys
import matplotlib.pyplot as plt
from matplotlib import pylab


def save_graph(graph, file_name):
    print("Construction and saving %s.pdf..." % file_name)

    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name+".pdf", bbox_inches="tight")
    pylab.close()
    del fig

    print("Done!")

def general_reply_graph(collection):
    print("Constructing general reply graph...")
    users = list(collection.find({}).distinct("user"))
    tweets = list(collection.find({}))
    reply_graph = nx.DiGraph()
    reply_graph.add_nodes_from(users)
    for tweet in tweets:
        if("replying_to_user" in tweet):
            reply_graph.add_edge(tweet["user"], tweet["replying_to_user"])
    print("Done!")
    return reply_graph

def cluster_reply_graphs(collection):
    print("Constructing cluster reply graphs...")
    clusters = list(collection.distinct("cluster"))
    cluster_reply_graphs = []
    for cluster in sorted(clusters):
        print("Constructing reply graph for cluster %d..." % cluster, end="")
        cluster_tweets = list(collection.find({"cluster":cluster}))
        cluster_users = list(collection.find({"cluster":cluster}).distinct("user"))
        reply_graph = nx.DiGraph()
        reply_graph.add_nodes_from(cluster_users)
        for tweet in cluster_tweets:
            if("replying_to_user" in tweet and tweet["replying_to_user"] is not None):
                reply_graph.add_edge(tweet["user"], tweet["replying_to_user"])
        cluster_reply_graphs.append(reply_graph)
        print("Done!")
    return(cluster_reply_graphs)

def general_mention_graph(collection):
    print("Constructing general mention graph...")
    users = list(collection.find({}).distinct("user"))
    tweets = list(collection.find({}))
    mention_graph = nx.DiGraph()
    mention_graph.add_nodes_from(users)
    for tweet in tweets:
        if(("mentioned_users" in tweet) and len(tweet["mentioned_users"]) > 0):
            for mention in tweet["mentioned_users"]:
                mention_graph.add_edge(tweet["user"], mention)
    print("Done!")
    return mention_graph

def cluster_mention_graphs(collection):
    print("Constructing cluster mention graphs...")
    clusters = list(collection.distinct("cluster"))
    cluster_mention_graphs = []
    for cluster in sorted(clusters):
        print("Constructing mention graph for cluster %d..." % cluster, end="")
        cluster_tweets = list(collection.find({"cluster":cluster}))
        cluster_users = list(collection.find({"cluster":cluster}).distinct("user"))
        mention_graph = nx.DiGraph()
        mention_graph.add_nodes_from(cluster_users)
        for tweet in cluster_tweets:
            if(("mentioned_users" in tweet) and len(tweet["mentioned_users"]) > 0):
                for mention in tweet["mentioned_users"]:
                    mention_graph.add_edge(tweet["user"], mention)
        cluster_mention_graphs.append(mention_graph)
        print("Done!")
    return(cluster_mention_graphs)

def general_retweet_graph(collection):
    print("Constructing general retweet graph...")
    users = list(collection.find({}).distinct("user"))
    tweets = list(collection.find({}))
    retweet_graph = nx.DiGraph()
    retweet_graph.add_nodes_from(users)
    for tweet in tweets:
        if(("retweeted_user" in tweet) and len(tweet["retweeted_user"]) > 0):
            retweet_graph.add_edge(tweet["retweeted_user"], tweet["user"])
    print("Done!")
    return retweet_graph

def cluster_retweet_graphs(collection):
    print("Constructing cluster retweet graphs...")
    clusters = list(collection.distinct("cluster"))
    cluster_retweet_graphs = []
    for cluster in sorted(clusters):
        print("Constructing retweet graph for cluster %d..." % cluster, end="")
        cluster_tweets = list(collection.find({"cluster":cluster}))
        cluster_users = list(collection.find({"cluster":cluster}).distinct("user"))
        retweet_graph = nx.DiGraph()
        retweet_graph.add_nodes_from(cluster_users)
        for tweet in cluster_tweets:
            if(("retweeted_user" in tweet) and len(tweet["retweeted_user"]) > 0):
                retweet_graph.add_edge(tweet["retweeted_user"], tweet["user"])
        cluster_retweet_graphs.append(retweet_graph)
        print("Done!")
    return(cluster_reply_graphs)

def general_hashtag_graph(collection):
    print("Constructing general hashtag graph...", end="")
    hashtags = list(collection.find({}).distinct("hashtags"))
    tweets = list(collection.find({}))
    hashtag_graph = nx.Graph()
    hashtag_graph.add_nodes_from(hashtags)
    for tweet in tweets:
        if(("hashtags" in tweet) and len(tweet["hashtags"]) > 0):
            for hashtag1 in tweet["hashtags"]:
                for hashtag2 in tweet["hashtags"]:
                    if(hashtag1 != hashtag2):
                        hashtag_graph.add_edge(hashtag1, hashtag2)
    print("Done!")
    return hashtag_graph

def cluster_hashtag_graphs(collection):
    print("Constructing cluster hashtag graphs...")
    clusters = list(collection.distinct("cluster"))
    cluster_hashtag_graphs = []
    for cluster in sorted(clusters):
        print("Constructing hashtag graph for cluster %d..." % cluster, end="")
        cluster_tweets = list(collection.find({"cluster":cluster}))
        cluster_hashtags = list(collection.find({"cluster":cluster}).distinct("hashtags"))
        hashtag_graph = nx.Graph()
        hashtag_graph.add_nodes_from(cluster_hashtags)
        for tweet in cluster_tweets:
            if(("hashtags" in tweet) and len(tweet["hashtags"]) > 0):
                for hashtag1 in tweet["hashtags"]:
                    for hashtag2 in tweet["hashtags"]:
                        if(hashtag1 != hashtag2):
                            hashtag_graph.add_edge(hashtag1, hashtag2)
        cluster_hashtag_graphs.append(hashtag_graph)
        print("Done!")
    return(cluster_hashtag_graphs)
