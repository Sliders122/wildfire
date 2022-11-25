from pycaret.classification import *
import numpy as np
import pandas as pd
import waitress

if __name__ == "__main__":
    # Load the data from a github repository
    url_test = "https://raw.githubusercontent.com/Sliders122/wildfire/main/df_test_balanced.csv"
    url_train = "https://raw.githubusercontent.com/Sliders122/wildfire/main/df_train_balanced.csv"

    # Load the data into a pandas dataframe and parsing the 'time' column as a datetime object
    df_test = pd.read_csv(url_test, parse_dates=['time'])
    df_train = pd.read_csv(url_train, parse_dates=['time'])

    # Initialize the setup with pycaret for the training data. Get the all set up for the training data
    clf1 = setup(data=df_train, target="FireMask", session_id=123, remove_outliers=True, silent=True)

    # Create a model from lightgbm
    lightgbm = create_model("lightgbm")

    # Tune the model
    tuned_lightgbm = tune_model(lightgbm)

    # Dashboard for the model display with 'dash' with a public ip address
    dashboard(tuned_lightgbm, display_format="dash", run_kwargs={"host": '0.0.0.0', "port": 9050, "use_waitress": True})







