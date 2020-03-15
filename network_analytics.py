from utils import networker
from itertools import combinations

import pymongo
import networkx as nx
import sys
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# https://stackoverflow.com/questions/20190520/listing-triads-in-a-multi-edge-graph
# http://www.analytictech.com/ucinet/help/hs4335.htm
# https://www.researchgate.net/figure/The-collection-of-all-triad-types-triad-census-The-labels-consist-of-three-digits-the_fig1_320707617
# https://stackoverflow.com/questions/54730863/how-to-get-triad-census-in-undirected-graph-using-networkx-in-python

def directed_triadic_census(graph, file_name):
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

    plt.bar(range(len(values)), values, align='center', alpha=0.5)
    plt.xticks(range(len(labels)), labels, rotation=60)
    plt.savefig("graphs/"+file_name+".png")

def undirected_triadic_census(graph):
    print("\nCalculating triadic census...")
    triadic_census = {}
    for nodes in combinations(graph.nodes, 3):
        n_edges = graph.subgraph(nodes).number_of_edges()
        triadic_census.setdefault(n_edges, []).append(nodes)
    print("Done!\n")
    if(1 in triadic_census):
        print("A-B,C triads: %d" % len(triadic_census[1]))
    else:
        print("A-B,C triads: %d" % 0)
    if(2 in triadic_census):
        print("A-B-C triads: %d" % len(triadic_census[2]))
    else:
        print("A-B-C triads: %d" % 0)
    if(3 in triadic_census):
        print("A-B-C,A-C triads: %d" % len(triadic_census[3]))
    else:
        print("A-B-C,A-C triads: %d" % 0)
    return triadic_census

if(len(sys.argv) - 1 < 1):
    print("Please run this program with arguments: network_analytics.py <Network_Type>")
    print("\n<Network_Type> choices:")
    print("1 - General Reply Interaction Graph")
    print("2 - Cluster Reply Interaction Graphs")
    print("3 - General Mention Interaction Graph")
    print("4 - Cluster Mention Interaction Graphs")
    print("5 - General Retweet Interaction Graph")
    print("6 - Cluster Retweet Interaction Graphs")
    print("7 - General Hashtag Co-occurence Graph")
    print("8 - Cluster Hashtag Co-occurence Graphs")
else:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["WebScienceAssessment"]
    collection = db["tweets"]
    GRAPH_CHOICE = int(sys.argv[1])

    if(GRAPH_CHOICE in (1, 3, 5, 7)):
        if(GRAPH_CHOICE == 1):
            print("Network analytics for general reply graph.")
            print("-------------------------------------------\n")
            graph = networker.general_reply_graph(collection)
            file_name = "general_reply_graph"
        elif(GRAPH_CHOICE == 3):
            print("Network analytics for general mention graph.")
            print("-------------------------------------------\n")
            graph = networker.general_mention_graph(collection)
        elif(GRAPH_CHOICE == 5):
            print("Network analytics for general retweet graph.")
            print("-------------------------------------------\n")
            graph = networker.general_retweet_graph(collection)
        elif(GRAPH_CHOICE == 7):
            print("Network analytics for general hashtag graph.")
            print("-------------------------------------------\n")
            graph = networker.general_hashtag_graph(collection)

        print()
        print("Ties: %d" % graph.number_of_edges())

        if(GRAPH_CHOICE in (1, 3, 5)):
            directed_triadic_census(graph, file_name)
        elif(GRAPH_CHOICE == 7):
            undirected_triadic_census(graph)

    elif(GRAPH_CHOICE in (2, 4, 6, 8)):
        if(GRAPH_CHOICE == 2):
            print("Network analytics for cluster reply graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networker.cluster_reply_graphs(collection)
        elif(GRAPH_CHOICE == 4):
            print("Network analytics for cluster mention graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networker.cluster_mention_graphs(collection)
        elif(GRAPH_CHOICE == 6):
            print("Network analytics for cluster retweet graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networker.cluster_retweet_graphs(collection)
        elif(GRAPH_CHOICE == 8):
            print("Network analytics for cluster hashtag graphs.")
            print("-------------------------------------------\n")
            cluster_graphs = networker.cluster_hashtag_graphs(collection)

        i = 0
        for graph in cluster_graphs:
            print("\n\nCluster %d." % i)
            print()
            print("Ties: %d" % graph.number_of_edges())
            if(GRAPH_CHOICE in (2, 4, 6)):
                directed_triadic_census(graph)
            elif(GRAPH_CHOICE == 8):
                undirected_triadic_census(graph)
            i += 1
