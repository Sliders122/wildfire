import harmonize as hz
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
from shapely.geometry import mapping

if __name__ == "__main__":

    ''' ----------------------------------------------------------------------------------------------------------------
----------------------------------------1. Load raw dataset ---------------------------------------------------------'''

    # Create a path to the data directory
    path_data = "../../data/final/"

    # Load the data set
    ndvi = xr.open_dataset(path_data + 'final_ndvi_16D_1km.nc')
    lai = xr.open_dataset(path_data + 'final_lai_8D_500m.nc')
    evap = xr.open_dataset(path_data + 'final_evap_8D_500m.nc')
    era = xr.open_dataset(path_data + 'Raw_weather_4H_9km.nc')
    lst_night = xr.open_dataset(path_data + 'final_lst_night_1D_1km.nc')
    lst_day = xr.open_dataset(path_data + 'final_lst_day_1D_1km.nc')
    active_fire = xr.open_dataset(path_data + 'final_active_fire_1M_500m.nc')
    burn_mask = xr.open_dataset(path_data + 'final_fire_mask_1M_1km.nc')
    fwi = xr.open_mfdataset(path_data + '/Raw_Fwi/*.nc', combine='by_coords', chunks=None)
    density = rxr.open_rasterio(path_data + 'fra_pd_2015_1km_UNadj.tif', masked=True).squeeze()

    ''' ----------------------------------------------------------------------------------------------------------------
-------------------------------------2. Select variables of interest ------------------------------------------------'''
    # Select the variables of interest
    ndvi_filter = ndvi['_1_km_16_days_EVI']
    lai_filter = lai['Fpar_500m']
    evap_filter = evap['ET_500m']
    era_filter = era[['u10', 'v10', 't2m', 'tp']]
    lst_night_filter = lst_night['LST_Night_1km']
    lst_day_filter = lst_day['LST_Day_1km']
    active_fire_filter = active_fire[['First_Day', 'Last_Day', 'Burn_Date']]
    burn_mask_filter = burn_mask['FireMask']

    ''' ----------------------------------------------------------------------------------------------------------------
----------------------------------------3. Select duration -------------------------------------------------------

    1) Harmonize the datacube to the same calendar: Julian calendar
    2) Select the period of interest: 2010-2021
    
    1) Harmonize the datacube to the same calendar: Julian calendar'''
    era_filter = era_filter.convert_calendar('julian')

    """ 2) Select the period of interest: 2010-2021"""
    ndvi_filter = ndvi_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    lai_filter = lai_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    evap_filter = evap_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    era_filter = era_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    lst_night_filter = lst_night_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    lst_day_filter = lst_day_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    active_fire_filter = active_fire_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    burn_mask_filter = burn_mask_filter.sel(time=slice('2010-01-01', '2021-01-01'))

    ''' ----------------------------------------------------------------------------------------------------------------
-------------------------------------4. Fill the missing values ------------------------------------------------

    1) Quadratic interpolation for the land surface temperature because of high number of missing values (more than 50%)
    2) Linear interpolation for variables from era5 which have around 20% of missing values
    3) Forwardfill for the other variables which have less than 10% of missing values and are categorical variables'''

    ''' 1) Quadratic interpolation '''
    lst_day_filter = lst_day_filter.interpolate_na(dim='time', method='quadratic').ffill(dim='xdim').ffill(dim='ydim')
    lst_night_filter = lst_night_filter.interpolate_na(dim='time', method='quadratic').ffill(dim='xdim').ffill(
        dim='ydim')

    ''' 2) Linear interpolation '''
    era_filter = era_filter.interpolate_na(dim='time', method='linear').ffill(dim='xdim').ffill(dim='ydim')

    ''' 3) Forwardfill '''
    ndvi_filter = ndvi_filter.ffill(dim='time').ffill(dim='xdim').ffill(dim='ydim')
    lai_filter = lai_filter.ffill(dim='xdim').ffill(dim='ydim').ffill(dim='time')
    evap_filter = evap_filter.ffill(dim='xdim').ffill(dim='ydim').ffill(dim='time')
    active_fire_filter = active_fire_filter.ffill(dim='xdim').ffill(dim='ydim').ffill(dim='time')
    burn_mask_filter = burn_mask_filter.ffill(dim='xdim').ffill(dim='ydim').ffill(dim='time')
    density = density.ffill(dim='x', limit=None).ffill(dim='y', limit=None)

    ''' ----------------------------------------------------------------------------------------------------------------
-------------------------------------5. Writing CRS ---------------------------------------------------------------

    1) Create a CRS object from a poj4 string for sinuoidal projection
    2) Set the CRS of the data sets with hz.define_crs()'''

    ''' 1) Create a CRS object from a poj4 string for sinuoidal projection'''
    crs_sinu = rasterio.crs.CRS.from_string(
        "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs")

    ''' 2) Set the CRS of the data sets with hz.define_crs()'''
    ndvi_filter = hz.define_crs(ndvi_filter, crs_sinu)
    lai_filter = hz.define_crs(lai_filter, crs_sinu)
    evap_filter = hz.define_crs(evap_filter, crs_sinu)
    era_filter = hz.define_crs(era_filter, 4326)
    lst_night_filter = hz.define_crs(lst_night_filter, crs_sinu)
    lst_day_filter = hz.define_crs(lst_day_filter, crs_sinu)
    active_fire_filter = hz.define_crs(active_fire_filter, crs_sinu)
    burn_mask_filter = hz.define_crs(burn_mask_filter, crs_sinu)
    density = hz.define_crs(density, 4326)

    ''' ----------------------------------------------------------------------------------------------------------------
-------------------------------------6. Clipping to the AOI ------------------------------------------------

    1) Define the AOI
    2) Clip the data sets to the AOI'''

    ''' 1) Define the AOI'''
    aoi = hz.define_area_of_interest(path_data + 'Large.zip')

    ''' 2) Clip the data sets to the AOI'''
    era_filter = hz.clip_to_aoi(era_filter, aoi)
    density = hz.clip_to_aoi(density, aoi)

    ''' ----------------------------------------------------------------------------------------------------------------
-------------------------------------7. Projection ------------------------------------------------

    1) Define a common grid to project the data sets
    2) Projection of the Era5 data set
        2.1 Downsample era5 first to daily data decrease the computational time
        2.2 Project the downsampled data set to the same crs as the common grid
        2.3 Rename the dimensions in order to project the data set to the common grid
        2.4 Project to the common grid
    3) Projection of the density dataaray
        3.1 Create a name for the data array
        3.2 Change the array into a data set
        3.3 Project the data set to the common grid 
    4) Projection of the other data sets'''

    ''' 1) Define a common grid to project the data sets'''
    common_grid = rxr.open_rasterio(path_data + 'final_lst_day_1D_1km.nc').isel(time=0)

    ''' 2) Projection of the Era5 data set'''
    ''' 2.1 Downsample era5 first to daily data decrease the computational time'''
    era_filter_daily = hz.resample_to_daily(era_filter)

    ''' 2.2 Project the downsampled data set to the same crs as the common grid'''
    era_sinu = era_filter_daily.rio.reproject(crs_sinu)

    ''' 2.3 Rename the dimensions in order to project the data set to the common grid'''
    era_filter_proj = era_sinu.rename({'y': 'ydim', 'x': 'xdim'})

    ''' 2.4 Project to the common grid'''
    era_filter_proj = hz.interpolate_to_common_grid(era_sinu, common_grid)

    ''' 3) Projection of the density dataaray    
        3.1 Create a name for the data array'''
    density.name = 'density'

    ''' 3.2 Change the array into a data set'''
    density = density.to_dataset()

    ''' 3.3 Project the data set to the common grid '''
    density_proj = hz.interpolate_to_common_grid(density, common_grid)

    ''' 4) Projection of the other data sets'''
    lai_filter_proj = hz.interpolate_to_common_grid(lai_filter, common_grid)

    evap_filter_proj = hz.interpolate_to_common_grid_categorical(evap_filter, common_grid)

    # Different method to interpolate the active fire data set because of the different data type
    active_fire_filter_proj = active_fire_filter.interp(ydim=ndvi["ydim"], xdim=ndvi['xdim'])

    ''' ----------------------------------------------------------------------------------------------------------------
-----------------------------------------8. Resampling to daily -----------------------------------------------------'''
    # Resample to daily
    ndvi_filter_daily = hz.resample_to_daily(ndvi_filter)
    burn_mask_filter_daily = hz.resample_to_daily_categorical(burn_mask_filter)
    lai_filter_proj_daily = hz.resample_to_daily(lai_filter_proj)
    evap_filter_proj_daily = hz.resample_to_daily_categorical(evap_filter_proj)
    active_fire_filter_proj_daily = hz.resample_to_daily(active_fire_filter_proj)

    ''' ----------------------------------------------------------------------------------------------------------------
------------------------------- 9 Prepare the datasets for merging --------------------------------------------

    Prepare the datasets for merging:
    1) Delete the attribute grid_mapping: unecessary and conflictual
    2) Create the two list from the name of the coordinates       
    3) Match the coordinates values of the data sets to match the other data sets
    4) Rename the coordinates of the data sets to match the other data sets
    5) Merge the data sets'''

    '''1) Delete the attribute grid_mapping: unnecessary and conflictual'''
    # Deleting attribute grid_mapping of the burn_mask_filter data set
    del burn_mask_filter.attrs['grid_mapping']
    # Deleting attribute grid_mapping of the evap_filter_proj data set
    del evap_filter_proj.attrs['grid_mapping']
    # Deleting attribute grid_mapping of the lst_night_filter data set
    del lst_night_filter.attrs['grid_mapping']
    # Deleting attribute grid_mapping of the lst_day_filter data set
    del lst_day_filter.attrs['grid_mapping']
    # Deleting attribute grid_mapping of the ndvi_filter data set
    del ndvi_filter.attrs['grid_mapping']
    # Deleting attribute grid_mapping of the lai_filter data set
    del lai_filter.attrs['grid_mapping']

    ''' 2) Create the two list from the name of the coordinates'''
    # Create a list of the data sets
    data_sets = [ndvi_filter_daily, burn_mask_filter_daily, lai_filter_proj_daily, evap_filter_proj_daily,
                 era_filter_proj, active_fire_filter_proj_daily]

    # Create a first list with coordinate x and y
    list_xy = [lai_filter_proj_daily,
               evap_filter_proj_daily,
               era_filter_proj,
               density_proj]

    # Create a second list with coordinate xdim and ydim
    list_xdimydim = [ndvi_filter_daily,
                     burn_mask_filter_daily,
                     active_fire_filter_proj_daily,
                     lst_night_filter,
                     lst_day_filter]

    # Merge and save by coordinates the data sets from the lists
    ds_xy = xr.combine_by_coords(list_xy, combine_attrs='drop_conflicts')
    ds_xdimydim = xr.combine_by_coords(list_xdimydim, combine_attrs='drop_conflicts')

    ''' 3) Match the coordinates of the data sets to match the other data sets'''
    ds_xdimydim_xdimydim = ds_xdimydim.assign_coords(xdim=ds_xy.coords['x'].values, ydim=ds_xy.coords['y'].values)

    ''' 4) Rename the coordinates to match the other data sets'''
    ds_xdimydim_xdimydim = ds_xdimydim_xdimydim.rename({'xdim': 'x', 'ydim': 'y'})

    ''' 5) Merge the data sets'''
    ds = xr.merge([ds_xy, ds_xdimydim_xdimydim])

    ''' ----------------------------------------------------------------------------------------------- 
---------------------------------10 Poject to GPS coordinates-------------------------------------------------'''

    ''' We have a datacube with the following dimensions: time, y, x. We want now:
        to project it into GPS coordinates.'''

    '''  Projection of the data cube into GPS coordinates'''
    # Projection of ds into WGS84
    ds_gps = ds.rio.reproject("EPSG:4326", grid_mapping_name='latitude_longitude')

    ''' ----------------------------------------------------------------------------------------------------------------
------------------------------- 11 Create aggregated variables --------------------------------------------

    1) Create a list of the dynamic variables to aggregate
    2) Split the datacube into 10 datacubes of 1 year for computation reasons       
    3) Apply the function to aggregate the variables: mean over 10 previous days
    4) Concatenate the datacubes'''

    ''' 1) Create a list of the dynamic variables to aggregate'''
    dynamic_variables = ['ET_500m',
                         'Fpar_500m',
                         'u10',
                         'v10',
                         't2m',
                         'tp',
                         'LST_Day_1km',
                         'LST_Night_1km',
                         '_1_km_16_days_EVI']

    ''' 2) Split the datacube into 10 datacubes of 1 year for computation reasons'''
    list_ds = hz.split_datacube(ds_gps, first_year=2010, last_year=2011)

    ''' 3) Apply the function to aggregate the variables: mean over 10 previous days'''
    for i in range(len(list_ds)):
        list_ds[i] = hz.aggregate_dataset(list_ds[i], period_size=10, dynamic_variables=dynamic_variables)
        print(f"list_ds[{i}] ok")

    ''' 4) Concatenate the datacubes'''
    aggregate_datacube = xr.concat(list_ds, dim="time")

    ''' ---------------------------------------------------------------------------------------------------------------- 
----------------------------------------------12. Save the datacube--------------------------------------------------

    1) Delete unnecessary attributes
    2) Save the datacube'''

    ''' 1) Delete unnecessary attributes'''
    del aggregate_datacube['First_Day'].attrs['grid_mapping']
    del aggregate_datacube['Last_Day'].attrs['grid_mapping']
    del aggregate_datacube['Burn_Date'].attrs['grid_mapping']
    del aggregate_datacube['FireMask'].attrs['grid_mapping']

    ''' 2) Save the datacube'''
    aggregate_datacube.to_netcdf(path_data + 'dummy.nc')
