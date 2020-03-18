from utils import networking
from itertools import combinations

import pymongo
import networkx as nx
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
matplotlib.rcParams.update({'figure.autolayout': True})

def directed_triadic_census(graph, file_name, save_graphs):
    print("\nCalculating triadic census...")
    triadic_census = nx.triadic_census(graph)
    print("Done!\n")

    # There's probably a much more efficient way of doing this
    values = []
    labels = []
    print("A<-B->C triads: %d" % triadic_census["021D"])
    values.append(triadic_census["021D"])
    labels.append("A<-B->C")
    print("A->B<-C triads: %d" % triadic_census["021U"])
    # values.append(triadic_census["021U"])
    # labels.append("A->B<-C")
    print("A->B->C triads: %d" % triadic_census["021C"])
    values.append(triadic_census["021C"])
    labels.append("A->B->C")
    print("A<->B<-C triads: %d" % triadic_census["111D"])
    values.append(triadic_census["111D"])
    labels.append("A<->B<-C")
    print("A<->B->C triads: %d" % triadic_census["111U"])
    values.append(triadic_census["111U"])
    labels.append("A<->B->C")
    print("A->B<-C,A->C triads: %d" % triadic_census["030T"])
    values.append(triadic_census["030T"])
    labels.append("A->B<-C,A->C")
    print("A<-B<-C,A->C triads: %d" % triadic_census["030C"])
    values.append(triadic_census["030C"])
    labels.append("A<-B<-C,A->C")
    print("A<->B<->C triads: %d" % triadic_census["201"])
    values.append(triadic_census["201"])
    labels.append("A<->B<->C")
    print("A<-B->C,A<->C triads: %d" % triadic_census["120D"])
    values.append(triadic_census["120D"])
    labels.append("A<-B->C,A<->C")
    print("A->B<-C,A<->C triads: %d" % triadic_census["120U"])
    values.append(triadic_census["120U"])
    labels.append("A->B<-C,A<->C")
    print("A->B->C,A<->C triads: %d" % triadic_census["120C"])
    values.append(triadic_census["120C"])
    labels.append("A->B->C,A<->C")
    print("A->B<->C,A<->C triads: %d" % triadic_census["210"])
    values.append(triadic_census["210"])
    labels.append("A->B<->C,A<->C")
    print("A<->B<->C,A<->C triads: %d" % triadic_census["300"])
    values.append(triadic_census["300"])
    labels.append("A<->B<->C,A<->C")

    if(save_graphs == 1):
        plt.figure()
        plt.bar(range(len(values)), values, align='center', alpha=0.5)
        plt.xticks(range(len(labels)), labels, rotation=60)
        plt.savefig("graphs/"+file_name+".png")

def undirected_triadic_census(graph, file_name, save_graphs):
    print("\nCalculating triadic census...")
    triadic_census = {"A-B-C":0, "A-B-C,A-C":0}
    while(len(graph.nodes())>0):
        a = list(graph.nodes())[0]
        for b in graph.neighbors(a):
            for c in graph.neighbors(b):
                if c in graph.neighbors(a):
                    triadic_census["A-B-C,A-C"] += 1
                else:
                    triadic_census["A-B-C"] += 1
        graph.remove_node(a)
    print("Done!\n")

    values = []
    labels = []
    print("A-B-C triads: %d" % triadic_census["A-B-C"])
    values.append(triadic_census["A-B-C"])
    labels.append("A-B-C")
    print("A-B-C,A-C triads: %d" % triadic_census["A-B-C,A-C"])
    values.append(triadic_census["A-B-C,A-C"])
    labels.append("A-B-C,A-C")

    if(save_graphs == 1):
        plt.figure()
        plt.bar(range(len(values)), values, align='center', alpha=0.5)
        plt.xticks(range(len(labels)), labels, rotation=60)
        plt.savefig("graphs/"+file_name+".png")

