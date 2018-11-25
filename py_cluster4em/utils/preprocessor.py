import networkx as nx

def prune_based_on_threshold(matches_df, threshold, score):
    """
    Keeps only records whose score > threshold supplied.

    Args:
        matches_df (DataFrame): the matches dataframe
        threshold (float): threshold score above which to consider true matches

    Returns:
        matches_df (DataFrame): the matches dataframe after pruning

    Notes:
        This is an exposed helper function that is used by the implemented clustering approaches.
        This can also be used for a custom clustering implementation at user's will.
    """
    # type cast
    matches_df[[score]] = matches_df[[score]].astype(float)
    # prune
    matches_df = matches_df[matches_df[score] > threshold]
    return matches_df

def create_graph_from_matches(matches_df, l_id, r_id, score):
    """
    Builds the graph of matches, each edge representing a match

    Args:
        matches_df (DataFrame): the matches dataframe
        l_id (str): column name representing left id
        r_id (str): column name representing right id
        score (str): column name representing the match score between l_id and r_id

    Returns:
        Undirected Graph (nx.Graph)

    Notes:
        This is an exposed helper function that is used by the implemented clustering approaches.
        This can also be used for a custom clustering implementation at user's will.
    """
    G = nx.Graph()
    # addition of 1 to account for the index column
    l_id_idx = matches_df.columns.get_loc(l_id) + 1
    r_id_idx = matches_df.columns.get_loc(r_id) + 1
    score_idx = matches_df.columns.get_loc(score) + 1
    for row in matches_df.itertuples():
        G.add_edge(row[l_id_idx], row[r_id_idx], weight = row[score_idx])
    return G