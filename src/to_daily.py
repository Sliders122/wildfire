from tests import *

# #     output: harmonized dataray to daily resolution from 01/01/2010 to 01/09/2022
# Import the datasets
path_data="../data/"
#%%
ndvi = xr.open_dataset(path_data+'ndvi_01012010_09012022.nc')

def print_start_end_date(ds):
    print("Start date: ", ds.time[0].values)
    print("End date: ", ds.time[-1].values)

# Function to print the time resolution of the dataset
def print_time_resolution(ds):
    print("Time resolution of: ", ds.time[1] - ds.time[0])

# Function to determine the minimum of the starting date from a list of datasets
def min_start_date(ds_list):
    # input: ds_list: list of xarray datasets
    # output: the minimum of the starting date from a list of datasets
    # example: min_start_date([ds1,ds2,ds3])
    return max([ds.time[0] for ds in ds_list])

# Function to determine the maximum of the ending date from a list of datasets
def max_end_date(ds_list):
    # input: ds_list: list of xarray datasets
    # output: the maximum of the ending date from a list of datasets
    # example: max_end_date([ds1,ds2,ds3])
    return min([ds.time[-1] for ds in ds_list])


if __name__ == "__main__":
    # Print the start date and end date of the dataset
    print_start_end_date(ndvi)
    # Print the time resolution of the dataset
    print_time_resolution(ndvi)
    # Test if the time resolution is daily
    test_daily_resolution([ndvi])



