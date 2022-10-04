# Datasets 


## Leaf Area Index from MOD15A2H v061([link](https://lpdaac.usgs.gov/products/mod15a2hv061/)):

**Start date:**  2009-12-27 00:00:00

**End date:**  2022-08-29 00:00:00

**Resolution:** 500m

**Projection:**  sinusoidal

**Spatial extent**: AOI

**Temporal granulometry:** 8 days

**List of variables:** 
- Fpar_500m: Fraction of Photosynthetically Active Radiation *(continuous)*
	-min: 0 
	-max: 2.54
    -unit: percentage

- Lai_500m:	Leaf Area Index *(continuous)*
 	-min: 0
	-max: 25.4 
    -unit: m²/m²

**Comment on Fpar and LAI:**

Leaf area index (LAI) and fraction of absorbed photosynthetically active radiation (fAPAR) are two biophysical
parameters that are closely related and often measured and validated in parallel in the field. LAI is typically
defined as the total one-sided area of leaf tissues per unit of ground surface area. Utilizing this definition,
LAI is a dimensionless unit which characterises the canopy of a given ecosystem (Breda, 2003). On the other
hand, fAPAR is defined as the fraction of photosynthetically active radiation (PAR) in the 400-700 nm
wavelengths that is absorbed by a canopy and it can include over-storey, understory and ground cover
elements.



- **FparStdDev_500m**: 	Standard deviation of FPAR *(continuous)*
	-min: 0 
	-max: 2.54
    -unit: percentage
    
- **LaiStdDev_500m:** Standard deviation of LAI *(continuous)*
 	-min: 0
	-max: 25.4 
    -unit: m²/m²
    
- **FparLai_QC:** Quality for LAI and FPAR *(categorical)*
 	-min: 0
	-max: 157 
    -unit: it needs to be converted into bit for interpretation

- **FparExtra_QC:** Extra detail Quality for LAI and FPAR *(categorical)*
 	-min: 0
	-max: 205 
    -unit: it needs to be converted into bit for interpretation

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/LAI_distrib.png?raw=true)
![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/LAI_plot.png?raw=true)

**Comments:** 
* The continuous variables  will be useful for the input of the model.Categorical for subesting depending on the quality.
* We can see that there is a strong correlation between LAI and FPAR (0.96 over time and spatial dimensions) and we will keep only Fpar has it has a more centered distribution value and closer to 0. It also emcompasses somehow the LAI.
* We notice the almost binary distribution of the stad deviation for Fpar an LAI. It might be because of the cities and the mountains. 
* We also otice we have categorical variable, so we could not interpolate with a bilinear or cubic resampling, so we will use the nearest neighbourhood method. The spatial extent is already crop to the PACA resolution but we do need updampling the temporal resolution and donwsampling the spatial resolution.

## NDVI from MOD13A2 v061([link](https://lpdaac.usgs.gov/products/mod13a2v061/)):

**Start date:**  2009-12-19 00:00:00

**End date:**  2022-08-13 00:00:00

**Resolution:** 1000m

**Projection:**  sinusoidal

**Spatial extent**: AOI

**Temporal granulometry:** 16 days

**projection:** sinusoidal

**List of variables:** 
- **_1_km_16_days_EVI: **Ehanced Vegetation Index *(continuous)*
 	-min: -02
	-max: 0.8983
    -unit: none

- **_1_km_16_days_NDVI:** Normalized Differentiation Vegetation Index *(continuous)*
 	-min: -02
	-max: 1
    -unit: none

- **_1_km_16_days_VI_Quality** *(categorical)*

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/NDVI_EVI_Quality_distrib.png?raw=true)

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/NDVI_EVI_Quality_plot.png?raw=true)



**Comments:** 
* EVI and NDVI have the same range of value but the EVI is centered whereas NDVI has a left skewdistribution
* We can see there is a strong correlation between NDVI and EVI (0.88 over time and spatial dimension), which is expected, and we will keep only EVI as it is an upgrade of the NDVI.

* There is almost an overlap with the quality of the data and with value around 0 for EVI and NDVI, so we need to have a closer look when preprocessing if we can take into account these value.
* Because of the categorical value of the quality variable we can't youse bilinear or cubic interpolation, we will use nearest to keep the same catgorical value.
* The spatial extent is already crop to the PACA extent but we do need updampling the temporal resolution


##  Evapotranspiration. MOD16A2 v061([link](https://lpdaac.usgs.gov/products/mod16a2v061/)):

