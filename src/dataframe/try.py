import numpy as np
import xarray as xr
import pandas as pd


# Define a function which split the datacube into 10 datacubes, one for each year. Call them ds_2015, ds_2016, etc.
def split_datacube(the_ds, first_year=2015, last_year=2019):
    """
    This function returns a list of datacubes, one for each year in the given period
    input:
        the_ds: the dataset
        first_year: the first year of the period
        last_year: the last year of the period
    output:
        a list of datacubes
    """
    # Create an empty list
    list_ds = []
    # Loop over the years
    for year in range(first_year, last_year+1):
        # Select the datacube for the year
        ds_year = the_ds.sel(time=str(year))
        # Append the datacube to the list
        list_ds.append(ds_year)
    return list_ds


def fill_ds_mean(the_ds, period_size=10, list_variables=[]):
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
    # Add a new variable to the dataset
    for var in list_variables:
        the_ds[var + '_last' + str(period_size) + 'days' + '_mean'] = (('x', 'y',
                                                                        'time'), np.zeros(
            (the_ds.x.size, the_ds.y.size, the_ds.time.size)))

    # loop over the dataset to fill the new variable
    for var in list_variables:
        for x in range(the_ds.x.size):
            for y in range(the_ds.y.size):
                for t in range(the_ds.time.size):
                    the_ds[var + '_last' + str(period_size) + 'days' + '_mean'].values[x, y,
                                                                                       t] = get_lastdays_mean_ds(the_ds,
                                                                                                                 t=t,
                                                                                                                 x=x,
                                                                                                                 y=y,
                                                                                                                 period_size=period_size,
                                                                                                                 variable=var)

    # drop the old variables
    the_ds = the_ds.drop(dynamic_variables)

    return the_ds

def get_lastdays_mean_ds(the_ds, t=0, x=0, y=0, period_size=10, variable='u10'):
    """
    This function returns a the mean value of the selected pixel and the selected period of time
    input:
        the_ds: the dataset
        t: the time index
        x: the x index
        y: the y index
        period_size: the size of the period
        variable: the variable to be selected
    output:
        the mean value over the previous period_size days
        of the selected pixel and the selected period of time
    """

    mean_value = the_ds[variable].isel(x=x, y=y, time=slice(t-period_size-1, t-1)).mean(dim='time').values

    return mean_value



# Define a function which create a list of dataframes  for each year. call them df_2015, df_2016, etc.
def get_df_list(list_ds):
    """
    This function returns a list of dataframes, one for each year in the given period
    input:
        list_ds: the list of datacubes
    output:
        a list of dataframes
    """
    # Create an empty list
    list_df = []

    # Loop over the datacubes
    for ds in list_ds:
        # Convert the datacube to a dataframe
        df = ds.to_dataframe()

        #drop the unnecessary variables
        df = df.drop(columns=['crs', 'band', 'spatial_ref'])

        # Remove the NaN values
        df = df.dropna()

        # Change the value of FireMAsk to 0 and 1. 0 = no fire, 1 = fire . If FireMask is 7,8,9 then it is a fire. If not, it is not a fire.
        df['FireMask'] = df['FireMask'].replace([0, 1, 2, 3, 4, 5, 6], 0)
        df['FireMask'] = df['FireMask'].replace([7, 8, 9], 1)

        # Sum the number of fires in  data and change into an integer
        num_fires = int(df['FireMask'].sum())

        # Keep all the observations with FireMask = 1 and keep 'fire_count' observations with FireMask = 0 randomly
        df = df[df['FireMask'] == 1].append(
            df[df['FireMask'] == 0].sample(n=num_fires, random_state=1))


        # Append the dataframe to the list
        list_df.append(df)
    return list_df



if __name__ == "__main__":
    # Create a path to the data directory
    path_data = "../../data/final/"

    # Load the data set
    datacube = xr.open_dataset(path_data + 'aggregate_datacube.nc')


    # Split the datacube into 10 datacubes, one for each year
    list_ds = split_datacube(datacube, first_year=2010, last_year=2021)


    # print the length of the list
    print(len(list_ds))

    # Create a list of dataframes
    list_df = get_df_list(list_ds)

    # Stack the dataframes from the list on top of each other

    # Save the first dataframe into a csv
    list_df[0].to_csv(path_data + 'df_2010.csv')
    print("2010 ok")

    df_final = pd.concat(list_df, axis=0, ignore_index=False)

    # Save the final dataframe into a csv
    df_final.to_csv(path_data + 'df_final.csv')

    # Save the dataframe
   #df_210 df_final.to_csv(path_data + 'final_dataframe_gps.csv')

    # # Print the shape of the final dataframe
    # print(df_final.shape)
    #
    # # Print the number of fires
    # print(df_final['FireMask'].sum())
    #
    # # Print the number of non fires
    # print(df_final['FireMask'].count() - df_final['FireMask'].sum())
    #
    # # Print the number of observations
    # print(df_final['FireMask'].count())
    #
    #
    # # Print the head of the dataframe
    # print(df_final.head())






