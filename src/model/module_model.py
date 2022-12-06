import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import datetime
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier


# define a function to get the correlation matrix and plot it
def get_correlation_matrix(the_df):
    """
    This function returns the correlation matrix of the dataframe
    input:
        the_df: the dataframe
    output:
        the correlation matrix
    """
    # Correlation matrix : 
    cor = the_df.corr() 
    plt.figure(figsize=(15, 15))
    sns.heatmap(cor, square = True, cmap="coolwarm", linewidths=0.5, annot=True, xticklabels='auto', yticklabels='auto',)
    # return the correlation matrix    
    return cor


# define a function to perform cross validation for the given models
def cross_validation(models, the_df, n_splits=10, random_state=71, stratified=True, shuffle=True):
    """
    This function performs cross validation for the given models
    input:
        models: the models to be evaluated
        X: the features
        y: the target
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
        if shuffle:
            kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        else:
            kf = StratifiedKFold(n_splits=n_splits, shuffle=False)
    else:
        # create a non stratified k-fold object
        if shuffle:
            kf = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        else:
            kf = KFold(n_splits=n_splits, shuffle=False) 
    # Define target and features
    X = the_df.drop(['time','FireMask'], axis=1)
    y = the_df['FireMask'].astype(int)
    # loop over the folds
    for train_index, test_index in kf.split(X, y):
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

            # store the results in the dataframe sorted by accuracy
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


# Define the function to fit the model
def fit_lgbm_model(the_df_train, n_estimators=100, max_depth=2):
    """
    This function fits a lgmb model
    input:
        the_df_train: the dataframe
        n_estimators: the number of estimators
        max_depth: the maximum depth
        path_data: the path where to save the pickle file
    output:
        the model
    """
    # define the model
    model = LGBMClassifier(n_estimators=n_estimators, max_depth=max_depth)
    # define the features and the target
    X_train = the_df_train.drop(['time','FireMask'], axis=1)
    y_train = the_df_train['FireMask'].astype(int)
    # fit the model
    time_start = datetime.datetime.now()
    model.fit(X_train, y_train)
    time_end = datetime.datetime.now()
    # Add the time as model attribute
    model.time = (time_end - time_start).total_seconds()
    # Return the model
    return model


# Define the function to predict the target
def predict_lgbm_model(the_df_test, model):
    """
    This function predicts the lgbm model
    input:
        the_df_test: the tet dataframe
        model: the model
    output:
        the predictions
    """
    # define the features
    X_test = the_df_test.drop(['time','FireMask'], axis=1)
    # predict the model
    y_pred = model.predict(X_test)
    # give the perobabilities of the predictions
    y_pred_proba = model.predict_proba(X_test)
    
    # Stack the prediction with the time and target
    the_df_pred = pd.DataFrame({"time":the_df_test["time"], "FireMask": the_df_test["FireMask"].astype(int),
                                "FireMask_pred": y_pred, "FireMask_proba": y_pred_proba[:, 1]})
    # return the the dataframe
    return the_df_pred


# define a function to plot accuracy, precision, recall, f1-score and time to fit
def plot_metrics(model, y_test, y_pred):
    """
    This function plots the accuracy, precision, recall, f1-score
    input:
        y_test: the test target
        y_pred: the predictions
    output:
        None
    """
    results = pd.DataFrame(columns=['model', 'accuracy', 'precision', 'recall', 'f1'])
    # compute the metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    # plot the metrics
    results = results.append({'model': model.__class__.__name__,
                                      'accuracy': accuracy,
                                      'precision': precision,
                                      'recall': recall,
                                      'f1': f1,
                                      'time to fit [s]': model.time
                                      }, ignore_index=True)
    return results
    