**Start date:**  2009-12-27 00:00:00

**End date:**  2022-08-29 00:00:00

**Resolution:** 500m

**Projection:**  sinusoidal

**Spatial extent**: AOI

**Temporal granulometry:** 8 days

**List of variables:** 
-** ET_500m:** Total Evapotranspiration *(continuous)*
	-min: 0
	-max: 3.277e+03
    -unit: kg/m²/8day

- **LE_500m:**	Average Latent Heat Flux *(continuous)*
 	-min: 0
	-max: 3.277e+08
    -unit: J/m²/day


- **PET_500m:** 	Total Potential Evapotranspiration *(continuous)*
	-min: -0.4
	-max: 3.277e+03
    -unit: kg/m²/8day

- **PLE_500m:** Average Potential Latent Heat Flux *(continuous)*
 	-min: 0
	-max: 3.277e+08
    -unit: J/m²/day

- **ET_QC_500m:** Evapotranspiration Quality Control flags *(categorical)*
 	-min: 0
	-max: 
    -unit: it needs to be converted into bit for interpretation

**Comments**: 

ET is the mass of evaporated water per unit area per unit time, and LE is the latent heat flux, which is the energy flux associated with the evaporation of water. The two variables are strongly correlated, and we will keep only ET. There is no difference between the portential and actual. So we will keep only the ET_500m.


##  Meteorological data. ERA5-Land variables([link](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land?tab=overview)):

**Start date:**  2010-01-01 04:00:00

**End date:**  2022-07-31 20:00:00

**Resolution:** 9km

**Projection:**  WG84 --> EPSG 4326

**Spatial extent**: larger than the AOI --> need to be clipped

**Temporal granulometry:** 4 hours

**List of variables:** 

- **u10:** Eastward component of the 10m wind  *(continuous)*
	-min: -17.09
	-max: 15.15
    -unit: m/s

- **v10:**	Northward component of the 10m wind *(continuous)*
 	-min: -15.89
	-max: 14.17
    -unit: m/s


- **t2m:** 	Temperature of air at 2m above the surface of land, sea or in-land waters. *The temperature measured in kelvin can be converted to degrees Celsius (°C) by subtracting 273.15*. *(continuous)*
	-min: 244
	-max: 317
    -unit: K

- **tp:** precipitation *(continuous)*
 	-min: 0
	-max: 0.122
    -unit: m


**Comments**

Nothing to do with the data. However we need to project the dataset into a sinusoidal projection and clipping to the right AOI. We will aslo need to regridding to a 1km resoltuion and downsampling to a daily temporal resolution. We have to be careful and checking the dataset agin after all this transformation.


## Land Surface Temperature. MOD11A1 variables ([link](https://lpdaac.usgs.gov/products/mod11a1v061/)):

**Start date:**  2009-12-28 00:00:00

**End date:**  2022-09-01 00:00:00

**Resolution:** 1km

**Projection:**  sinusoidal

**Spatial extent**: AOI

**Temporal granulometry:** daily

**List of variables:** 

- LST_Day_1km: Land Surface Temperature day  *(continuous)*
	-min: 240.0
	-max: 332.9
    -unit: K

- LST_Night_1km:Land Surface Temperature day *(continuous)*
 	-min: 227.3
	-max: 321.2
    -unit: K
![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/lstdaynight.png?raw=true)


![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/lst_distrib.png?raw=true)

**Comments**
Nothing to do with the data.

## Fire Weather Index ([link](https://cds.climate.copernicus.eu/cdsapp#!/dataset/cems-fire-historical?tab=overview))

**Start date:**  2010-01-01 00:00:00

**End date:**  2022-12-31 00:00:00

**Resolution:** 0.25°

**Projection:**  rotated pole

**Spatial extent**: Europe

**Temporal granulometry:** daily

**List of variables:** 

- **FWI**: Fire Weather Index *(continuous)*
	-min: 1
	-max: 473
    -unit: dimensionless
    - comment:It is customary to quote a danger class as well as an index number. The fire weather index can be categorised into 6 classes of danger as follows: Very low danger: FWI is less than 5.2. Low danger: FWI is between 5.2 and 11.2. Moderate danger: FWI is between 11.2 and 21.3. High danger: FWI is between 21.3 and 38.0. Very high danger: FWI is between 38.0 and 50. Extreme danger: FWI is greater than 50.

![Quantième 150](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/fwi.png?raw=true)


