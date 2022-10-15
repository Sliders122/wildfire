# WildFire Forecast

## Name
WildFire forecast

## Description
The aim of this project is to create an Artificial Inteligence Model that will be able to predict fire in the PACA (France) region

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
One difficulties of the project is to manage the depedencies. We work under a windows OS, with python 3.9 +.
To manage the dependencies it is recommanded to use a conda environement and use conda forge in first choice. The advantage of using the conda package manager is that it provides pre-built binaries for all the required and optional dependencies for Rasterio, Xarray and geopandas.

First add `conda-forge` to your channels with:
```
copy conda config --add channels conda-forge
copy conda config --set channel_priority strict
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
