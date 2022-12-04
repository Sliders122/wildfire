# WildFire Forecast

## Name

WildFire forecast

## Description

The aim of this project is to create an Artificial Inteligence Model that will be able to predict fire in the PACA (France) region

![image.png](assets/image.png)

## Structure of the project

├── .github                     : CI/CD pipeline using GitHub Actions
|  └── workflows                : Contains yml files that trigger the workflows in GitHub Actions.
|       ├── docker_flask.yml
|       ├── docker_telegram.yml
|       ├── terraform.yml
|       └── unittests.yml
├── api                         : Python Flask REST API with Swagger
|   ├── helpers
|   ├── tests
|   ├── .dockerignore
|   ├── __init__.py
|   ├── app.py
|   ├── Dockerfile
|   ├── README.md
|   └── requirements.txt
├── generators                   : Sensor's data generators in real-time
|   ├── kafkaproducer
|   ├── raspberrypi
|   ├── sensors
|   ├── __init__.py
|   ├── pc.py
|   ├── raspberry.py
|   └── README.md
├── iac                         : Infrastructure as Code
|   ├── .terraform
|   ├── .gitignore
|   ├── config.tf
|   ├── data.tf
|   ├── main.tf
|   ├── outputs.tf
|   ├── terraform.tfstate
|   ├── terraform.tfstate.backup
|   ├── variables.tf
|   └── README.md               : Further explanations on IaC part
├── kafkaconsumer               : Kafka Consumer
|   ├── schemas
|   ├── .dockerignore
|   ├── __init__.py
|   ├── config.py
|   ├── consumer.py
|   ├── Dockerfile
|   ├── dynamodb.py
|   ├── main.py
|   ├── pc.py
|   ├── predictor.py
|   ├── raspberry.py
|   ├── README.md
|   └── requirements.txt
├── model                        : ML Modeling
|   ├── exported_models
|   ├── training_data
|   ├── __init__.py
|   ├── config.py
|   ├── data_retriever.py
|   ├── model.py
|   └── README.md
├── telegrambot                  : Telegram Bot for alerting and monitoring
|   ├── .dockerignore
|   ├── __init__.py
|   ├── config.py
|   ├── Dockerfile
|   ├── dynamodb_config.py
|   ├── main_telegram.py
|   ├── requirements.txt
|   ├── utils.py
|   └── README.md
├── image                       : Folder containing all the images used in the README.md files.
├── .env                        : File to store environment variables (not published)
├── .gitignore
├── README.md
├── requirements.txt            : File containing the library requirements to run the project locally
└── setup.py                    : Setup python file of the project

## Visuals

Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

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