**Comments**
need to change the extent and the projection

## Active fire variable ([link](https://lpdaac.usgs.gov/products/mcd64a1v061/)):

**Start date:**  2010-01-01 00:00:00

**End date:**  2022-02-01 00:00:00

**Resolution:** 500m

**Projection:**  sinusoidal

**Spatial extent**: AOI

**Temporal granulometry:** Monthly

**List of variables:** 

- Burn_Date: ordinal day of burn *(categorical)*
	-min: 0
	-max: 366
    -unit: day

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/Burn_date.png?raw=true)


**Comments:**
There is an issue with the formatting and a shift of 30 years exactly. Despite that, we observe the count of active fire seems to follow a pattern with more fire in estival period. However, I'm quite surprise to observe there are still so many fire all along the year.

- First_Day: First day of the year of reliable change detection *(categorical)*
	-min: 0
	-max: 366
    -unit: day

- Last_Day: Last day of the year of reliable change detection *(categorical)*
	-min: 0
	-max: 366
    -unit: day
- Burn_Date_Uncertainty: Estimated uncertainty in burn day *(categorical)*
	-min: 0
	-max: 100
    -unit: day
    
![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/FirstDay_LastDay_plot.png?raw=true)

**Comments:**
We can interpret that most of the fire extinguishe between day100 and day150 (Mars-April) and day250 to 325(October) and this is significant as it is the most rainy day.
We see also there is a peak for the first day around August, even if it is the 8th month.

- QA: Quality Assurance Indicators *(categorical)*
 	-min: 0
	-max: 
    -unit: it needs to be converted into bit for interpretation

**Comments**
Need to the grid and have a look on how we will merge. Indeed the time resolution is monthly, and the variables are days.**Warning** We will have a try on resample to a daily resolution, bu I have a doubt the pixel will keep the count rightly.

## Burned mask variables MYD14A2 [(link)](https://lpdaac.usgs.gov/products/myd14a2v061/)
The MYD14A2 gridded composite contains maximum value of individual fire pixel classes detected during the eight days of acquisition.

**Start date:**  2009-12-27 00:00:00

**End date:**  2022-08-29 00:00:00

**Resolution:** 1km

**Projection:**  sinusoidal

**Spatial extent**: AOI

**Temporal granulometry:** 8 days

**List of variables:** 

- **FireMask** *(categorical)*
Value	Description
0	Not processed (missing input data)
1	Not processed (obsolete; not used since Collection 1)
2	Not processed (other reason)
3	Non-fire water pixel
4	Cloud (land or water)
5	Non-fire land pixel
6	Unknown (land or water)
7	Fire (low confidence, land or water)
8	Fire (nominal confidence, land or water)
9	Fire (high confidence, land or water)

- **QA**: Quality Assurance Indicators *(categorical)*
Bit(s) Meaning
0-1 land/water state (00 = water, 01 = coast, 10 = land, 11 = unused)
2 3.9 µm high-gain flag (0 = band 21, 1 = band 22)
3 atmospheric correction performed (0 = no, 1 = yes)
4 day/night algorithm (0 = night, 1 = day)
5 potential fire pixel (0 = false, 1 = true)
6 spare (set to 0)
7-10 background window size parameter
11-16 individual detection test flags (0 = fail, 1 = pass)
17-19 spare (set to 0)
20 adjacent cloud pixel (0 = no, 1 = yes)
21 adjacent water pixel (0 = no, 1 = yes)
22-23 sun glint level (0–3)
24-28 individual rejection test flags (0 = false, 1 = true)
29-31 spare (set to 0)

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/percentage_fire.png?raw=true)


**Comments*
We see from the picture most of the time tere is no fire, so the final dataset may be very unbalanced.

## Density ([link)](https://hub.worldpop.org/geodata/listing?id=76)
**Resolution:** 1km

**Projection:**  WG84 EPSG 4326

**Spatial extent**: France

**Temporal granulometry:** none, one raster geotiff format. We Have check the geotiff for all the years from 2010 and 2022, and as it not change significantly, we will keep only the one from 2015 (in the middle)

**Count:**
* MAXIMUM:  53646.03515625
* MEAN:     119.46772920052
* MINIMUM:  0
* STDDEV:   644.66432858711

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/density.png?raw=true)

**Comments**: Need to be clipped into the AOI and project onti sinusoidal.

Start_date: 2010-01-01
End_date: 2022-02-01