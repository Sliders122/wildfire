import numpy as np
import rasterio
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
import harmonize as hz

if __name__ == "__main__":
    # Create a path to the data directory
    path_data = "../data/final/"

    # Load the data set
    datacube = xr.open_dataset(path_data + 'datacube_gps.nc')

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
