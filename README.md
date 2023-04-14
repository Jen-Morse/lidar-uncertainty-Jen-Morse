LiDAR Uncertainty at two NEON Field Sites

This repository contains files to load and plot tree height data for comparison between in situ and LiDAR estimated data sets from two National Ecological Observatory Network (NEON) Field Sites in California, United States:

 -[SJER](https://www.neonscience.org/field-sites/sjer)
 -[SOAP](https://www.neonscience.org/field-sites/soap)

 Data for this comparison is provided by CU Boulder Earth Lab's Earthpy Data Subsets, and uses data from the 
spatail-vector-lidar data set. More documentation and how to use the earthpy.data.get_data() function can be found at
https://earthpy.readthedocs.io/en/latest/earthpy-data-subsets.html

spatial-vector-lidar

This dataset contains vector and Lidar data This includes a subset of spatial data for the California Madera County and NEON Soaproot Saddle (SOAP) and San Joaquin Experimental Range (SJER) sites in California. There are also some other general spatial boundary layers from natural earth, including global roads, political boundaries, and populated places. Finally, there are NEON Lidar data and insitu measurements for SOAP and SJER sites.


Contents:

*environment.yml file

*Img folder with .png files of images for each site

*lidar-uncertainty.ipynb notebook to load and plot data

*dataloaders.py file with classes and functions to load and clean data sets

*lisence MIT from github

*.gitignore default python from github

*.devcontatiner to load environment (needed to run this repository with github codespaces)

    To set up the earth analytics python environment with the environment.yml file, 
    follow the instructions on earthdatascience.org:
https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/

