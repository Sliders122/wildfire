# WildFire Forecast: a geospatial datascience project

## Table of Content

[TOC]

## Name

WildFire forecast

## Description

The aim of this project is to build 2 applications:
- One application to visualize a risk map for predicted fire ignition localisation in the next day. This tools is meant to be used to help firefighters to better organize their ressources.
- A second application to go deeper in the explanation of the model. This meant to be used to test the resilience of the model and to understand on a longer term how can we decrease the risk.


## Pipeline

We collect data from satellite imagery, reanalysis and vector drawing. Then we process this data to merge same in a unique datacube. From this datacube, we can easily extract a dataframe wich will be used for model training and prediction.
Finally , the risk map will be deploy on a PowerBi Service, and the dashboard application to explain the feature importance on a AWS server.

![](https://github.com/Sliders122/wildfire/blob/main/resources/Image/data_pipeline.png?raw=true)


## Structure of the project

###GitHub: main branch

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
		
	- [model](https://github.com/Sliders122/wildfire/tree/main/src/model) 
input: dataframe  
output: dataframe+modèle
		- modelize.py
		- model_selection.ipynb
		- model.pkl

## Installation

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

## Usage

Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap

If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing

State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment

Luigi GIANNETTI - luigi.giannetti1@gmail.com
Quentin VOITURON - Quentin.voituron@gadz.org
Sascha MOCCOZET - saschamoccozet.pro@posteo.net

## License

For open source projects, say how it is licensed.

## Project status

Work in progress

## Context

This project is done in collaboration with the DataScience Tech Institute https://www.datasciencetech.institute/fr/. It is an evaluated project organised by Assan SANOGO.
