import harmonize as hz
import numpy as np
import xarray as xr
import rioxarray as rxr

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


if __name__ == "__main__":
    # Create a path to the data directory
    path_data = "../data/final/"

    # Load the final_datacube_gps
    final_datacube_gps = xr.open_dataset(path_data + "final_datacube_gps.nc")

    # Print percentage of missing values of ET_500m
    print(f"Percentage of missing values of ET_500m: {final_datacube_gps.ET_500m.isnull().sum().item() / final_datacube_gps.ET_500m.size * 100:.2f}%")

    # Keep only year 2018
    #final_datacube_gps = final_datacube_gps.sel(time="2018")

    # Split the datacube into 10 datacubes, one for each year
    list_ds = split_datacube(final_datacube_gps, first_year=2010, last_year=2021)


    # Build a list of dynamic variables
    dynamic_variables = ['ET_500m',
                         'Fpar_500m',
                         'u10',
                         'v10',
                         't2m',
                         'tp',
                         'LST_Day_1km',
                         'LST_Night_1km',
                         '_1_km_16_days_EVI']

    # Update list_ds with the mean of the dynamic variables over 10 days (hz.aggregate_dataset) for each year
    for i in range(len(list_ds)):
        list_ds[i] = hz.aggregate_dataset(list_ds[i], period_size=10, dynamic_variables=dynamic_variables)
        print(f"list_ds[{i}] ok")


    # Merge the datacubes into one datacube
    aggregate_datacube = xr.concat(list_ds, dim="time")

    # Print Min the variable ET_500m_mean
    print("Min ET_500m_mean: ", aggregate_datacube.ET_500m_mean.min().values)

    # Print Max the variable ET_500m_mean
    print("Max ET_500m_mean: ", aggregate_datacube.ET_500m_mean.max().values)

    # Print mean of the variable ET_500m_mean
    print("Mean ET_500m_mean: ", aggregate_datacube.ET_500m_mean.mean().values)

    # Print median of the variable ET_500m_mean
    print("Median ET_500m_mean: ", aggregate_datacube.ET_500m_mean.median().values)

    # Print standard deviation of the variable ET_500m_mean
    print("Standard deviation ET_500m_mean: ", aggregate_datacube.ET_500m_mean.std().values)

    # Print the percentage of missing values of the variable ET_500m_mean
    print("Percentage of missing values ET_500m_mean: ", np.sum(aggregate_datacube.ET_500m_mean.isnull())/aggregate_datacube.ET_500m_mean.size*100)

    # Save the aggregate_datacube
    aggregate_datacube.to_netcdf(path_data + "aggregate_datacube.nc")


