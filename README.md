# py_cluster4em
py_cluster4em is a Python package for performing clustering. 
It provides different clustering approaches that you could take to generate clusters out of a matches file. 

As an example, you could output clusters out of the below given matches file sample:\
*insert example here*

## Usage:
You could call the script as follows:\
```python py_cluster4em.py matches.csv left_id_column_name right_id_column_name match_score threshold_score output_liberal.json output_conservative.json```\
where all of the below arguments are required.
* matches.csv: Name of the csv file containing the matches.
* left_id_column_name: Name of the column containing the left side of the matching ids.
* right_id_column_name: Name of the column containing the right side of the matching ids.
* match_score: Name of the column containing the score representing the strength of the match between left column and the right column just specified.
* threshold_score: Represents the threshold score. Only matches having score greater than this threshold will be considered as actual matches.
* output_liberal.json, output_conservative.json: File names to store the output of liberal and conservative approaches respectively.

## Types of clustering approaches supported:
All clustering approaches assume a graph representation of matches where nodes are the different ids and the labelled edges represent a match between the two with a certain score.

1. Liberal Clustering: Generates the clusters out of the connected components in the matches graph.

2. Conservative Clustering: Generates the clusters out of the maximal cliques in the matches graph.



