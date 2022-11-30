import numpy as np
import rasterio
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
from shapely.geometry import mapping

# Definition of a function to print the crs of the data
def print_crs(dataray):
    """Prints the crs of the dataray"""
    return print(dataray.rio.crs)

# Definition of a function to define a crs for the dataray
def define_crs(dataray, crs=2154):
    """Defines a crs for the dataray"""
    return dataray.rio.write_crs(crs, inplace=True)

# Definition of a function to define the area of interest
def define_area_of_interest(aoi):
    """Defines the area of interest"""
    "input: path to aoi's shapefile"
    crop_extent = gpd.read_file(aoi)
    return crop_extent

# Definition of a function to print the crs of the crop_extent
def print_crs_crop_extent(crop_extent):
    """Prints the crs of the crop_extent"""
    return print(crop_extent.crs)

#Function to clip a datasets to the area of interest
def clip_to_aoi(dataset, aoi):
    """Clips the dataray to the area of interest"""
    "input: dataray, aoi"
    return dataset.rio.clip(aoi.geometry.apply(mapping), aoi.crs)

# Definition of a function to reproject a dataray from longlat to Lambert93
def reproject_to_lambert93(dataray):
    """Reprojects a dataray from longlat to Lambert93"""
    return dataray.rio.reproject("EPSG:2154")

def print_raster(raster):
    """Prints the raster's metadata and shape"""
    return f"shape: {raster.rio.shape}\n resolution: {raster.rio.resolution()}\n bounds: {raster.rio.bounds()}\n sum: {raster.sum().item()}\n CRS: {raster.rio.crs}\n" 

# Definition of a function to interpolate the datasets of continuous variables to a common grid
def interpolate_to_common_grid(dataray, common_grid):
    """Interpolates the dataray to a common grid"""
    return dataray.rio.reproject_match(common_grid, resampling=rasterio.enums.Resampling.bilinear)

# Definition of a function to interpolate the datasets of categorical variables to a common grid
def interpolate_to_common_grid_categorical(dataray, common_grid):
    """Interpolates the categorical dataray to a common grid"""
    return dataray.rio.reproject_match(common_grid, resampling=rasterio.enums.Resampling.mode)

def resample_to_daily(dataray):
    """Resamples the dataray to daily values"""
    return dataray.resample(time="1D").interpolate("linear")

# Definition of a function to resample catagorical variables to daily values
def resample_to_daily_categorical(dataray):
    """Resamples the categorical dataray to daily values"""
    return dataray.resample(time="1D").nearest()

    # put this for loop into a function
def aggregate_dataset(ds, dynamic_variables, period_size=10):
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
    for var in dynamic_variables:
        ds[var + '_mean'] = ds[var].rolling(time=period_size, center=False).mean().dropna(dim='time')

    return ds

# # Definition of a function to check on the dataset open before combining them
# def print_raster(raster):
#     """Prints the raster's metadata and shape"""
#     print(
#         f"shape: {raster.rio.shape}\n"
#         f"resolution: {raster.rio.resolution()}\n"
#         f"bounds: {raster.rio.bounds()}\n"
#         f"sum: {raster.sum().item()}\n"
#         f"CRS: {raster.rio.crs}\n"
#     )


# # Open the data
# def open_data(path):
#     """Opens the data"""
#     "input: path to the data"
#     return rxr.open_rasterio(path, masked=True).squeeze()


# # Resample the data to daily values
# # Definition of a function to resample the data to daily values
# def resample_to_daily(dataray):
#     """Resamples the dataray to daily values"""
#     return dataray.resample(time="1D").interpolate("linear")


# # Definition of a function to interpolate the data to a common grid
# def interpolate_to_common_grid(dataray):
#     """Interpolates the dataray to a common grid"""
#     return dataray.rio.reproject_match(common_grid)


# # Definition of the area of interest
# # Definition of a function to define the area of interest
# def define_area_of_interest(aoi):
#     """Defines the area of interest"""
#     "input: path to aoi's shapefile"
#     crop_extent = gpd.read_file(aoi)
#     return crop_extent


# # print the crs of the data
# # Definition of a function to print the crs of the data
# def print_crs(dataray):
#     """Prints the crs of the dataray"""
#     return print(dataray.rio.crs)


