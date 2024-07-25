#!/usr/bin/env python

import argparse
import concurrent.futures
import pandas as pd
from scipy.spatial.distance import braycurtis 


def calculate(index_list):
    feature_i = list(PROFILE_DF.loc[:, index_list[0]])
    feature_j = list(PROFILE_DF.loc[:, index_list[1]])
    bc = braycurtis(feature_i, feature_j) 
    return index_list + [ bc ]
 

def calculate_bray_curtis_dist(input_file, output_file, threads):
    global PROFILE_DF
    PROFILE_DF = pd.read_csv(input_file, low_memory=False, index_col=[0])

    dist_list = []
    index_list = []

    columns = list(PROFILE_DF.columns)
    for i in range(0, len(columns)):
        for j in range(i, len(columns)):
            subject_i = columns[i]
            subject_j = columns[j]
            index_pair = [subject_i, subject_j]
            index_list.append(index_pair)

    print(f"total of {len(index_list)} samples pairs")

    with concurrent.futures.ProcessPoolExecutor(max_workers=threads) as executor:
        for dist_res in executor.map(calculate, index_list):
            dist_list.append(dist_res)

    dist_df = pd.DataFrame(dist_list, columns=["subject_i", "subject_j", "bray_curtis_distance"])
    dist_df.to_csv(output_file, sep="\t", index=False)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate Bray-Curtis distance from feature profile"
    ) 
    parser.add_argument(
        "--profile",
        type=str,
        help="input profile, rowname is feature, colname is subject, format: csv"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Bray-Curtis distance matrix for each subject"
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=32,
        help="Threads"
    )
    args = parser.parse_args()
    calculate_bray_curtis_dist(args.profile, args.output, args.threads)


if __name__ == "__main__":
    main()
