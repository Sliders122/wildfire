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

**Comment on Fpar and LAI:**

Leaf area index (LAI) and fraction of absorbed photosynthetically active radiation (fAPAR) are two biophysical
parameters that are closely related and often measured and validated in parallel in the field. LAI is typically
defined as the total one-sided area of leaf tissues per unit of ground surface area. Utilizing this definition,
LAI is a dimensionless unit which characterises the canopy of a given ecosystem (Breda, 2003). On the other
hand, fAPAR is defined as the fraction of photosynthetically active radiation (PAR) in the 400-700 nm
wavelengths that is absorbed by a canopy and it can include over-storey, understory and ground cover
elements.



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

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/LAI_distrib.png?raw=true)
![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/LAI_plot.png?raw=true)

**Comments:** 
* The continuous variables  will be useful for the input of the model.Categorical for subesting depending on the quality.
* We can see that there is a strong correlation between LAI and FPAR (0.96 over time and spatial dimensions) and we will keep only Fpar has it has a more centered distribution value and closer to 0. It also emcompasses somehow the LAI.
* We notice the almost binary distribution of the stad deviation for Fpar an LAI. It might be because of the cities and the mountains. 
* We also otice we have categorical variable, so we could not interpolate with a bilinear or cubic resampling, so we will use the nearest neighbourhood method. The spatial extent is already crop to the PACA resolution but we do need updampling the temporal resolution and donwsampling the spatial resolution.

### NDVI from MOD13A2 v061([link](https://lpdaac.usgs.gov/products/mod13a2v061/)):

**Start date:**  2009-12-19 00:00:00

**End date:**  2022-08-13 00:00:00

**Resolution:** 1000m

**Temporal granulometry:** 16 days

**projection:** sinusoidal

**List of variables:** 
- _1_km_16_days_EVI: Ehanced Vegetation Index *(continuous)*
 	-min: -02
	-max: 0.8983
    -unit: none

- _1_km_16_days_NDVI: Normalized Differentiation Vegetation Index *(continuous)*
 	-min: -02
	-max: 1
    -unit: none

- _1_km_16_days_VI_Quality *(categorical)*

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/NDVI_EVI_Quality_distrib.png?raw=true)

![](https://github.com/Sliders122/wildfire/blob/datacube/resources/Image/NDVI_EVI_Quality_plot.png?raw=true)



**Comments:** 
* EVI and NDVI have the same range of value but the EVI is centered whereas NDVI has a left skewdistribution
* We can see there is a strong correlation between NDVI and EVI (0.88 over time and spatial dimension), which is expected, and we will keep only EVI as it is an upgrade of the NDVI.

* There is almost an overlap with the quality of the data and with value around 0 for EVI and NDVI, so we need to have a closer look when preprocessing if we can take into account these value.
* Because of the categorical value of the quality variable we can't youse bilinear or cubic interpolation, we will use nearest to keep the same catgorical value.
* The spatial extent is already crop to the PACA extent but we do need updampling the temporal resolution


###  Evapotranspiration. MOD16A2 v061([link](https://lpdaac.usgs.gov/products/mod16a2v061/)):

**Start date:**  2009-12-27 00:00:00

**End date:**  2022-08-29 00:00:00

**Resolution:** 500m

**Temporal granulometry:** 8 days

**List of variables:** 
- ET_500m: Total Evapotranspiration *(continuous)*
	-min: 0
	-max: 3.277e+03
    -unit: kg/m²/8day

- LE_500m:	Average Latent Heat Flux *(continuous)*
 	-min: 0
	-max: 3.277e+08
    -unit: J/m²/day


- PET_500m: 	Total Potential Evapotranspiration *(continuous)*
	-min: -0.4
	-max: 3.277e+03
    -unit: kg/m²/8day

- PLE_500m: Average Potential Latent Heat Flux *(continuous)*
 	-min: 0
	-max: 3.277e+08
    -unit: J/m²/day

- ET_QC_500m: Evapotranspiration Quality Control flags *(categorical)*
 	-min: 0
	-max: 
    -unit: it needs to be converted into bit for interpretation

**Comments**: 

ET is the mass of evaporated water per unit area per unit time, and LE is the latent heat flux, which is the energy flux associated with the evaporation of water. The two variables are strongly correlated, and we will keep only ET. There is no difference between the portential and actual. So we will keep only the ET_500m.


###  Evapotranspiration. MOD16A2 v061([link](https://lpdaac.usgs.gov/products/mod16a2v061/)):

**Start date:**  2010-01-01 04:00:00

**End date:**  2022-07-31 20:00:00

**Resolution:** 9km

**Temporal granulometry:** 4 hours

**List of variables:** 

- u10: Eastward component of the 10m wind  *(continuous)*
	-min: -17.09
	-max: 15.15
    -unit: m/s

- v10:	Northward component of the 10m wind *(continuous)*
 	-min: -15.89
	-max: 14.17
    -unit: m/s


- t2m: 	Temperature of air at 2m above the surface of land, sea or in-land waters. *The temperature measured in kelvin can be converted to degrees Celsius (°C) by subtracting 273.15*. *(continuous)*
	-min: 244
	-max: 317
    -unit: K

- tp: precipitation *(continuous)*
 	-min: 0
	-max: 0.122
    -unit: m


**Comments**

ET is the mass of evaporated water per unit area per unit time, and LE is the latent heat flux, which is the energy flux associated with the evaporation of water. The two variables are strongly correlated, and we will keep only ET. There is no difference between the portential and actual. So we will keep only the ET_500m.
