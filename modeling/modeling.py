# Project: League Strength
# Description: Create model to project players into the NBA
# Data Sources: RealGM
# Last Updated: 9/26/2019

import numpy as np
import pandas as pd
import glob

def create_feature_matrix(save=False):
    """
    Combine all individual league data into one feature matrix.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.
    Returns:
        combined_data (DataFrame): Per 48 Minute Pace-Adjusted statistics between
        2009-2010 and 2018-2019 seasons for all leagues on RealGM.
    """
    # Set path to parent directory of individual league data
    path = '../data/leagues'
    # Extract all league data paths
    all_files = glob.glob(path + "/*.csv")
    # Instantiate placeholder list to append individual dataframes to
    df_list = []
    # Loop through individual league data and append to df_list
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        df_list.append(df)
    # Combine all league dataframes into one
    combined_data = pd.concat(df_list, axis=0, ignore_index=True)
    # If the function parameter of save is set to TRUE then save the resulting
    # dataframe to a .csv file
    if save:
        combined_data.to_csv('../data/combined_data/combined_data.csv', index=False)
    else:
        pass
    return combined_data


if __name__=='__main__':
    # Combine and save all individual league data
    # combined_data = create_feature_matrix(save=True)
    # If the above line has already been run then that combined dataframe
    # can be read in via:
    combined_data = pd.read_csv('../data/combined_data/combined_data.csv')
