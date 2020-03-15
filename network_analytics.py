from utils import networker
from itertools import combinations

import pymongo
import networkx as nx
import sys

# https://stackoverflow.com/questions/20190520/listing-triads-in-a-multi-edge-graph
# http://www.analytictech.com/ucinet/help/hs4335.htm
# https://www.researchgate.net/figure/The-collection-of-all-triad-types-triad-census-The-labels-consist-of-three-digits-the_fig1_320707617
# https://stackoverflow.com/questions/54730863/how-to-get-triad-census-in-undirected-graph-using-networkx-in-python

def directed_triadic_census(graph):
    print("\nCalculating triadic census...")
    triadic_census = nx.triadic_census(graph)
    print("Done!\n")
    print("A<-B->C triads: %d" % triadic_census["021D"])
    print("A->B<-C triads: %d" % triadic_census["021U"])
    print("A->B->C triads: %d" % triadic_census["021C"])
    print("A<->B<-C triads: %d" % triadic_census["111D"])
    print("A<->B->C triads: %d" % triadic_census["111U"])
    print("A->B<-C,A->C triads: %d" % triadic_census["030T"])
    print("A<-B<-C,A->C triads: %d" % triadic_census["030C"])
    print("A<->B<->C triads: %d" % triadic_census["201"])
    print("A<-B->C,A<->C triads: %d" % triadic_census["120D"])
    print("A->B<-C,A<->C triads: %d" % triadic_census["120U"])
    print("A->B->C,A<->C triads: %d" % triadic_census["120C"])
    print("A->B<->C,A<->C triads: %d" % triadic_census["210"])
    print("A<->B<->C,A<->C triads: %d" % triadic_census["300"])

def undirected_triadic_census(graph):
    print("\nCalculating triadic census...")
    triad_class = {}
    for nodes in combinations(graph.nodes, 3):
        n_edges = graph.subgraph(nodes).number_of_edges()
        triad_class.setdefault(n_edges, []).append(nodes)
    print("Done!\n")
    print(triad_class)

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
            directed_triadic_census(graph)
        elif(GRAPH_CHOICE == 7):
            undirected_triadic_census(graph)

    elif(GRAPH_CHOICE in (2, 4, 6, 8)):
        if(GRAPH_CHOICE == 2):
            cluster_reply_graphs = networker.cluster_reply_graphs(collection)
        elif(GRAPH_CHOICE == 4):
            cluster_mention_graphs = networker.cluster_mention_graphs(collection)
        elif(GRAPH_CHOICE == 6):
            cluster_retweet_graphs = networker.cluster_retweet_graphs(collection)
        elif(GRAPH_CHOICE == 8):
            cluster_hashtag_graphs = networker.cluster_hashtag_graphs(collection)
