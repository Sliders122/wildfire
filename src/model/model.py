import numpy as np
import modelize as mz
import rasterio
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
from shapely.geometry import mapping
import pyproj
import pandas as pd
import sklearn as skl
from imblearn.under_sampling import RandomUnderSampler
from lightgbm import LGBMClassifier
from matplotlib.widgets import Cursor
from matplotlib import animation
import datetime
import pickle
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

if __name__ == "__main__":

    # Create a path to the data directory
    path_data = "../dataframe/"

    # open the csv file with the data
    df = pd.read_csv(path_data + "df_final.csv", parse_dates=["time"])

    # get the correlation matrix and plot it
    mz.get_correlation_matrix(df)
    
    # First, define the models we want to use
    # We use the default parameters for each model
    # We use the same random state for each model to be able to compare them
    # We use the class_weight parameter to balance the classes
    # We use the max_iter parameter to avoid convergence warnings
    # We use the n_estimators parameter to avoid convergence warnings
    # We use the max_depth parameter to avoid convergence warnings
    # We use the l1_ratio parameter to avoid convergence warnings
    
    # Linear regression, k nearest neighbors, random forest, xgboost, lightgbm 
    model_LR = skl.linear_model.LogisticRegression(C=0.05, l1_ratio=None, max_iter=10000)
    model_KNN = skl.neighbors.KNeighborsClassifier()
    model_RF = skl.ensemble.RandomForestClassifier(n_estimators=100, max_depth=2)
    model_XGB = XGBClassifier(n_estimators=100, max_depth=2, use_label_encoder=False, eval_metric='logloss')
    model_LGBM = LGBMClassifier(n_estimators=100, max_depth=2)

    # put all those models in a list
    models = [model_LR, model_KNN, model_RF, model_XGB, model_LGBM]

    # Run the cross validation for each models the for combinatotions of stratified and shuffle 
    #stratified = True, shuffle = True
    results_stratified_shuffle = mz.cross_validation(models, df, n_splits=10, random_state=71, 
                                                                stratified=True, shuffle=True)
    # stratified = True, shuffle = False
    results_stratified_noshuffle = mz.cross_validation(models, df, n_splits=10, random_state=71,
                                                                stratified=True, shuffle=False)
    # stratified = False, shuffle = True
    results_nostatified_shuffle = mz.cross_validation(models, df, n_splits=10, random_state=71, 
                                                                stratified=False, shuffle=True)
    # stratified = False, shuffle = False
    results_nostatified_noshuffle = mz.cross_validation(models, df, n_splits=10, random_state=71, 
                                                                stratified=False, shuffle=False) 
    print('Stratified and shuffle')
    print(results_stratified_shuffle)

    print('Stratified and no shuffle')
    print(results_stratified_noshuffle)
    
    print('No stratified and shuffle')
    print(results_nostatified_shuffle)

    print('No stratified and no shuffle')
    print(results_nostatified_noshuffle)
    

    # Split the data into train on 2010 to 2017 and test on 2018 to 2020
    df = pd.read_csv(path_data + "df_final.csv", parse_dates=["time"])
    # Split the data into train and test
    df_train = df[df["time"] < "2018-01-01"]
    df_test = df[df["time"] >= "2018-01-01"]

    # fit a lgmb model
    lgbm_model = mz.fit_lgbm_model(df_train, n_estimators=100, max_depth=2)

    # generate the pickle file
    pickle.dump(lgbm_model, open('model_lgbm.pkl', 'wb'))

    # predict the model
    df_pred = mz.predict_lgbm_model(df_test, lgbm_model)

    # Compute the metrics
    results = mz.plot_metrics(lgbm_model, df_test['FireMask'], df_pred['FireMask'])

    # reset the index
    df_pred.reset_index(inplace=True, drop=False)
    df_test.reset_index(inplace=True, drop=False)

    # drop time and FireMask from the pred dataframe
    df_pred.drop(['time','FireMask'], axis=1, inplace=True)

    # merge the pred dataframe with the test dataframe
    df_model = pd.merge(df_test, df_pred, on='index', how='left')

    # save the dataframe to csv
    df_model.to_csv("df_model.csv", index=False)

    