if(len(sys.argv) - 1 < 3):
    print("Please run this program with arguments: network_analytics.py <Network_Type> <Save_Network> <Save_Graphs>")
    print("\n<Network_Type> choices:")
    print("1 - General Reply Interaction Graph")
    print("2 - Cluster Reply Interaction Graphs")
    print("3 - General Mention Interaction Graph")
    print("4 - Cluster Mention Interaction Graphs")
    print("5 - General Retweet Interaction Graph")
    print("6 - Cluster Retweet Interaction Graphs")
    print("7 - General Hashtag Co-occurence Graph")
    print("8 - Cluster Hashtag Co-occurence Graphs")
    print("\n<Save_Network> choices:")
    print("0 - Don't save networks")
    print("1 - Save networks as .pdf files in /graphs (WARNING: VERY TIME CONSUMING)")
    print("\n<Save_Graphs> choices:")
    print("0 - Don't save graphs")
    print("1 - Save graphs as .png files in /graphs")
else:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["WebScienceAssessment"]
    collection = db["tweets"]
    GRAPH_CHOICE = int(sys.argv[1])
    SAVE_NETWORKS = int(sys.argv[2])
    SAVE_GRAPHS = int(sys.argv[3])

    if(GRAPH_CHOICE in (1, 3, 5, 7)):
        if(GRAPH_CHOICE == 1):
            print("Network analytics for general reply graph.")
            print("-------------------------------------------\n")
            graph = networking.general_reply_graph(collection, SAVE_NETWORKS)
            file_name = "replies/general/general_reply_graph"
        elif(GRAPH_CHOICE == 3):
            print("Network analytics for general mention graph.")
            print("-------------------------------------------\n")
            graph = networking.general_mention_graph(collection, SAVE_NETWORKS)
            file_name = "mentions/general/general_mention_graph"
        elif(GRAPH_CHOICE == 5):
            print("Network analytics for general retweet graph.")
            print("-------------------------------------------\n")
            graph = networking.general_retweet_graph(collection, SAVE_NETWORKS)
            file_name = "retweets/general/general_retweet_graph"
        elif(GRAPH_CHOICE == 7):
            print("Network analytics for general hashtag graph.")
            print("-------------------------------------------\n")
            graph = networking.general_hashtag_graph(collection, SAVE_NETWORKS)
            file_name = "hashtags/general/general_hashtag_graph"

        print()
        print("Ties: %d" % graph.number_of_edges())

        if(GRAPH_CHOICE in (1, 3, 5)):
            directed_triadic_census(graph, file_name, SAVE_GRAPHS)
        elif(GRAPH_CHOICE == 7):
            undirected_triadic_census(graph, file_name, SAVE_GRAPHS)

    elif(GRAPH_CHOICE in (2, 4, 6, 8)):
        if(GRAPH_CHOICE == 2):
            print("Network analytics for cluster reply graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networking.cluster_reply_graphs(collection, SAVE_NETWORKS)
            file_name = "replies/clusters/cluster_reply_graph"
        elif(GRAPH_CHOICE == 4):
            print("Network analytics for cluster mention graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networking.cluster_mention_graphs(collection, SAVE_NETWORKS)
            file_name = "mentions/clusters/cluster_mention_graph"
        elif(GRAPH_CHOICE == 6):
            print("Network analytics for cluster retweet graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networking.cluster_retweet_graphs(collection, SAVE_NETWORKS)
            file_name = "retweets/clusters/cluster_retweet_graph"
        elif(GRAPH_CHOICE == 8):
            print("Network analytics for cluster hashtag graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networking.cluster_hashtag_graphs(collection, SAVE_NETWORKS)
            file_name = "hashtags/clusters/cluster_hashtag_graph"

        i = 0
        for graph in cluster_graphs:
            print("\n\nCluster %d:" % i)
            print()
            print("Ties: %d" % graph.number_of_edges())
            if(GRAPH_CHOICE in (2, 4, 6)):
                directed_triadic_census(graph, file_name+"_cluster_"+str(i), SAVE_GRAPHS)
            elif(GRAPH_CHOICE == 8):
                undirected_triadic_census(graph, file_name+"_cluster_"+str(i), SAVE_GRAPHS)
            i += 1
