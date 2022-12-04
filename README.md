

# WildFire Forecast: a geospatial datascience project

A presentation of the project is accessible in a powerpoint version in the section resources >Presentation -> [Wildfire forecast](https://github.com/Sliders122/wildfire/blob/main/resources/Presentation/Wildfire%20forecast.pptx)

## Table of Content

- [WildFire Forecast: a geospatial datascience project](#wildfire-forecast--a-geospatial-datascience-project)
  * [Table of Content](#table-of-content)
  * [Description](#description)
  * [Pipeline](#pipeline)
  * [Structure of the project](#structure-of-the-project)
  * [Installation](#installation)
    + [Environement for the Datacube creation](#environement-for-the-datacube-creation)
    + [Rasterio](#rasterio)
    + [Xarray](#xarray)
    + [Geopandas](#geopandas)
    + [Rioxarray](#rioxarray)
    + [Environement for building the model](#environement-for-building-the-model)
  * [Authors and acknowledgment](#authors-and-acknowledgment)
  * [Context](#context)

## Description

The aim of this project is to build 2 applications:
- One application to visualize a risk map to predict fire ignition localisations in the next day. This tools is meant to be used to help firefighters to better organize their ressources.
- A second application to go deeper in the explanation of the model. This meant to be used to test the resilience of the model and to understand on a longer term how can we decrease the risk.

The Area of Interest is the South East of France, and we have builtour model base on data from 2010 to 2021. The size of each pixel is  1day * 1km *1km.


## Pipeline

We collect data from satellites, reanalysis and vector drawings. These data comes in different structure (resolution, granularity, projection : more info in [Raw_data_desc.md](https://github.com/Sliders122/wildfire/blob/main/src/cube/Raw_data_desc.md)) and need to be harmonized before merge. The processing and the merge is done in [cube.py](https://github.com/Sliders122/wildfire/blob/main/src/cube/cube.py). From this datacube, we can extract a dataframe wich will be used for model training and prediction, we have decided to balance the data 50/50. It turns we have around 15k observations with no fires and 15k observations with fire. After conducted a model selection  (),  we have decided to keep a LightGBMH classifier as a good tradeoff between performance and speed of training. It is from this model we have deployed two applications.
Finally , the risk map will be deploy on a PowerBi Service, and the dashboard application to explain the feature importance on a AWS server.

![](https://github.com/Sliders122/wildfire/blob/main/resources/Image/data_pipeline.png?raw=true)


## Structure of the project


- **resources**
	- Images
	- Modis Documentation
	- Presentation: with the powerpoint presenation of the project
	- Tuto - Earth Data Analytics Online Certificate

- **src**: it follows the pipeline describe above Cube -> Dataframe -> Model -> Deployement
	- [cube](https://github.com/Sliders122/wildfire/tree/main/src/cube) --> everything about the cube. from collecting the data to build the final cube
		- [Explanation](https://github.com/Sliders122/wildfire/tree/main/src/cube/explanation): a list of Jupyter Notebook used to explain how we have build the cube and face difficulties
		- [Raw_data_desc.md](https://github.com/Sliders122/wildfire/blob/main/src/cube/Raw_data_desc.md): to provide an analysis of the data before processing
		- [cube.py](https://github.com/Sliders122/wildfire/blob/main/src/cube/cube.py): script to build the cube
		- [harmonize.py](https://github.com/Sliders122/wildfire/blob/main/src/cube/harmonize.py): module with all the builded functions used in the cube.py script

	- [dataframe](https://github.com/Sliders122/wildfire/tree/main/src/dataframe)
		- [dataframe.py](https://github.com/Sliders122/wildfire/blob/main/src/dataframe/dataframe.py) : script to create and save the dataframe from the datacube
		- [module_dataframe.py](https://github.com/Sliders122/wildfire/blob/main/src/dataframe/module_dataframe.py) : module with built functions used in the dataframe script
		- df_final.csv: output of the script
		
	- [model](https://github.com/Sliders122/wildfire/tree/main/src/model) 
		- modelize.py
		- model_selection.ipynb: exlanation of modele selection
		- model.pkl: modele selected : lightGBMH classifier

	- [deployement:](https://github.com/Sliders122/wildfire/tree/main/src/deployement)
		-	[powerbi_model.pbix](https://github.com/Sliders122/wildfire/blob/main/src/deployement/powerbi_model.pbix): the report to be download
		-	...

## Installation
We have to build two different virtual environement, one for building the cube and another one for the model.
As we have deployed the model on a docker, we do not enter in the detail on how to intall dependencies for the second environement. Nevertheless, building the cube, need careful attention while installing packages.

### Environement for the Datacube creation
One difficulties of the project is to manage the depedencies. We work under a windows OS, with python 3.9 +.
To manage the dependencies it is recommanded to use a conda environement and use conda forge in first choice. The advantage of using the conda package manager is that it provides pre-built binaries for all the required and optional dependencies for Rasterio, Xarray and geopandas.

First add `conda-forge` to your channels with:

```
conda config --add channels conda-forge
conda config --set channel_priority strict
```

### Rasterio

[(more info here)](https://github.com/conda-forge/rasterio-feedstock#installing-rasterio)

Once the `conda-forge` channel has been enabled, `rasterio` can be installed with `conda`:

```
conda install rasterio
```

### Xarray

Xarray Installation [(more info here)](https://docs.xarray.dev/en/stable/getting-started-guide/installing.html) if you haven't set conda forge as a priority channel, you can still mention it excplicitly

```
conda install -c conda-forge xarray dask netCDF4 bottleneck`
````

### Geopandas

[(more info here)](https://geopandas.org/en/stable/getting_started/install.html)

```
conda install --channel conda-forge geopandas
```

### Rioxarray

[(more info here)](https://github.com/conda-forge/rioxarray-feedstock)

```
conda install --channel conda-forge rioxarray
```

### Environement for building the model

No need for that, it has been deployed on a Docker with love, for you :) But in case of, it runs with python 3.8. 


## Authors and acknowledgment

Luigi GIANNETTI - luigi.giannetti1@gmail.com
Quentin VOITURON - Quentin.voituron@gadz.org
Sascha MOCCOZET - saschamoccozet.pro@posteo.net



## Context

This project is done in collaboration with the DataScience Tech Institute https://www.datasciencetech.institute/fr/. It is an evaluated project organised by Assan SANOGO.
