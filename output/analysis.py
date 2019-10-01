# Project: League Strength
# Description: Analyze prediction results and calculate league strength metric
# Data Sources: RealGM
# Last Updated: 9/27/2019

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import imgkit

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
    sns.distplot(df[df['LEAGUE']==league1]['PREDICTION'], color='#30a2da', label=league1.replace('_', ' '))
    sns.distplot(df[df['LEAGUE']==league2]['PREDICTION'], color='#fc4f30', label=league2.replace('_', ' '))
    ax.set_xlim(-10, 10)
    ax.set_xlabel('Predicted Win Share')
    ax.set_yticks([])
    ax.legend()
    plt.title('Comparison of Predicted WS Between Leagues')
    plt.tight_layout()
    plt.show()

def ranking_table(df):
    """
    Create table of median predicted WS by league providing a ranking of
    overall strength to compare across leagues.

    Args:
        df (DataFrame): Dataframe containing all player/season predictions.

    Returns:
        None
    """
    # Aggregate player/season WS prediction to league-level, calculate median
    # prediction for each league and sort by overall league value.
    # Style pandas dataframe and save output for documentation.
    ranking = (df.groupby('LEAGUE')
                 .median()['PREDICTION']
                 .sort_values(ascending=False)
                 .reset_index()
                 .round(3)
                 .style
                 .set_table_styles(
                     [{'selector': 'tr:nth-of-type(odd)',
                       'props': [('background', '#eee')]},
                      {'selector': 'tr:nth-of-type(even)',
                       'props': [('background', 'white')]},
                      {'selector':'th, td', 'props':[('text-align', 'center')]}])
                .set_properties(subset=['LEAGUE'], **{'text-align': 'left'})
                .hide_index())
    html = ranking.render()
    imgkit.from_string(html, 'plots/ranking.png', {'width': 1})


if __name__=='__main__':
    # Read in prediction dataframe
    predictions_df = pd.read_csv('../data/predictions/predictions.csv')
    # Plot distribution of predictions between two leagues
    plot_distributions(predictions_df, 'NBA', 'NBA_PLAYOFFS') # South Korean KBL

    # Aggregate predictions to the league level to compare median prediciton
    # as a quick sanity check on league strength ranking.
    ranking_table(predictions_df)
