# py_cluster4em
py_cluster4em is a Python package for performing clustering. 
It provides different clustering approaches that you could take to generate clusters out of matches.


## Types of clustering approaches supported
All clustering approaches assume a graph representation of matches where nodes are the different ids and the labelled edges represent a match between the two with a certain score.

1. Liberal Clustering: Generates the clusters out of the connected components in the matches graph.

2. Conservative Clustering: Generates the clusters out of the maximal cliques in the matches graph.

## Usage
Given a matches dataframe(native or after loading from a csv using pandas) with the following columns/attributes: 
* left_id_column_name: Name of the column containing the left side of the matching ids.
* right_id_column_name: Name of the column containing the right side of the matching ids.
* match_score: Name of the column containing the score representing the strength of the match between left column and the right column just specified.

You could use one of the two supported approaches from: 
* py_cluster4em/py_cluster4em/clustercreators/cluster_conservative.py
* py_cluster4em/py_cluster4em/clustercreators/cluster_liberal.py 

As mentioned in their respective docstrings, you'll need to pass in one more required argument:
* threshold_score: Represents the threshold score. Only matches having score greater than this threshold will be considered as actual matches.

Example: \
(As also specified in the file py_cluster4em/py_cluster4em/clustercreators/py_cluster4em.py)

```
# Reading file
import pandas as pd
M = pd.read_csv(input_file, usecols=[l_id, r_id, score])

# Just for testing - so taking smaller dataset
M = M.head(40)

from clustercreators.cluster_conservative import cluster_conservative
from clustercreators.cluster_liberal import cluster_liberal

cluster_liberal(M, l_id, r_id, score, threshold)
cluster_conservative(M, l_id, r_id, score, threshold)
```


## Dependencies
The required dependencies to build the packages are: 
* pandas (provides data structures to store and manage tables). Tested on version 0.22.0.
* networkx (provides implementations for graph based algorithms). Tested on version 2.1.

## Platforms
py_cluster4em has been tested only on Windows at the moment.

