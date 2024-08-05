# TESLA-kit Coastal risk assessment 

Teslakit is a Python3 collection of libraries for numerical and statistical calculations and methodologies for handling global climate data.

The stochastic climate emulator proposed is built on the recognition that coastal conditions are the result of meteorological forcing, and that synoptic-scale meteorology is in turn a consequence of large-scale quasi-steady atmospheric and oceanic patterns (e.g., Anderson et al. 2019)


## Main contents

teslakit modules:

- [alr](./teslakit/alr.py) AutoRegressive Logistic Model customized wrapper
- [climate\_emulator](./teslakit/climate_emulator.py) DWTs-Waves Extremes Statistical Emulator (GEV, Gumbel, Weibull)
- [estela](./teslakit/estela.py) SLP ESTELA Predictor module
- [extremes](./teslakit/extremes.py) Extremes Statistics library
- [intradaily](./teslakit/intradaily.py) Intradaily Hydrographs library
- [kma](./teslakit/kma.py) KMeans Classification library 
- [mda](./teslakit/mda.py) MaxDiss Classification library 
- [mjo](./teslakit/mjo.py) Madden-Julian Oscilation data functions 
- [pca](./teslakit/pca.py) Customized Principal Component Analysis library 
- [rbf](./teslakit/rbf.py) Radial Basis Function library 
- [statistical](./teslakit/statistical.py) statistical multipurpose module: KDE,
  GeneralizedPareto, Empirical Kernels for copula fit and simulation
- [storms](./teslakit/storms.py) storms and tropical cyclones library
- [tides](./teslakit/tides.py) tides functions library
- [waves](./teslakit/waves.py) waves functions library

- [plotting](./teslakit/plotting/) set of modules for teslakit data and output plotting 
- [database](./teslakit/database.py) custom database developed to ease the multiple files required for a teslakit site 

databases:

- Sea Surface Temperature (SST): https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/netcdf/
- Madden-Julian Oscillation (MJO): http://www.bom.gov.au/climate/mjo/ 
- Tropical Cyclones (TCs): https://www.ncdc.noaa.gov/ibtracs/
- Waves Spectra (WVS): http://data-cbr.csiro.au/thredds/catalog/catch_all/CMAR_CAWCR-Wave_archive/CAWCR_Wave_Hindcast_aggregate/spec/catalog.xml


## Documentation

Anderson, D., Rueda, A., Cagigal, L., Antolinez, J. A. A., Mendez, F. J., & Ruggiero, P. (2019). Time‐varying emulator for short and long‐term analysis of coastal flood hazard potential. Journal of Geophysical Research: Oceans, 124. https://doi.org/10.1029/2019JC015312

Anderson, D., Ruggiero, P., Mendez, F. J., Rueda, A., Antolinez, J. A., Cagigal, L., Storlazzi, C., Barnard, P., & Marra, J. (2018). TIME-VARYING EMULATOR FOR SHORT- AND LONG-TERM ANALYSIS OF COASTAL FLOODING (TESLA-FLOOD). Coastal Engineering Proceedings, 1(36), currents.4. https://doi.org/10.9753/icce.v36.currents.4

Rueda, Hegermiller, Antolinez, Camus, Vitousek, Ruggiero, Barnard, Erikson, Tomas, Mendez (2017): Multi-scale climate emulator of multimodal wave spectra: MUSCLE-spectra, J. Geophy. Res. Oceans, vol. 122, pp 1400-1415.

Serafin, Ruggiero (2014): Simulating extreme total water levels using a time-dependent, extreme value approach. J. Geophys. Res. Oceans, vol. 119, pp. 6305-6329.


## Install 
- - -

Source code is currently privately hosted on GitLab at:  https://gitlab.com/geoocean/bluemath/bluemath-projects/teslakit/tree/master 

A public "push" mirror can be located on GitHub at: https://github.com/teslakit/teslakit/tree/master 

Teslakit-SF was originally run on a Linux OS. 
PermissionErrors may be encountered when writing to .nc files if not using Linux OS.

For Linux installation instructions on Windows see: https://learn.microsoft.com/en-us/linux/install.
If using WSL for teslakit, modify all path references by adding the prefix "/mnt/".

For Linux installation instruction on Mac see: https://www.hellotech.com/guide/for/how-to-install-linux-on-mac

If teslakit cannot be run on Linux OS, download Miniconda: https://docs.anaconda.com/miniconda/


### Environment setup

Using a Python virtual environment is recommended


### For Linux:
Open Command Prompt
Navigate to the base root of [teslakit](./)
```
#install virtualenv package 
python3 -m pip install virtualenv

#create a new virtual environment for teslakit installation
#ensure python 3.7 is installed
python3 -m venv --python=python3.7 teslakit_env

#now activate the virtual environment
source teslakit_env/bin/activate


#now  install teslakit requirements
pip install -r requirements/requirements.txt


#then install teslakit
python setup.py install
```


### For Miniconda
Open Miniconda Prompt
Navigate to the base root of [teslakit](./)
```
#create a new virtual environment for teslakit installation
#ensure python 3.7 is installed
conda create --name teslakit_env python=3.7


#now activate the virtual environment
conda activate teslakit_env


#now  install teslakit requirements
pip install -r requirements/requirements.txt


#then install teslakit
python setup.py install
```


### Installing optional modules

Basemap module is used in some Teslakit figures.

It is not needed to run any calculation and installing it is optional

Follow Basemap installation instructions at https://github.com/matplotlib/basemap

```
pip install git+https://github.com/matplotlib/basemap.git
```

## Handling a Teslakit Project 
- - -

Jupyter notebook files can be found at [notebooks](notebooks/)

launch jupyter notebook
```
jupyter notebook
```
or if you use an IDE
```
code .
```

Current development test site notebooks can be found at [SF](notebooks/SF/)

Input data acquisition is currently not integrated in teslakit

### Updating Configuration File and Running Notebooks

Open [input_configuration](./input_configuration.py) and fill in the input variables.
*Note - the input_configuration only contains global input variables. Each notebook may contain varying/unique input values (e.g. simulation dates, coordinates, coefficients, etc.). Review these input values before running the associated code cell.*

Once data is downloaded and unpacked, an input data check can be done at: [00_Set_Database.ipynb](notebooks/SF/01_Offshore/00_Set_Database.ipynb).
Place input data files in paths described in this notebook.
San Francisco input data can be found at [teslakit-SF_data](https://github.com/cadillac-desert/teslakit-SF_data).


## Contributors

Nicolás Ripoll Cabarga (nicolas.ripoll@unican.es)\
Ana Cristina Rueda Zamora (anacristina.rueda@unican.es)\
Laura Cagigal Gil (laura.cagigal@unican.es)\
Alba Cid Carrera (alba.cid@unican.es)\
Alba Ricondo Cueva (alba.ricondo@unican.es)\
Sara Ortega Van Vloten (sara.ortegav@unican.es)\
Israel Rubio Llarena (israel.rubio@unican.es)\
Fernando Mendez Incera (fernando.mendez@unican.es)


## License

This project is licensed under the MIT License - see the [license](LICENSE.txt) file for details


## Disclaimer

These notebooks encompass various aspects of the comprehensive weather generation process associated with Teslakit. The scripts that are part of this installation are tailored for an example San Francisco site.  Each simulation and process involves distinct input parameters that can vary across different sites, notebooks, and runs. The current values assigned to these input variables have been tested and demonstrated to run successfully. Altering these variables may impact the results and potentially lead to errors in the notebooks. 




