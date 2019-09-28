# Project: League Strength
# Description: Scrape Per 48 Minute (Pace Adjusted) statistics for all
# leagues between 2009-2010 and 2018-2019 seasons.
# Data Sources: RealGM
# Last Updated: 9/26/2019

import numpy as np
import pandas as pd
from time import sleep

def scraper(league, save=False):
    """
    Scrape Per 48 Pace-Adjusted statistics between the 2009-2010 and 2018-2019
    seasons for a specified league from RealGM.

    Args:
        league (str): Name of league to scrape. To view all league names from
                    RealGM open `League_Strength/data/url_mapping/url_mapping.csv`
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.
    Returns:
        df (DataFrame): Per 48 Minute Pace-Adjusted statistics between 2009-2010
        and 2018-2019 seasons for a specified league.
    """
    # Read in mapping table containing league names and urls from RealGM
    url_mapping = pd.read_csv('../data/url_mapping/url_mapping.csv',
                                usecols = ['LEAGUE', 'URL_NUMBER'])
    # Transform mapping table into dictionary to index into during scraping
    #p rocess
    url_dict = dict(zip(url_mapping['LEAGUE'], url_mapping['URL_NUMBER']))
    # Instantiate placeholder dataframe on which to append data to in season and
    # page for-loop
    df = pd.DataFrame()
    # Loop through all seasons between 2009-2010 and 2018-2019
    for season in np.arange(2010, 2020):
        # Loop through all pages on the season webpage
        for page in np.arange(1, 100):
            # Random sleep timer to avoid being throttled by RealGM
            sleep(np.random.randint(5, 10))
            # Try/Except to break when looping through pages runs out of
            # existing pages to loop through
            try:
                # If the input league is 'nba' use the following url
                if league == 'nba':
                    # Set specific url to the correct league, season, and page
                    # in the loop



                    url = 'https://basketball.realgm.com/{0}/stats/{1}/Per_48/All/points/All/asc/{2}/Regular_Season?pace_adjustment='.format(league, season, page)
                    # Extract the table from the raw html
                    table = pd.read_html(url)[0]
                    # Create a new column with the season
                    table['SEASON'] = season
                    # Create a new column with the league name
                    table['LEAGUE'] = 'NBA'
                    # Append the dataframe within the loop to the placeholder
                    # dataframe that contains all seasons and pages
                    df = df.append(table, sort=False)
                # If the input league does not equal 'nba' use the following
                # international url.
                else:
                    url = 'https://basketball.realgm.com/international/league/{0}/{1}/stats/{2}/Per_48/All/All/points/All/desc/{3}?pace_adjustment='.format(url_dict[league], league.replace(' ', '-'), season, page)
                    table = pd.read_html(url)[0]
                    table['SEASON'] = season
                    table['LEAGUE'] = league
                    df = df.append(table, sort=False)
            except:
                break
    # If the function parameter of save is set to TRUE then save the resulting
    # dataframe to a .csv file in the `data/leagues` directory under the
    # individual team name.
    if save:
        df.to_csv('../data/leagues/{0}.csv'.format(league), index=False)
    else:
        pass
    return df

def scrape_targets(save=False):
    """
    Scrape Advanced statistics between the 2009-2010 and 2018-2019
    seasons for all NBA players to use as targets in subsequent modeling step.

    Args:
        save (bool): Indicates whether to write resulting pandas DataFrame to
                     .csv file. Defaults to False.
    Returns:
        df (DataFrame): Advanced statistics between 2009-2010
        and 2018-2019 seasons for all NBA players.
    """
    df = pd.DataFrame()
    # Loop through all seasons between 2009-2010 and 2018-2019
    for season in np.arange(2010, 2020):
        # Loop through all pages on the season webpage
        for page in np.arange(1, 100):
            # Random sleep timer to avoid being throttled by RealGM
            sleep(np.random.randint(5, 10))
            # Try/Except to break when looping through pages runs out of
            # existing pages to loop through
            try:
                # Set specific url to the correct season, and page
                # in the loop
                url = 'https://basketball.realgm.com/nba/stats/{0}/Misc_Stats/All/per/All/asc/{1}/Regular_Season?pace_adjustment='.format(season, page)
                # Extract the table from the raw html
                table = pd.read_html(url)[0]
                # Create a new column with the season
                table['SEASON'] = season
                # Create a new column with the league name
                table['LEAGUE'] = 'NBA'
                # Append the dataframe within the loop to the placeholder
                # dataframe that contains all seasons and pages
                df = df.append(table, sort=False)
            except:
                break
    # If the function parameter of save is set to TRUE then save the resulting
    # dataframe to a .csv file in the `data/targets` directory
    if save:
        df.to_csv('../data/targets/targets.csv', index=False)
    else:
        pass
    return df

if __name__=='__main__':
    # Read in the mapping table with all league names from RealGM
    url_mapping = pd.read_csv('../data/url_mapping/url_mapping.csv')
    # Extract list of league names from mapping table
    leagues = url_mapping['LEAGUE'].unique()
    # Loop through mapping table, saving each league to it's own individual
    # .csv file in the `data/leagues` directory.
    for league in leagues:
        out_df = scraper(league, True)
    # Scrape Targets (Advanced NBA MEtrics)
    targets_df = scrape_targets(save=True)
