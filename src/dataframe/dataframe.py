import numpy as np
import xarray as xr
import pandas as pd
import module_dataframe as mdf

if __name__ == "__main__":
    # Create a path to the data directory
    path_data = "../../data/final/"

    # Load the data set
    datacube = xr.open_dataset(path_data + 'aggregate_datacube.nc')


    # Split the datacube into 10 datacubes, one for each year
    list_ds = mdf.split_datacube(datacube, first_year=2010, last_year=2021)


    # print the length of the list
    print(len(list_ds))

    # Create a list of dataframes
    list_df = mdf.get_df_list(list_ds)

    # Stack the dataframes from the list on top of each other

    df_final = pd.concat(list_df, axis=0, ignore_index=False)

    # Save the final dataframe into a csv
    #df_final.to_csv(path_data + 'df_final.csv')


