import networkx as nx
import uuid
import json
from utils.data_validator import contains_columns, is_dataframe
from utils.preprocessor import prune_based_on_threshold, create_graph_from_matches

def cluster_liberal(matches_df, l_id, r_id, score, threshold, verbose_flag = True, output_file = None):
    """
    Performs clustering in a liberal way such that nodes in the same connected component fall in the same cluster.

    Args:
        matches_df (DataFrame): the matches dataframe
        l_id (str): column name representing left id
        r_id (str): column name representing right id
        score (str): column name representing the match score between l_id and r_id
        threshold (float): threshold score above which to consider true matches
        verbose_flag (bool): display basic statistics about clusters
        output_file (str): name of the cluster output file


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

            # liberal clustering logic
            cc = nx.connected_components(G)
            map_clusters = {}
            maxClusterSize = 0
            for component in cc:
                key = str(uuid.uuid4())
                map_clusters[key] = list(component)
                length_component = len(component)
                maxClusterSize = max(maxClusterSize, length_component)

            if verbose_flag:
                # Printing the clusterId vs clusters
                for key, value in map_clusters.items():
                    print(key, ': ', value)
                # Printing some statistics - Should we keep them and store somewhere?
                print('Number of clusters: ' + str(len(map_clusters)))
                print('Max cluster size: ' + str(maxClusterSize))

            if output_file is None:
                return map_clusters
            else:
                # Serialize the clusters to the output file in json format.
                with open(output_file, 'w') as file:
                    file.write(json.dumps(map_clusters))
                return None

    except NameError as exp:
        raise
    except TypeError as exp:
        raise
    except Exception as exp:
        # log if necessary
        raise  # bare raise - preserves the stack trace