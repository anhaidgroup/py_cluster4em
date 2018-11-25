import sys
import pandas as pd


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
output_file_conservative = sys.argv[7]

# Reading file
M = pd.read_csv(input_file, usecols=[l_id, r_id, score])

# Just for testing - so taking smaller dataset
M = M.head(40)

from clustercreators.cluster_conservative import cluster_conservative
from clustercreators.cluster_liberal import cluster_liberal

cluster_liberal(M, l_id, r_id, score, threshold, output_file=output_file_liberal)
cluster_conservative(M, l_id, r_id, score, threshold, output_file=output_file_conservative)