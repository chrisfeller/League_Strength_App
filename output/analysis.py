# Project: League Strength
# Description: Analyze prediction results and calculate league strength metric
# Data Sources: RealGM
# Last Updated: 9/27/2019

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Plotting Style
plt.style.use('fivethirtyeight')

def plot_distributions(df, league1, league2):
    """
    Plot the distribution of all player/season predictions between two leagues.

    Args:
        df (DataFrame): Dataframe containing all player/season predictions.
        league1 (str): First league to use in comparison. For list of league
                       names, open `url_mapping.csv` in `data/url_mapping/`
        league2 (str): Second league to use in comparison.

    Returns:
        None
    """
    fig, ax = plt.subplots(figsize=(18, 5))
    sns.distplot(df[df['LEAGUE']==league1]['Prediction'], color='#30a2da', label=league1.replace('_', ' '))
    sns.distplot(df[df['LEAGUE']==league2]['Prediction'], color='#fc4f30', label=league2.replace('_', ' '))
    ax.set_xlim(-10, 10)
    ax.set_xlabel('Predicted Win Share')
    ax.set_yticks([])
    ax.legend()
    plt.title('Comparison of Predicted WS Between Leagues')
    plt.tight_layout()
    plt.show()


if __name__=='__main__':
    # Read in prediction dataframe
    predictions_df = pd.read_csv('../data/predictions/predictions.csv')
    # Plot distribution of predictions between two leagues
    plot_distributions(predictions_df, 'South Korean KBL', 'NBA_PLAYOFFS')
