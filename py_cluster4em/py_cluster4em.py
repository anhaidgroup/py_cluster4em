import sys
import pandas as pd
import networkx as nx
import uuid
import gc
import json

def create_graph_from_matches(M, l_id, r_id, score):
    """
    Builds the graph of matches, each edge representing a match

    Args:
        M (DataFrame): Matches dataframe
        l_id (str): column name representing left id
        r_id (str): column name representing right id
        score (str): column name representing the match score between l_id and r_id

    Returns: Undirected Graph (nx.Graph)
    """
    G = nx.Graph()
    # addition of 1 to account for the index column
    l_id_idx = M.columns.get_loc(l_id) + 1
    r_id_idx = M.columns.get_loc(r_id) + 1
    score_idx = M.columns.get_loc(score) + 1
    for row in M.itertuples():
        G.add_edge(row[l_id_idx], row[r_id_idx], weight = row[score_idx])
    return G

def liberal_clustering(G, output_file):
    """
    Performs clustering in a liberal way such that nodes in the same connected component fall in the same cluster.
    Dumps the clusters into the output file in a json format.

    Args:
        G (nx.Graph): Graph of matches
        output_file (str): name of the cluster output file

    Returns: Void
    """
    cc = nx.connected_components(G)
    map_clusters = {}
    maxClusterSize = 0
    for component in cc:
        key = str(uuid.uuid4())
        map_clusters[key] = list(component)
        length_component = len(component)
        maxClusterSize = max(maxClusterSize, length_component)

    # Serialize the clusters to the output file in json format.
    with open(output_file, 'w') as file:
        file.write(json.dumps(map_clusters))

    # Printing the clusterId vs clusters
    for key, value in map_clusters.items():
        print(key, ': ', value)
    # Printing some statistics - Should we keep them and store somewhere?
    print('Number of clusters: ' + str(len(map_clusters)))
    print('Max cluster size: ' + str(maxClusterSize))


def conservative_clustering(G, output_file, serialization_factor):
    """
    Performs clustering in a conservative way such that nodes in the same maximal clique fall in the same cluster.
    Dumps the clusters into the output file in a json format.

    Args:
        G (nx.Graph): Graph of matches
        output_file (str): name of the cluster output file
        serialization_factor (int): To preserve memory, output is appended to the output file after every
            "serialization_factor" number of clusters.

    Returns: Void
    """
    count = 0
    map_clusters = {}
    maxClusterSize = 0
    with open(output_file, 'a') as file:
        for c in nx.algorithms.clique.find_cliques(G):
            key = str(uuid.uuid4())
            map_clusters[key] = c
            length_component = len(c)
            count += 1
            maxClusterSize = max(maxClusterSize, length_component)
            # Periodically, serialize the cluster mapping to disk to reduce memory utilization.
            if count % serialization_factor == 0:
                file.write(json.dumps(map_clusters))
                print('Written till ', str(count), 'to ', output_file)
                # dereference map_clusters and do garbage collection to free up memory
                map_clusters = {}
                gc.collect()
        # Serialize the last remaining clusters to the output file in json format.
        file.write(json.dumps(map_clusters))

    # Printing the clusterId vs clusters
    for key, value in map_clusters.items():
        print(key, ': ', value)
    # Printing some statistics - Should we keep them and store somewhere?
    print('Number of clusters: ', count)
    print('Max cluster size: ' + str(maxClusterSize))

# Reading in arguments
if len(sys.argv) != 8:
    print("7 Arguments expected in call")
    exit(1)
input_file = sys.argv[1]
l_id = sys.argv[2]
r_id = sys.argv[3]
score = sys.argv[4]
threshold = float(sys.argv[5])
output_file_liberal = sys.argv[6]
output_file_conservative = sys.argv[6]

# Reading file
M = pd.read_csv(input_file, usecols=[l_id, r_id, score])

# Pruning based on threshold
M[[score]] = M[[score]].astype(float)
M = M[M[score] > threshold]

# Create graph from matches
G = create_graph_from_matches(M, l_id, r_id, score)

# Perform liberal clustering
print('Liberal Approach Clusters: ')
liberal_clustering(G, output_file_liberal)

# Perform conservative clustering
print('Conservative Approach Clusters: ')
serialization_factor = 10000 # should we bring this in too from the user?
conservative_clustering(G, output_file_conservative, serialization_factor)

