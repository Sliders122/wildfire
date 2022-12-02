import numpy as np
import rasterio
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
import harmonize as hz
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report
import datetime


# Create a path to the data directory
path_data = "C:/Users/luigi/OneDrive - Data ScienceTech Institute/Projet_PML/dataset/"

# open the csv file with the data
df = pd.read_csv(path_data + "df_final.csv")

# define a function to get the correlation matrix and plot it
def get_correlation_matrix(the_df, target_var='FireMask'):
    """
    This function returns the correlation matrix of the dataframe
    input:
        the_df: the dataframe
    output:
        the correlation matrix
    """
    # Correlation matrix : 
    cor = the_df.corr() 
    plt.figure(figsize=(10, 10))
    sns.heatmap(cor, square = True, cmap="coolwarm", linewidths=0.5, annot=True, xticklabels='auto', yticklabels='auto',)
        
    # get the correlation matrix of the target variable
    #cor_target = abs(cor[target_var])
    # select the features with a correlation higher than 0.5
    #relevant_features = cor_target[cor_target>0.5]
    # print the features
    #print(relevant_features)
    
    return cor

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
model_XGB = XGBClassifier(n_estimators=100, max_depth=6, use_label_encoder=False)
model_LGBM = LGBMClassifier(n_estimators=100, max_depth=2)

# put all those models in a list
models = [model_LR, model_KNN, model_RF, model_XGB, model_LGBM]

# define a function to perform cross validation for the given models
def cross_validation(models, the_df, X, y, n_splits=10, random_state=71):
    """
    This function performs cross validation for the given models
    input:
        models: the models to be evaluated
        the_df: the dataframe
        n_splits: the number of splits
        random_state: the random state
    output:
        a dataframe with the results
    """
    # create a dataframe to store the results
    results = pd.DataFrame(columns=['model', 'accuracy', 'precision', 'recall', 'f1'])
    # Create conditional statement to check if stratified or not
    if stratified:
        # create a stratified k-fold object
        skf = StratifiedKFold(n_splits=n_splits, shuffle=False) #, random_state=random_state)
    else:
        # create a non stratified k-fold object
        skf = KFold(n_splits=n_splits, shuffle=False) #, random_state=random_state)
    # Define the features and the target
    X = the_df.drop(['FireMask'], axis=1)
    y = the_df['FireMask'].astype(int)
    # loop over the folds
    for train_index, test_index in skf.split(X, y):
        # split the data
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        # loop over the models
        for model in models:
            # fit the model
            time_0 = datetime.datetime.now()
            model.fit(X_train, np.ravel(y_train))
            time_1 = datetime.datetime.now()
            # predict the target
            y_pred = model.predict(X_test)
            # compute the accuracy
            accuracy = accuracy_score(y_test, y_pred)
            # compute the precision
            precision = classification_report(y_test, y_pred, output_dict=True)['1']['precision']
            # compute the recall
            recall = classification_report(y_test, y_pred, output_dict=True)['1']['recall']
            # compute the f1 score
            f1 = classification_report(y_test, y_pred, output_dict=True)['1']['f1-score']
            # compute the time to fit the model in seconds
            time_fit = (time_1 - time_0).total_seconds()
            # store the results in the dataframe
            results = results.append({'model': model.__class__.__name__,
                                      'accuracy': accuracy,
                                      'precision': precision,
                                      'recall': recall,
                                      'f1': f1,
                                      'Time to fit': time_fit}, ignore_index=True)
            # group the results by model
            results = results.groupby('model').mean().reset_index().sort_values(by='accuracy',
                             ascending=False).reset_index(drop=True)
    # return the dataframe
    return results