# Brian Blaylock
# 4/22/2016
# Plot TDWR radar and MesoWest Stations on Same Plot

# Had to convert the .nids TDWR radar files to a text file 
# using NOAA's Weather and Climate Toolkit
#   Download here: http://www.ncdc.noaa.gov/wct/
#   Data > Load Data > Local File -or- THREDDS
#   (If you use the THREDDS Server, I get radial velocity from this URL
#   http://thredds.ucar.edu/thredds/catalog/terminal/level3/TV0/SLC/20160203/catalog.xml)
#   List Files > Export > Select Output Format "ESRI ASCII GRID" and change the output directory
#   Next until done

# Place these converted ASCII files in the directory you run this script.

##---- Multiprocessing -------------------------------------------------------------------##
## There are a lot of data files for the two days of TDWR data that need to be plotted.
## We want to make these plots really fast, so use the multiprocessing module
## to create a separate plot on each available processor.
##      1) Place the plotting script in a function. 
##         The input (can only take one) is the file name of the data to be plotted
##      2) In the main program (bottom section of this script) 
##         a) creat a list of the file names (this simple loop is very fast)
##         b) count the number
##         c) creat the pool object p = multiprocessing.Pool(num_proc)
##         d) send each list item to the plot function with the pool function
## This method makes 475 plots in a few minutes rather than over an hour!!!
##---- Multiprocessing -------------------------------------------------------------------##


import multiprocessing #:)

import matplotlib.pyplot as plt
import numpy as np
import sys,getopt
#from netCDF4 import Dataset  # use scipy instead
from scipy.io import netcdf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes
#import mayavi.mlab as mlab #Used for 3d Plotting
import matplotlib.colors as mcolors
from functions_domains_models import *
from mesowest_stations_radius import *

 
# Set universal figure margins
width = 3.25
height = 4.5
plt.figure(1, figsize=(width,height))
plt.rc("figure.subplot", left = 0)
plt.rc("figure.subplot", right = 1)
plt.rc("figure.subplot", bottom = 0)
plt.rc("figure.subplot", top = 1)
#plt.tight_layout(pad=5.08)
       
        
## Get some geography data from our WRF runs
output_file = 'auxhist24_d02_2015-06-17_00:00:00'
spat= 'auxhist23_d02_2015-06-17_00:00:00'
# Open file in a netCDF reader   
directory = '/uufs/chpc.utah.edu/common/home/horel-group4/model/bblaylock/WRF3.7_urbanforest/DATA/more_trees/'
out_dir = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/MS/TDWR/fig/movie/multiprocess/'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
wrf_file_name = output_file #NC files are named differently in a windows system
print 'opening', directory+wrf_file_name
nc         = netcdf.netcdf_file(directory+wrf_file_name,'r')
nc_spatial = netcdf.netcdf_file(directory+spat,'r')


HGT = nc_spatial.variables['HGT'][0,:,:] #topography
landmask = nc_spatial.variables['LANDMASK'][0,:,:]
#-------------------------------------------
# Creat the basemap only once per domain. (This significantly speeds up the plotting speed)
#-------------------------------------------

# x_dim and y_dim are the x and y dimensions of the model
# domain in gridpoints
x_dim = nc.dimensions['west_east']
y_dim = nc.dimensions['south_north']

# Get the grid spacing
dx = float(nc.DX)
dy = float(nc.DY)

width_meters = dx * (x_dim - 1)		#Domain Width
height_meters = dy * (y_dim - 1)	#Domain Height


# Define the map boundaries lat/lon
domain = get_domain('salt_lake_valley')
top_right_lat = domain['top_right_lat']+.1
top_right_lon = domain['top_right_lon']-.1
bot_left_lat = domain['bot_left_lat']
bot_left_lon = domain['bot_left_lon']

## Map in cylindrical projection (data points may apear skewed)
m = Basemap(resolution='i',projection='cyl',\
    llcrnrlon=bot_left_lon,llcrnrlat=bot_left_lat,\
    urcrnrlon=top_right_lon,urcrnrlat=top_right_lat,)
 


# This sets the standard grid point structure at full resolution
#	Converts WRF lat and long to the maps x an y coordinate
XLONG = nc_spatial.variables['XLONG'][0]
XLAT  = nc_spatial.variables['XLAT'][0]
x,y = m(XLONG,XLAT)    
    
    ## Plot a map for each TDWR radial velocity file
    # list ascii radar files in directory, plot data


