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
    path_data = "../data/Raw/"

    # Load the data set
    ndvi = xr.open_dataset(path_data + 'Raw_NDVI_16D_1km.nc')
    lai = xr.open_dataset(path_data + 'Raw_LAI_8D_500m.nc')
    evap = xr.open_dataset(path_data + 'Raw_Evap_8D_500m.nc')
    era = xr.open_dataset(path_data + 'Raw_weather_4H_9km.nc')
    lst_night = xr.open_dataset(path_data + 'Raw_LST_Night_1D_1km.nc')
    lst_day = xr.open_dataset(path_data + 'Raw_LST_Day_1D_1km.nc')
    active_fire = xr.open_dataset(path_data + 'Raw_ActiveFire_500m.nc')
    burn_mask = xr.open_dataset(path_data + 'Raw_BurnMask_1km.nc')
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
    active_fire_filter = active_fire[['First_Day', 'Last_Day']]
    burn_mask_filter = burn_mask['FireMask']

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
    aoi = hz.define_area_of_interest(path_data+'AreaOfInterest.zip')

    # Clip the data sets to the AOI
    era_filter = hz.clip_to_aoi(era_filter, aoi)
    # fwi_filter = hz.clip_to_aoi(fwi_filter, aoi)
    density = hz.clip_to_aoi(density, aoi)

    #   Definition of the common grid
    common_grid = rxr.open_rasterio(path_data+'Raw_LST_Day_1D_1km.nc').isel(time=0)

    # Downsample the era data to a daily resolution before regridding
    era_filter_daily = hz.resample_to_daily(era_filter)
    #Projection of the era into sinuoidal projection
    era_sinu = era_filter_daily.rio.reproject(crs_sinu)
    # Regrid the era data to the common grid
    era_filter_proj = hz.interpolate_to_common_grid(era_sinu, common_grid)


    #  Resample the data sets to the common grid
    lai_filter_proj = hz.interpolate_to_common_grid(lai_filter, common_grid)
    evap_filter_proj = hz.interpolate_to_common_grid(evap_filter, common_grid)
    # fwi_filter_proj = hz.interpolate_to_common_grid(fwi_filter, common_grid)
    density_proj = hz.interpolate_to_common_grid(density, common_grid)

    # Different method to interpolate the active fire data set
    active_fire_filter_proj = active_fire_filter.interp(ydim=ndvi["ydim"], xdim=ndvi['xdim'])


    # Resample to daily
    ndvi_filter_daily = hz.resample_to_daily(ndvi_filter)
    burn_mask_filter_daily = hz.resample_to_daily(burn_mask_filter)
    lai_filter_proj_daily = hz.resample_to_daily(lai_filter_proj)
    evap_filter_proj_daily = hz.resample_to_daily(evap_filter_proj)
    # fwi_filter_proj_daily = hz.resample_to_daily(fwi_filter_proj)
    active_fire_filter_proj_daily = hz.resample_to_daily(active_fire_filter_proj)

    # Create a list of the data sets
    data_sets = [ndvi_filter_daily, burn_mask_filter_daily, lai_filter_proj_daily, evap_filter_proj_daily, era_filter_proj, active_fire_filter_proj_daily]

    # Subset all dataset from the list using sel method to '2010-02-01', '2022-01-01'
    data_sets = [ds.sel(time=slice('2010-02-01', '2022-01-01')) for ds in data_sets]



    #Append the density data set to the list
    data_sets.append(density_proj)

    # Merge by coordinates the data sets
    data_merged = xr.combine_by_coords(data_sets, combine_attrs='drop_conflicts')

    # Save the data set
    data_merged.to_netcdf(path_data + 'data_merged.nc')









