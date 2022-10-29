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
    datacube = xr.open_dataset(path_data + 'datacube.nc')

    # To dataframe
    df = datacube.to_dataframe()

    # Remove the NaN values
    df = df.dropna()

    # Change the value of FireMAsk to 0 and 1. 0 = no fire, 1 = fire . If FireMask is 7,8,9 then it is a fire. If not, it is not a fire.
    df['FireMask'] = df['FireMask'].replace([0, 1, 2, 3, 4, 5, 6], 0)
    df['FireMask'] = df['FireMask'].replace([7, 8, 9], 1)

    # Create an object which counts the number of fire
    fire_count = df.groupby('FireMask').count()

    # Keep all the observations with FireMask = 1 and keep 'fire_count' observations with FireMask = 0 randomly
    df = df[df['FireMask'] == 1].append(df[df['FireMask'] == 0].sample(n=fire_count['FireMask'][1]))

    # Save the dataframe
    df.to_csv(path_data + 'dataframe.csv')

