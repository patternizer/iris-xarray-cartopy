#! /usr/bin python

#------------------------------------------------------------------------------
# PROGRAM: London_plot_comp.py
#------------------------------------------------------------------------------
# Version 0.1
# 3 March, 2021
# Satyaban Bishoyi Ratna & Michael Taylor
# s DOT bishoyi-ratna AT uea DOT ac DOT uk
# michael DOT a DOT taylor AT uea DOT ac DOT uk 
#------------------------------------------------------------------------------

import iris
import iris.analysis
import iris.plot as iplt
import matplotlib.pyplot as plt
import iris.quickplot as qplt
import numpy as np

file1 = 'DATA/tas_hadukgrid_uk_1km.nc'          # MT: load data from DATA/ directory
file2 = 'DATA/tas_rcp85_land-cpm_uk_2.2km.nc'   # MT: load data from DATA/ directory
file3 = 'DATA/tas_rcp85_land-rcm_uk_12km.nc'    # MT: load data from DATA/ directory
hadk = iris.load(file1)
cpm = iris.load(file2)
rcm = iris.load(file3)
print(hadk)
print(cpm)
print(rcm)
#tas1 = hadk[1]
#print(tas1)

hadkcpm = hadk[0].regrid(cpm[1], iris.analysis.Linear())
rcmcpm = rcm[1].regrid(cpm[1], iris.analysis.Linear())
##cubesnew = cubes1.regrid(cubes2, iris.analysis.Linear())
print(hadkcpm)
print(rcmcpm)

plt.figure(figsize=(10,10))

#anom_cmap = 'bwr'
anom_cmap = 'brewer_YlOrRd_09'
#levels = [-2, 0, 2, 4, 6, 8, 10, 12]
levels = np.arange(-4, 14, 0.5)

plt.subplot(1, 3, 1)
fig1 = iplt.contourf(hadkcpm[0,:,:], levels, cmap=anom_cmap)
plt.title('HadUK')
ax = plt.gca()
ax.coastlines(resolution='50m')
#ax.gridlines()

plt.subplot(1, 3, 2)
fig2 = iplt.contourf(cpm[1][0,0,:,:], levels, cmap=anom_cmap)
plt.title('CPM')
ax = plt.gca()
ax.coastlines(resolution='50m')
#ax.gridlines()

plt.subplot(1, 3, 3)
fig3 = iplt.contourf(rcmcpm[0,0,:,:], levels, cmap=anom_cmap)
plt.title('RCM')
ax = plt.gca()
ax.coastlines(resolution='50m')
#ax.gridlines()

#bar = plt.colorbar(fig1, orientation='horizontal')
plt.colorbar(orientation='horizontal')
#bar.set_ticks(tick_levels)

#plt.tight_layout()
#plt.show()
plt.savefig('PLOTS/London_plot_comp.png')       # MT: save PNG to PLOTS/ directory