def make_plot(i):    

    print i
    radar_time = i[8:23]
    
    DATETIME = datetime.datetime.strptime(radar_time,"%Y%m%d_%H%M%S")
    mesowest_time = DATETIME.strftime("%Y%m%d%H%M")
    
    string_time = DATETIME.strftime('%d %b %Y  %H:%M UTC')
    
    
    ### TDWR Radar Data (converted from .nids to .asc grid)
    text = 'SLC_TV0_'+radar_time+'.asc'
    this = np.flipud(np.genfromtxt(text,skip_header=6)) #flip the array        
    
    # Get from Data from .asc file header
    NCOLS = 800
    NROWS = 510
    XLLCORNER = -112.8279915
    YLLCORNER = 40.0570686
    CELLSIZE = 0.0025073
    NODATA_VALUE = -999.0000000
    
    # replace no data with nan
    this[this==800]=0.
    this[this==-999]=0.
    
    # convert from knots to m/s
    this = this*0.514
    
    # Mask the zero values so we can see the terrain in the background
    this = np.ma.masked_where(this == 0, this)
    
    # Array of lats and lons        
    lats = np.linspace(YLLCORNER,YLLCORNER+CELLSIZE*NROWS,NROWS)
    lons = np.linspace(XLLCORNER,XLLCORNER+CELLSIZE*NCOLS,NCOLS)
    
    ## Begin the Plot

    # terrain and lake mask
    m.contourf(x,y,HGT,levels=np.arange(1000,4000,500),cmap=plt.get_cmap('binary'))        
    plt.contour(x,y,landmask, [0,1], linewidths=1.5, colors="b")        
    
    # radar data
    m.pcolormesh(lons,lats,this,cmap='BrBG',vmax=10,vmin=-10)
    #cbar_loc = plt.colorbar(shrink=.8,pad=.02,extend='both',orientation="horizontal")
    #cbar_loc.ax.set_xlabel('Radial Velocity (m/s)',fontsize=10)
    #cbar_loc.ax.tick_params(labelsize=8) 
    
    
    #m.drawcoastlines(color='blue',linewidth=2)
    #m.drawstates()
    
    # Location of TDWR and other observing stations for reference
    m.scatter(-111.93,40.9669, s=75, c='w',zorder=40)               # TDWR
    m.scatter(-112.01448,40.71152, s=75, c='b',zorder=40)           # NAA
    m.scatter(-111.93072,40.95733, s=75, c='darkorange',zorder=40)  # O3S02                        
    m.scatter(-111.828211,40.766573, s=75, c='r',zorder=40)         # MTMET                       
    m.scatter(-111.8717,40.7335, s=75, c='darkgreen',zorder=40)     # QHW               
    m.scatter(-111.96503,40.77069, s=75, c='w',zorder=40)           # SLC               
    m.scatter(-112.34551,40.89068 , s=75, c='w',zorder=40)          # GSLBY        
    
    
    # Plot MesoWest wind data
    a = get_mesowest_radius_winds(mesowest_time,'10')
    u,v = wind_spddir_to_uv(a['WIND_SPEED'],a['WIND_DIR'])
    m.barbs(a['LON'],a['LAT'],u,v,
            length=5.5,                
            barb_increments=dict(half=1, full=2, flag=10),
            sizes=dict(spacing=0.15, height=0.3, emptybarb=.1))
    
    plt.title(string_time,fontsize=10)
    #plt.title('TDWR Radial Velocity and \nMesoWest Surface Winds\n'+radar_time)
    #plt.xlabel('half= 1 m/s, full = 5 m/s, flag = 10 m/s')        
    
    plt.savefig(out_dir+radar_time+'.png', bbox_inches="tight", dpi=500)
    print 'saved ',out_dir+radar_time,'.png'
        



"""    
# convert all files to a movie
os.system("ffmpeg -f image2 -pattern_type glob -framerate 6 -i '201506*.png' foo.avi")
# Must make movie on meso1. ffmpeg isn't available on other boxes
"""

if __name__ == '__main__':

    # List of file names we want to make plots for
    somelist = []
    for i in os.listdir('./'):
        if i[0:3]=='SLC' and i[-3:]=='asc': # get the file name of a TDWR file for all files
            somelist.append(i)      

    # Count number of processors
    num_proc = multiprocessing.cpu_count()
    p = multiprocessing.Pool(num_proc)
    p.map(make_plot,somelist)
