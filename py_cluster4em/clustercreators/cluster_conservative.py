import networkx as nx
import uuid
import json
from utils.data_validator import contains_columns, is_dataframe
from utils.preprocessor import prune_based_on_threshold, create_graph_from_matches


def cluster_conservative(matches_df, l_id, r_id, score, threshold, verbose_flag = True, output_file = None, serialization_factor = 10000):
    """
    Performs clustering in a conservative way such that nodes in the same maximal clique fall in the same cluster.

    Args:
        matches_df (DataFrame): the matches dataframe
        l_id (str): column name representing left id
        r_id (str): column name representing right id
        score (str): column name representing the match score between l_id and r_id
        threshold (float): threshold score above which to consider true matches
        verbose_flag (bool): display basic statistics about clusters
        output_file (str): name of the cluster output file
        serialization_factor (int): To preserve memory, output is appended to the output file after every
            "serialization_factor" number of clusters.

    Returns:
        Prepares dict of cluster_id vs list of ids in the cluster and,
        If the output_file is not described, returns the dict (mapping)
        If the output_file is given, dumps the dict to the file in json format
    """

    try:

        # validate if the supplied dataframe contains the mentioned columns
        if is_dataframe(matches_df) and contains_columns(matches_df, l_id, r_id, score):

            # remove the matches which have strength below the specified threshold
            matches_df = prune_based_on_threshold(matches_df, threshold, score)

            # build graph of matches
            G = create_graph_from_matches(matches_df, l_id, r_id, score)

            # conservative clustering logic
            map_clusters = {}
            max_cluster_size = 0

            if output_file is None:
                for c in nx.algorithms.clique.find_cliques(G):
                    key = str(uuid.uuid4())
                    map_clusters[key] = c
                    length_component = len(c)
                    max_cluster_size = max(max_cluster_size, length_component)
            else:
                count = 0
                with open(output_file, 'a') as file:
                    for c in nx.algorithms.clique.find_cliques(G):
                        key = str(uuid.uuid4())
                        map_clusters[key] = c
                        length_component = len(c)
                        count += 1
                        max_cluster_size = max(max_cluster_size, length_component)
                        # Periodically, serialize the cluster mapping to disk to reduce memory utilization.
                        if count % serialization_factor == 0:
                            file.write(json.dumps(map_clusters))
                            if verbose_flag:
                                print('Written till ', str(count), 'to ', output_file)
                            # dereference map_clusters and do garbage collection to free up memory
                            map_clusters = {}
                            gc.collect()
                    # Serialize the last remaining clusters to the output file in json format.
                    file.write(json.dumps(map_clusters))
                    if verbose_flag:
                        print('Written last ', str(len(map_clusters)), 'to ', output_file)

            if verbose_flag:
                # Printing the clusterId vs clusters
                for key, value in map_clusters.items():
                    print(key, ': ', value)
                # Printing some statistics - Should we keep them and store somewhere?
                print('Number of clusters: ', count)
                print('Max cluster size: ' + str(max_cluster_size))

            if output_file is None:
                return map_clusters
            else:
                # Serialization already happened
                return None

    except NameError as exp:
        raise
    except TypeError as exp:
        raise
    except Exception as exp:
        # log if necessary
        raise  # bare raise - preserves the stack trace