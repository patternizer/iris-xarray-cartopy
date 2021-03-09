#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: rotated-pole-transform.py
#------------------------------------------------------------------------------
# Version 0.1
# 5 March, 2021
# Satyaban Bishoyi Ratna & Michael Taylor
# s DOT bishoyi-ratna AT uea DOT ac DOT uk
# michael DOT a DOT taylor AT uea DOT ac DOT uk 
#------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
# IMPORT PYTHON LIBRARIES
# ---------------------------------------------------------------------------------------------------------

from math import *
import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import iris.analysis
import cartopy.crs as ccrs
import cartopy.feature as cf
#from cartopy.io import shapereader
#from cartopy.util import add_cyclic_point
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# Silence library version change notifications
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
matplotlib.rcParams['mpl_toolkits.legacy_colorbar'] = False

# ---------------------------------------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------------------------------------

datacube = 'DATA/tas_rcp85_land-cpm_uk_2.2km.nc'

# Plot settings:
cmap = 'YlOrRd'
fontsize = 12
levels = np.arange(-4, 14, 0.5)
x0 = -0.60; x1 = 0.70; # London region extent (longitude)
y0 = 51.10; y1 = 51.85 # London region extent (latitude)

# Runtime flags (True / False):
plot_datacube = True

# ---------------------------------------------------------------------------------------------------------
# METHODS
# ---------------------------------------------------------------------------------------------------------

def rotated_grid_transform(grid_in, option, SP_coor):

    lon = grid_in[0]
    lat = grid_in[1];
    lon = (lon*pi)/180; # Convert degrees to radians
    lat = (lat*pi)/180;
    SP_lon = SP_coor[0];
    SP_lat = SP_coor[1];
    theta = 90+SP_lat; # Rotation around y-axis
    phi = SP_lon; # Rotation around z-axis
    theta = (theta*pi)/180;
    phi = (phi*pi)/180; # Convert degrees to radians
    x = cos(lon)*cos(lat); # Convert from spherical to cartesian coordinates
    y = sin(lon)*cos(lat);
    z = sin(lat);
    if option == 1: # Regular -> Rotated
        x_new = cos(theta)*cos(phi)*x + cos(theta)*sin(phi)*y + sin(theta)*z;
        y_new = -sin(phi)*x + cos(phi)*y;
        z_new = -sin(theta)*cos(phi)*x - sin(theta)*sin(phi)*y + cos(theta)*z;
    else:  # Rotated -> Regular
        phi = -phi;
        theta = -theta;
        x_new = cos(theta)*cos(phi)*x + sin(phi)*y + sin(theta)*cos(phi)*z;
        y_new = -cos(theta)*sin(phi)*x + cos(phi)*y - sin(theta)*sin(phi)*z;
        z_new = -sin(theta)*x + cos(theta)*z;
    lon_new = atan2(y_new,x_new); # Convert cartesian back to spherical coordinates
    lat_new = asin(z_new);
    lon_new = (lon_new*180)/pi; # Convert radians back to degrees
    lat_new = (lat_new*180)/pi;

    return lon_new,lat_new

def plot_cartopy(lon,lat,val,levels,cmap,fontsize,titlestr,figstr):

    # Generic cartopy contour plotting function

    print('generating Cartopy contour plot ...')

    fig  = plt.figure(figsize=(10,10))
    ax = plt.axes(projection=ccrs.PlateCarree())
    cp = plt.contourf(lon, lat, val, levels, transform=ccrs.PlateCarree(), zorder=0, alpha=0.65, cmap=cmap)        
    cb = plt.colorbar(cp, orientation="vertical", shrink=0.5, pad=0.05)            
    ax.add_feature(cf.LAND)        
    ax.add_feature(cf.OCEAN)        
    ax.add_feature(cf.COASTLINE)        
    ax.add_feature(cf.BORDERS, linestyle=':')        
    ax.set_extent([x0, x1, y0, y1])        
    plt.title(titlestr, fontsize=fontsize)        
    plt.savefig(figstr)

# ---------------------------------------------------------------------------------------------------------
# LOAD: datacubes into Xarray and define regridded datasets 
# ---------------------------------------------------------------------------------------------------------

print('loading datacubes into Xarray ...')

cpm = xr.open_dataset(datacube2, decode_cf=True)

#Out[82]: (6, 10, 2, 484, 606, 1)

#np.shape(cpm.tas)  --> (10, 1, 606, 484)

val = cpm.tas[0,0,:,:]    # NB: (longitude,latitude) in RotatedPole coords

print('convert from datacube coords to rotated pole to Cartesian ...')

lon = []
lat = []
for i in range(val.longitude.shape[0]):
    for j in range(val.longitude.shape[1]):                  
        lon.append(rotated_grid_transform((0,0), 1, (val.longitude[i,j].values, val.longitude[i,j].values)))
        lat.append(rotated_grid_transform((0,0), 1, (val.latitude[i,j].values, val.latitude[i,j].values)))

# ---------------------------------------------------------------------------------------------------------
# PLOTS
# ---------------------------------------------------------------------------------------------------------

if plot_datacube == True:

    titlestr = 'CPM'; figstr = 'PLOTS/ukcp18-london-cartopy-cpm.png'
    plot_cartopy(lon,lat,val,levels,cmap,fontsize,titlestr,figstr)

# ------------------------------------------------------------------------------------------------------------------
print('** END')

