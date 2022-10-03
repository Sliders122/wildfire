# Datasets 

## Dynamic data
### Leaf Area Index from MOD15A2H v061([link](https://lpdaac.usgs.gov/products/mod15a2hv061/)):

**Start date:**  2009-12-27 00:00:00

**End date:**  2022-08-29 00:00:00

**Resolution:** 500m

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


- FparStdDev_500m: 	Standard deviation of FPAR *(continuous)*
	-min: 0 
	-max: 2.54
    -unit: percentage
    
- LaiStdDev_500m: Standard deviation of LAI *(continuous)*
 	-min: 0
	-max: 25.4 
    -unit: m²/m²
    
- FparLai_QC: Quality for LAI and FPAR *(categorical)*
 	-min: 0
	-max: 157 
    -unit: it needs to be converted into bit for interpretation

- FparExtra_QC: Extra detail Quality for LAI and FPAR *(categorical)*
 	-min: 0
	-max: 205 
    -unit: it needs to be converted into bit for interpretation

**Comments:** The continuous variables  will be useful for the input of the model.Categorical for subesting depending on the qulity. We also notice by plotting there might be strong correlation between them, so we may remove them after further analysis with a correlation matrix. We also otice we have categorical variable, so we could not interpolate with a bilinear or cubic resampling, so we will use the nearest neighbourhood method. The spatial extent is already crop to the PACA resolution but we do need updampling the temporal resolution and donwsampling the spatial resolution.

### NDVI from MOD13A2 v061([link](https://lpdaac.usgs.gov/products/mod13a2v061/)):

**Start date:**  2009-12-19 00:00:00

**End date:**  2022-08-13 00:00:00

**Resolution:** 1000m

**Temporal granulometry:** 16 days

**projection:** sinusoidal

**List of variables:** 
- _1_km_16_days_EVI: Ehanced Vegetation Index
 	-min: -02
	-max: 0.8983
    -unit: none

- _1_km_16_days_NDVI: Normalized Differentiation Vegetation Index
 	-min: -02
	-max: 1
    -unit: none

- _1_km_16_days_VI_Quality

**Comments:** 
EVI and NDVI have the same range of value but the EVI is centered whereas NDVI has a left skewdistribution
The continuous variables  will be useful for the input of the model.Categorical for subesting depending on the qulity. We also notice by plotting there might be strong correlation between them, so we may remove them after further analysis with a correlation matrix. We also otice we have categorical variable, so we could not interpolate with a bilinear or cubic resampling, so we will use the nearest neighbourhood method. The spatial extent is already crop to the PACA resolution but we do need updampling the temporal resolution and donwsampling the spatial resolution.
