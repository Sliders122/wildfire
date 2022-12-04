import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import datetime
import pickle


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
model_XGB = XGBClassifier(n_estimators=100, max_depth=2, use_label_encoder=False)
model_LGBM = LGBMClassifier(n_estimators=100, max_depth=2)

# put all those models in a list
models = [model_LR, model_KNN, model_RF, model_XGB, model_LGBM]

# define a function to perform cross validation for the given models
def cross_validation(models, the_df, X, y, n_splits=10, random_state=71, stratified=True):
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

# Split the data into train on 2010 to 2017 and test on 2018 to 2020
df = pd.read_csv(path_data + "df_final.csv", parse_dates=["time"])
# Split the data into train and test
df_train = df[df["time"] < "2018-01-01"]
df_test = df[df["time"] >= "2018-01-01"]

# define a function to fit a lgmb model
def fit_lgbm_model(the_df_train, n_estimators=100, max_depth=2, path_data=""):
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
    model.time_to_fit = (time_end - time_start).total_seconds()
    # generate and save the pickle file
    pickle.dump(model, open(path_data + 'model_lgbm.pkl', 'wb'))
    return model

# define a function to predict the target
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

# define a function to compute the metrics
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
                                      'time to fit [s]': model.time_to_fit
                                      }, ignore_index=True)
    return results
    