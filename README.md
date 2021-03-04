![image](https://github.com/patternizer/iris-xarray-cartopy/blob/master/ukcp18.png)

# iris-xarray-cartopy

Python code to read in IRIS data cubes, convert coordinates to PlateCarree and apply extent for multipanel plots using Cartopy

## Contents

* `London_plot_comp.py` - python code to read in Iris 3.1 (scitools-iris.readthedocs.io) datacubes for a UKCP18 study and use iplt.contourf to display a 3-dataset comparison (Satyaban Bishoyi Ratna) 
* `iris-xarray-cartopy.py` - python code to read in Iris 3.1 datacubes, convert coordinates from OSGB to PlateCarree and apply (lat,lon) extent for multipanel plots using Cartopy
* `DATA/` - directory containing netCDF-4 datasets
* `PLOTS/` - directory containing generated PNG plots

The first step is to clone the latest iris-xarray-cartopy code and step into the check out directory as follows: 

    $ git clone https://github.com/patternizer/iris-xarray-cartopy.git
    $ cd iris-xarray-cartopy

### Using Standard Python

The code should run with the [standard CPython](https://www.python.org/downloads/) installation and was tested in a conda virtual environment running a 64-bit version of Python 3.8.5.

iris-xarray-cartopy scripts can be run from sources directly, once dependencies are satisfied. In addition to the python libraries imported in iris-xarray-cartopy.py it is necessary to have the Iris 3.1 datasets in your iris-xarray-cartopy/DATA directory. Change the flags in the 'Settings' part of the code for various plotting options.

Run with:

    $ python London_plot_comp.py
    $ python iris-xarray-cartopy.py

## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Satyaban Bishoyi Ratna](s.bishoyi-ratna@uea.ac.uk)
* [Michael Taylor](michael.a.taylor@uea.ac.uk)

