import harmonize as hz
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray as rxr
import geopandas as gpd
from shapely.geometry import mapping

if __name__ == "__main__":
    # Create a path to the data directory
    path_data = "../data/final/"

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

    # Select the variables of interest
    ndvi_filter = ndvi['_1_km_16_days_EVI']
    lai_filter = lai['Fpar_500m']
    evap_filter = evap['ET_500m']
    era_filter = era[['u10', 'v10', 't2m', 'tp']]
    lst_night_filter = lst_night['LST_Night_1km']
    lst_day_filter = lst_day['LST_Day_1km']
    # fwi_filter = fwi['fwi-daily-proj']
    active_fire_filter = active_fire[['First_Day', 'Last_Day', 'Burn_Date']]
    burn_mask_filter = burn_mask['FireMask']

    # Convert era calendar to cftime.DatetimeJulian
    era_filter = era_filter.convert_calendar('julian')
    # Subset the data sets to the same time period: 2010-01-01 to 2021-01-01
    ndvi_filter = ndvi_filter.sel(time=slice('2010-01-01', '2011-03-01'))
    lai_filter = lai_filter.sel(time=slice('2010-01-01', '2011-03-01'))
    evap_filter = evap_filter.sel(time=slice('2010-01-01', '2011-03-01'))
    era_filter = era_filter.sel(time=slice('2010-01-01', '2011-03-01'))
    lst_night_filter = lst_night_filter.sel(time=slice('2010-01-01', '2011-03-01'))
    lst_day_filter = lst_day_filter.sel(time=slice('2010-01-01', '2011-03-01'))
    # fwi_filter = fwi_filter.sel(time=slice('2010-01-01', '2021-01-01'))
    active_fire_filter = active_fire_filter.sel(time=slice('2010-01-01', '2011-03-01'))
    burn_mask_filter = burn_mask_filter.sel(time=slice('2010-01-01', '2011-03-01'))

    # Create a CRS object from a poj4 string for sinuoidal projection
    crs_sinu = rasterio.crs.CRS.from_string(
        "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs")

    # Set the CRS of the data sets with hz.define_crs()
    ndvi_filter = hz.define_crs(ndvi_filter, crs_sinu)
    lai_filter = hz.define_crs(lai_filter, crs_sinu)
    evap_filter = hz.define_crs(evap_filter, crs_sinu)
    era_filter = hz.define_crs(era_filter, 4326)
    lst_night_filter = hz.define_crs(lst_night_filter, crs_sinu)
    lst_day_filter = hz.define_crs(lst_day_filter, crs_sinu)
    # fwi_filter = hz.define_crs(fwi_filter, crs_sinu)
    active_fire_filter = hz.define_crs(active_fire_filter, crs_sinu)
    burn_mask_filter = hz.define_crs(burn_mask_filter, crs_sinu)
    density = hz.define_crs(density, 4326)

    # Define the AOI
    aoi = hz.define_area_of_interest(path_data + 'Large.zip')

    # Clip the data sets to the AOI
    era_filter = hz.clip_to_aoi(era_filter, aoi)
    # fwi_filter = hz.clip_to_aoi(fwi_filter, aoi)
    density = hz.clip_to_aoi(density, aoi)

    #   Definition of the common grid
    common_grid = rxr.open_rasterio(path_data + 'final_lst_day_1D_1km.nc').isel(time=0)

    # Downsample the era data to a daily resolution before regridding
    era_filter_daily = hz.resample_to_daily(era_filter)
    # Projection of the era into sinuoidal projection
    era_sinu = era_filter_daily.rio.reproject(crs_sinu)

    # Renaming dimensions of era data set to match the other data sets
    # era_filter_proj = era_sinu.rename({'y': 'ydim', 'x': 'xdim'})

    # Regrid the era data to the common grid
    era_filter_proj = hz.interpolate_to_common_grid(era_sinu, common_grid)

    #  Resample the data sets to the common grid
    lai_filter_proj = hz.interpolate_to_common_grid(lai_filter, common_grid)

    evap_filter_proj = hz.interpolate_to_common_grid_categorical(evap_filter, common_grid)

    # fwi_filter_proj = hz.interpolate_to_common_grid(fwi_filter, common_grid)

    # Rename dataArrays before merging
    density.name = 'density'
    # change density_proj to xarray dataset
    density = density.to_dataset()
    density_proj = hz.interpolate_to_common_grid(density, common_grid)

    # Different method to interpolate the active fire data set
    active_fire_filter_proj = active_fire_filter.interp(ydim=ndvi["ydim"], xdim=ndvi['xdim'])

    # Pre-processing before daily interpolation
    # Deleting attribute grid_mapping of the burn_mask_filter data set
    del burn_mask_filter.attrs['grid_mapping']
    # Deleting attribute grid_mapping of the evap_filter_proj data set
    del evap_filter_proj.attrs['grid_mapping']

    # Resample to daily
    ndvi_filter_daily = hz.resample_to_daily(ndvi_filter)
    burn_mask_filter_daily = hz.resample_to_daily_categorical(burn_mask_filter)
    lai_filter_proj_daily = hz.resample_to_daily(lai_filter_proj)
    evap_filter_proj_daily = hz.resample_to_daily_categorical(evap_filter_proj)
    # fwi_filter_proj_daily = hz.resample_to_daily(fwi_filter_proj)
    active_fire_filter_proj_daily = hz.resample_to_daily(active_fire_filter_proj)

    # Create a list of the data sets
    data_sets = [ndvi_filter_daily, burn_mask_filter_daily, lai_filter_proj_daily, evap_filter_proj_daily,
                 era_filter_proj, active_fire_filter_proj_daily]

    # Subset all dataset from the list using sel method to '2010-02-01', '2022-01-01'
    data_sets = [ds.sel(time=slice('2011-02-01', '2021-01-01')) for ds in data_sets]

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

    # Match the coordinates values of the data sets
    ds_xdimydim_xdimydim = ds_xdimydim.assign_coords(xdim=ds_xy.coords['x'].values, ydim=ds_xy.coords['y'].values)

    # Renaming the coordinates of the data sets to match the other data sets
    ds_xdimydim_xdimydim= ds_xdimydim_xdimydim.rename({'xdim': 'x', 'ydim': 'y'})



    # Merge the data sets
    ds = xr.merge([ds_xy, ds_xdimydim_xdimydim])

    # Save the data set
    ds.to_netcdf(path_data + 'datacube.nc')
