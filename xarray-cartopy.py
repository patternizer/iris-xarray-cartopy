#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: xarray-cartopy.py --> --> Xarray only code using Cartopy to plot
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
#from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# Silence library version change notifications
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
matplotlib.rcParams['mpl_toolkits.legacy_colorbar'] = False

# ---------------------------------------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------------------------------------

datacube1 = 'DATA/tas_hadukgrid_uk_1km.nc'
datacube2 = 'DATA/tas_rcp85_land-cpm_uk_2.2km.nc'
datacube3 = 'DATA/tas_rcp85_land-rcm_uk_12km.nc'

# Plot settings:
cmap = 'brewer_YlOrRd_09'
fontsize = 12
levels = np.arange(-4, 14, 0.5)
x0 = -0.60; x1 = 0.70; # London region extent (longitude)
y0 = 51.10; y1 = 51.85 # London region extent (latitude)

# Runtime flags (True / False):
plot_uk_xarray = True
plot_london_cartopy = True

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

hadk = xr.open_dataset(datacube1, decode_cf=True)
cpm = xr.open_dataset(datacube2, decode_cf=True)
rcm = xr.open_dataset(datacube3, decode_cf=True)

#np.shape(hadk.tas) --> (10, 1450, 900)
#np.shape(cpm.tas)  --> (10, 1, 606, 484)
#np.shape(rcm.tas)  --> (10, 1, 112, 82)

data1 = hadk.tas[0,:,:]
data2 = cpm.tas[0,0,:,:]
data3 = rcm.tas[0,0,:,:]

print('convert from rotated pole to Cartesian ...')

# rotated_grid_transform((0,0), 1, (0,0))

print('regridding datacubes in Xarray ...')

# Get CPM grid:

#new_lon = np.linspace(cpm_tas.projection_x_coordinate[0], cpm_tas.projection_x_coordinate[-1], int(len(cpm_tas.projection_x_coordinate)))
#new_lat = np.linspace(cpm_tas.projection_y_coordinate[0], cpm_tas.projection_y_coordinate[-1], int(len(cpm_tas.projection_y_coordinate)))
new_lon = np.linspace(cpm.grid_longitude[0], cpm.grid_longitude[-1], int(len(cpm.grid_longitude)))
new_lat = np.linspace(cpm.grid_latitude[0], cpm.grid_latitude[-1], int(len(cpm.grid_latitude)))

# Regrid using CPM grid:
 
hadkcpm = hadk.interp(projection_y_coordinate=new_lat, projection_x_coordinate=new_lon)
rcmcpm = rcm.interp(projection_y_coordinate=new_lat, projection_x_coordinate=new_lon)

data1 = hadkcpm
data2 = cpm
data3 = rcmcpm

fig, axes = plt.subplots(ncols=2, figsize=(10, 4))
hadk.plot(ax=axes[0])
axes[0].set_title("Raw data")
hadkcpm.plot(ax=axes[1])
axes[1].set_title("Interpolated data")

# ---------------------------------------------------------------------------------------------------------
# PLOTS
# ---------------------------------------------------------------------------------------------------------

if plot_uk_iplt == True:

    print('generating Iris contour plot ...')

    figstr = 'ukcp18-iplt.png'

    plt.figure(figsize=(10,10))
    plt.subplot(1, 3, 1)
    fig1 = iplt.contourf(data1, levels, cmap=cmap); plt.title('HadUK', fontsize=fontsize)
    ax1 = plt.gca(); ax1.coastlines(resolution='50m')
    plt.subplot(1, 3, 2)
    fig2 = iplt.contourf(data2, levels, cmap=cmap); plt.title('CPM', fontsize=fontsize)
    ax2 = plt.gca(); ax2.coastlines(resolution='50m')
    plt.subplot(1, 3, 3)
    fig3 = iplt.contourf(data3, levels, cmap=cmap); plt.title('RCM', fontsize=fontsize)
    ax3 = plt.gca(); ax3.coastlines(resolution='50m')
    plt.colorbar(orientation='horizontal')
    plt.savefig(figstr)

if plot_uk_xarray == True:

    print('generating Matplotlib Xarray contour plot ...')

    figstr = 'ukcp18-xarray.png'

    fig = plt.figure(figsize=(10, 10))
    grid = AxesGrid(fig, 111, nrows_ncols=(1, 3),
                    axes_pad=0.05,
                    cbar_mode='single', cbar_location='right', cbar_pad=0.1)
    j=0
    for ax in grid:
        ax.set_axis_off()
        if j == 0:
            fig1 = ax.contourf(xr.DataArray.from_iris(data1).values[:,:], levels, cmap=cmap)
            ax.set_title('HadUK', fontsize=fontsize)
        elif j == 1:
            fig2 = ax.contourf(xr.DataArray.from_iris(data2).values[:,:], levels, cmap=cmap)
            ax.set_title('CPM', fontsize=fontsize)
        elif j == 2:
            fig3 = ax.contourf(xr.DataArray.from_iris(data3).values[:,:], levels, cmap=cmap)
            ax.set_title('RCM', fontsize=fontsize)
        j += 1
    cbar = ax.cax.colorbar(fig3)
    plt.savefig(figstr)

if plot_london_cartopy == True:

    print('converting coords from OSGV to PlateCarree ...')
    lon, lat, val = convert_OSGB_PlateCarree(data1)

    titlestr = 'HadUK'; figstr = 'PLOTS/ukcp18-london-cartopy-hadkcpm.png'
    plot_cartopy(lon,lat,val,levels,cmap,fontsize,titlestr,figstr)

    print('converting coords from OSGV to PlateCarree ...')
    lon, lat, val = convert_OSGB_PlateCarree(data2)

    titlestr = 'CPM'; figstr = 'PLOTS/ukcp18-london-cartopy-cpm.png'
    plot_cartopy(lon,lat,val,levels,cmap,fontsize,titlestr,figstr)

    print('converting coords from OSGV to PlateCarree ...')
    lon, lat, val = convert_OSGB_PlateCarree(data3)

    titlestr = 'RCM'; figstr = 'PLOTS/ukcp18-london-cartopy-rcm.png'
    plot_cartopy(lon,lat,val,levels,cmap,fontsize,titlestr,figstr)

# ------------------------------------------------------------------------------------------------------------------
print('** END')

