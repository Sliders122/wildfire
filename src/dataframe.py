import numpy as np
import rasterio
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
import harmonize as hz
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler

if __name__ == "__main__":
    # Create a path to the data directory
    path_data = "../data/final/"

    # Load the data set
    datacube = xr.open_dataset(path_data + 'final_datacube_gps.nc')

    
    # define the variables to be modified
    dynamic_variables = ['ET_500m',
                            'Fpar_500m',
                            'u10',
                            'v10',
                            't2m',
                            'tp',
                            'LST_Day_1km',
                            'LST_Night_1km',
                            '_1_km_16_days_EVI']

    # define function to loop over the dataset to fill the new variable
    def fill_ds_mean(the_ds, period_size=10, list_variables = []):
        """
        This function appends and fills the new variables of the dataset with the mean values,
        then drops the old ones.
        input:
            the_ds: the dataset
            period_size: the size of the period
            list_variables: the variables to be selected
        output:
            the dataset with the new variables filled
        """
        # Add new variables to the dataset
        for var in list_variables:
            the_ds[var + '_last'+ str(period_size) + 'days' + '_mean'] = ds[var].rolling(time=period_size,
             center=False).mean().dropna(dim='time')

        # drop the old variables
        the_ds = the_ds.drop(dynamic_variables)

        return the_ds
    
    ds = fill_ds_mean(datacube, period_size=10, list_variables = dynamic_variables)

    # Define the dataframe
    def get_df(the_ds, first_year=2015, last_year=2019):
        """
        This function returns a dataframe from the dataset in the given period,
         dropping unnecessary variables and all NaN values
        input:
            the_ds: the dataset
        output:
            the_df: the dataframe
        """
        # define an empty dataframe
        the_df = pd.DataFrame()
        # Divide the dataset into every year
        
        for year in range(first_year, last_year+1):

            the_df = the_df.append(the_ds.sel(time=slice(str(year) + '-01-01'
            , str(year) + '-12-30')).to_dataframe())
        
        # Reshape FireMask variable
        
            # drop the columns we don't need anymore
        the_df = the_df.drop(columns = ["crs" , "band", "spatial_ref"])

            # drop observations with FireMask = 0, 1 & 2 equivalent to NaN
        the_df = the_df[(the_df.FireMask != 0) & (the_df.FireMask != 1) & (the_df.FireMask != 2)]

        # drop the rows with NaN values
        the_df = the_df.dropna()

        return the_df
    
    df = get_df(ds, first_year=2015, last_year=2019)

    # Define a function to get balanced preditors and binary target variables from the dataframe
    def get_balanced_pred_target(the_df, target_var):
        """
        This function returns the predictors and target variables from the dataframe
        input:
            the_df: the dataframe
            target_var: the target variable
        output:
            X_res: the balanced predictors
            y_res: the balanced target variable
        """
        X = the_df.drop(columns=[target_var])
        y = the_df[target_var]

        # Get y binary
        y = y.replace([7, 8, 9], 1)
        y = y.replace([3, 4, 5], 0)

        #Undersampling the dataframes to balance the classes
        rus = RandomUnderSampler()
        X_res, y_res = rus.fit_resample(X, y)

        return X_res, y_res

    X_res, y_res = get_balanced_pred_target(df, target_var='FireMask')

"""
    # Subset only for the month june, July, August of each year
    datacube = datacube.sel(time=datacube['time.month'].isin([4,5,6, 7, 8,9,10]))

    # Subset for training
    datacube_train = datacube.sel(time=slice('2010-01-01', '2017-12-31'))
    # Subset for testing
    datacube_test = datacube.sel(time=slice('2018-01-01', '2021-01-01'))

    # To dataframe
    df_train = datacube_train.to_dataframe()
    df_test = datacube_test.to_dataframe()

    # Drop the columns we don't need: crs, band, spatial_ref
    df_train = df_train.drop(columns=['crs', 'band', 'spatial_ref'])
    df_test = df_test.drop(columns=['crs', 'band', 'spatial_ref'])

    # Remove the NaN values except for the first_day column, last_day column and the burn_date column

    df_train = df_train.dropna()
    df_test = df_test.dropna()

    # Change the value of FireMAsk to 0 and 1. 0 = no fire, 1 = fire . If FireMask is 7,8,9 then it is a fire. If
    # not, it is not a fire.
    df_train['FireMask'] = df_train['FireMask'].replace([0, 1, 2, 3, 4, 5, 6], 0)
    df_train['FireMask'] = df_train['FireMask'].replace([7, 8, 9], 1)
    df_test['FireMask'] = df_test['FireMask'].replace([0, 1, 2, 3, 4, 5, 6], 0)
    df_test['FireMask'] = df_test['FireMask'].replace([7, 8, 9], 1)

    # Create an object which evaluates the length of FireMask==1

    # Sum the number of fires in the training data and change into an integer
    num_fires_train = int(df_train['FireMask'].sum())
    # Sum the number of fires in the testing data and change into an integer
    num_fires_test = int(df_test['FireMask'].sum())
	
	# Keep all the observations with FireMask = 1 and keep 'fire_count' observations with FireMask = 0 randomly
    df_train_balanced_gps = df_train[df_train['FireMask'] == 1].append(
        df_train[df_train['FireMask'] == 0].sample(n=(2*num_fires_train), random_state=1))
    df_test_balanced_gps = df_test[df_test['FireMask'] == 1].append(
        df_test[df_test['FireMask'] == 0].sample(n=(2*num_fires_test), random_state=1))

    # Save the dataframes df_train_balanced and df_test_balanced, df_test as csv files
    df_train_balanced_gps.to_csv(path_data + 'df_train_balanced.csv')
    df_test_balanced_gps.to_csv(path_data + 'df_test_balanced.csv')
    #df_test.to_csv(path_data + 'df_test_imbalanced.csv')
	

        mean_value = the_ds[variable].isel(x=x, y=y, time=slice(t-period_size-1, t-1)).mean(dim='time').values

        return mean_value

"""
