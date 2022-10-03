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

**Comments:** The continuous variables  will be useful for the input of the model. We also notice by plotting there might be strong correlation between them, so we may remove them after further analysis with a correlation matrix. We also otice we have categorical variable, so we could not interpolate with a bilinear or cubic resampling, so we will use the nearest neighbourhood method. The spatial extent is already crop to the PACA resolution but we do need updampling the temporal resolution and donwsampling the spatial resolution.

### NDVI from MOD13A2 v061([link](https://lpdaac.usgs.gov/products/mod13a2v061/)):

**Start date:**  2009-12-27 00:00:00

**End date:**  2022-08-29 00:00:00

**Resolution:** 500m

**Temporal granulometry:** 8 days

**List of variables:** 
- Fpar_500m: 
- Lai_500m
- FparLai_QC
- FparExtra_QC
- FparStdDev_500m
- LaiStdDev_500m
