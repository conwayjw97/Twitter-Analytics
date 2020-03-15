import pymongo
import networkx as nx
import re
import sys
import matplotlib.pyplot as plt
from matplotlib import pylab


def save_graph(graph, file_name):
    #initialze Figure
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

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

def general_reply_graph(collection):
    print("Constructing general reply graph...", end="")
    reply_graph = nx.DiGraph()
    users = list(collection.find({}).distinct("user"))
    reply_graph.add_nodes_from(users)
    for tweet in tweets:
        if (hasattr(tweet, "replying_to_user") and (tweet["replying_to_user"] is not None)):
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
            if (hasattr(tweet, "replying_to_user") and (tweet["replying_to_user"] is not None)):
                reply_graph.add_edge(tweet["user"], tweet["replying_to_user"])
        cluster_reply_graphs.append(reply_graph)
        print("Done!")
    return(cluster_reply_graphs)

def general_retweet_graph(collection):
    print("Constructing general retweet graph...", end="")
    retweet_graph = nx.DiGraph()
    users = list(collection.find({}).distinct("user"))
    retweet_graph.add_nodes_from(users)
    for tweet in tweets:
        if(hasattr(tweet, "retweeted_user") and (tweet["retweeted_user"] is not None)):
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
            if(hasattr(tweet, "retweeted_user") and (tweet["retweeted_user"] is not None)):
                retweet_graph.add_edge(tweet["retweeted_user"], tweet["user"])
        cluster_retweet_graphs.append(retweet_graph)
        print("Done!")
    return(cluster_reply_graphs)

if(len(sys.argv) - 1 < 1):
    print("Please run this program with arguments: Networker.py <Network_Type>")
    print("\n<Network_Type> choices:")
    print("1 - General Reply Interaction Graph")
    print("2 - Cluster Reply Interaction Graphs")
    print("3 - General Retweet Interaction Graph")
    print("4 - Cluster Retweet Interaction Graphs")
else:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["WebScienceAssessment"]
    collection = db["tweets"]
    tweets = list(collection.find({}))
    GRAPH_CHOICE = int(sys.argv[1])

    # Construct general reply interaction graph
    if(GRAPH_CHOICE == 1):
        reply_graph = general_reply_graph(collection)

    # Construct cluster reply interaction graphs
    elif(GRAPH_CHOICE == 2):
        cluster_reply_graphs = cluster_reply_graphs(collection)

    # Construct general retweet interaction graph
    elif(GRAPH_CHOICE == 3):
        retweet_graph = general_retweet_graph(collection)

    # Construct cluster retweet interaction graphs
    elif(GRAPH_CHOICE == 4):
        cluster_retweet_graphs = cluster_retweet_graphs(collection)