# # Definition of a function to print the crs of the crop_extent
# def print_crs_crop_extent(crop_extent):
#     """Prints the crs of the crop_extent"""
#     return print(crop_extent.crs)


# # defining a crs for the dataray
# # Definition of a function to define a crs for the dataray
# def define_crs(dataray, crs=2154):
#     """Defines a crs for the dataray"""
#     return dataray.rio.write_crs(crs, inplace=True)


# # Reproject a dataray from longlat to Lambert93
# # Definition of a function to reproject a dataray from longlat to Lambert93
# def reproject_to_lambert93(dataray):
#     """Reprojects a dataray from longlat to Lambert93"""
#     return dataray.rio.reproject("EPSG:2154")


# # Reproject a dataray from Lambert93 to longlat
# # Definition of a function to reproject a dataray from Lambert93 to longlat
# def reproject_to_longlat(dataray):
#     """Reprojects a dataray from Lambert93 to longlat"""
#     return dataray.rio.reproject("EPSG:4326")


# # clip the data to another dataray
# # Definition of a function to clip the data to another dataray
# def clip_to(dataray, dataray_to_clip_to):
#     """Clips the dataray to another dataray"""
#     return dataray.rio.clip(dataray_to_clip_to.rio.bounds(), dataray_to_clip_to.rio.crs)


# # Clip the data to a shapefile
# # Definition of a function to clip the data to a shapefile
# def clip_to_shapefile(dataray, path):
#     """Clips the dataray to a shapefile"""
#     "input: dataray, path to the shapefile"
#     return dataray.rio.clip(path, from_disk=True)


# # Clip the geotiff file to the netcdf file
# # Definition of a function to clip the geotiff file to the netcdf file
# def clip_geotiff_to_netcdf(geotiff, netcdf):
#     """Clips the geotiff file to the netcdf file"""
#     "input: geotiff, netcdf"
#     return clip_to(geotiff, netcdf)


# # Clip the geotiff file with a shapefile
# # Definition of a function to clip the geotiff file with a shapefile
# def clip_geotiff_with_shapefile(geotiff, path):
#     """Clips the geotiff file with a shapefile"""
#     "input: geotiff, path to the shapefile"
#     return clip_to_shapefile(geotiff, path)


# # Merge a geotiff file with a netcdf file
# # Definition of a function to merge a geotiff file with a netcdf file
# def merge_geotiff_netcdf(geotiff, netcdf):
#     """Merges a geotiff file with a netcdf file"""
#     "input: geotiff, netcdf"
#     return xr.merge([geotiff, netcdf])


# # Definition of a function to harmonize the data to a common grid
# def harmonize(dataray):
#     """Harmonizes the dataray to a common grid"""
#     return interpolate_to_common_grid(resample_to_daily(dataray))


# # Definition of a function to merge multiple datasets
# def merge_multiple(datarays):
#     """Merges multiple datarays"""
#     return xr.merge(datarays)


# # Harmonize a list of datasets
# # Definition of a function to harmonize a list of datarays
# def harmonize_multiple(datarays):
#     """Harmonizes a list of datarays
#     into a single harmonized dataray"""
#     """
#     input: list of datarays
#     output: harmonized dataray
#     """
#     return merge_multiple([harmonize(dataray) for dataray in datarays])


# # Export the harmonized data into a netcdf file
# # Definition of a function to export the harmonized data into a netcdf file
# def export_to_netcdf(dataray, path):
#     """Exports the dataray into a netcdf file"""
#     "input: dataray, path to the netcdf file"
#     return dataray.to_netcdf(path)


# # Read the data exported from the harmonize.py script
# # Definition of a function to read the data exported from the harmonize.py script
# def read_data(path):
#     """Reads the data exported from the harmonize.py script"""
#     "input: path to the data"
#     return xr.open_dataset(path)

# #plot the one variable
# # Definition of a function to plot the one variable at a specific time
# def plot_one_variable(dataray, variable, time):
#     """Plots the one variable at a specific time"""
#     "input: dataray, variable, time"
#     return dataray[variable].sel(time=time).plot()

# # Multiple plots of one variable over time range
# # Definition of a function to plot multiple plots of one variable over time range
# def plot_multiple(dataray, variable, time_range):
#     """Plots multiple plots of one variable over time range"""
#     "input: dataray, variable, time_range"
#     return dataray[variable].sel(time=time_range).plot(col="time", col_wrap=4)
