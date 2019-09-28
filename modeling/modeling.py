# Project: League Strength
# Description: Create model to project players into the NBA
# Data Sources: RealGM
# Last Updated: 9/27/2019

import numpy as np
import pandas as pd
import glob
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Lasso, Ridge, ElasticNet

def join_league_data(save=False):
    """
    Combine all individual league data into one dataframe .

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

def create_feature_matrix():
    """
    Join target variable (NBA WS from Season+1) with current-season predictors.
    Output will be used as feature matrix for model training.

    Args:
        None

    Returns:
        feature matrix (DataFrame): Dataframe containing predictors and targets
        for model training.
    """
    # Read in Per 48-Minutes Pace-Adjusted player/season data from all
    # leagues as well as targets (Win Shares) for NBA player/season records.
    combined_data = pd.read_csv('../data/combined_data/combined_data.csv')
    targets = pd.read_csv('../data/targets/targets.csv')
    # Create TARGET_SEASON to identify the season with which the target variable
    # (WS) is associated. The feature SEASON is then lagged by one season and is
    # associated with all predictor variables.
    targets['TARGET_SEASON'] = targets['SEASON']
    targets['SEASON'] = targets['SEASON'] - 1
    targets = targets[['Player', 'TARGET_SEASON', 'SEASON', 'WS']]
    # Inner join cominbed data and targets
    feature_matrix = pd.merge(targets, combined_data, on=['Player', 'SEASON'])
    feature_matrix = feature_matrix[['Player', 'TARGET_SEASON', 'SEASON', 'LEAGUE',
                                    'GP', 'MIN', 'FGM', 'FGA', 'FG%', '3PM', '3PA',
                                    '3P%', 'FTM', 'FTA', 'FT%', 'TOV', 'PF', 'ORB',
                                    'DRB', 'REB', 'AST', 'STL', 'BLK', 'PTS', 'WS']]
    return feature_matrix



if __name__=='__main__':
    # Combine and save all individual league data
    # combined_data = join_league_data(save=True)

    # Create feature matrix containing target and predictors
    # Filter MP and GP in training data
    feature_matrix = create_feature_matrix()
    feature_matrix = feature_matrix[(feature_matrix['MIN']>=15) &
                                    (feature_matrix['GP']>=10)]

    # Perform train/test split
    y = feature_matrix.pop('WS')
    X = feature_matrix[['GP', 'MIN', 'FGM', 'FGA', 'FG%', '3PM', '3PA',
                        '3P%', 'FTM', 'FTA', 'FT%', 'TOV', 'PF', 'ORB',
                        'DRB', 'REB', 'AST', 'STL', 'BLK', 'PTS']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)

    # Build Pipeline to pass to gridsearch for modeling.
    # This includes a data scaling step as well as the ridge regression model.
    pipeline = Pipeline([
    ('std_scaler', StandardScaler()),
    ('ridge_model', Ridge())
    ])

    # Define parameter list to gridsearch over
    ridge_param_list = {'ridge_model__alpha': np.linspace(.1, 1, 10),
                        'ridge_model__solver': ['auto', 'svd', 'lsqr', 'cholesky']}
    # Gridsearch on entire pipeline to optimixe model parameters.
    grid = GridSearchCV(pipeline, param_grid=ridge_param_list,
                                  scoring='neg_mean_squared_error',
                                  cv=3,
                                  n_jobs=-1)
    # Fit model with training data.
    grid.fit(X_train, y_train)

    # Make predictions on test set
    # Evaluate model using RMSE of final test set
    y_pred = grid.predict(X_test)
    print('Final Model RMSE: ', np.sqrt(mean_squared_error(y_test, y_pred)))

    # Using resulting model from the step above, make predictions for all
    # current NBA and international players after filtering to a certain
    # MP and GP threshold.
    combined_data = pd.read_csv('../data/combined_data/combined_data.csv')
    combined_data = combined_data[(combined_data['MIN']>=15) &
                                  (combined_data['GP']>=10)]
    combined_data = combined_data[['GP', 'MIN', 'FGM', 'FGA', 'FG%', '3PM', '3PA',
                        '3P%', 'FTM', 'FTA', 'FT%', 'TOV', 'PF', 'ORB',
                        'DRB', 'REB', 'AST', 'STL', 'BLK', 'PTS']]
    all_predictions = grid.predict(combined_data)
    combined_data['PREDICTION'] = all_predictions
    combined_data = combined_data[['Player', 'SEASON', 'LEAGUE', 'PREDICTION']]
    combined_data.to_csv('../data/predictions/predictions.csv', index=False)

    # Aggregate predictions to the league level to compare median prediciton
    # as a quick sanity check on league strength ranking.
    ranking = (combined_data.groupby('LEAGUE')
                            .median()['PREDICTION']
                            .sort_values(ascending=False))
