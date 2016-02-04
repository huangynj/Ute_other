# Brian Blaylock
# Plot TDWR radar and MesoWest Stations on Same Plot

# Had to convert the .nids TDWR radar files to a text file 
# using NOAA's Weather and Climate Toolkit
#   Download here: http://www.ncdc.noaa.gov/wct/
#   Data > Load Data > Local File -or- THREDDS
#   (If you use the THREDDS Server, I get radial velocity from this URL
#   http://thredds.ucar.edu/thredds/catalog/terminal/level3/TV0/SLC/20160203/catalog.xml)
#   List Files > Export > Select Output Format "ESRI ASCII GRID" and change the output directory
#   Next until done


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



        
        
        
## Get some geography data from our WRF runs
output_file = 'auxhist24_d02_2015-06-17_00:00:00'
spat= 'auxhist23_d02_2015-06-17_00:00:00'
# Open file in a netCDF reader   
directory = '/uufs/chpc.utah.edu/common/home/horel-group4/model/bblaylock/WRF3.7_spinup/WRFV3/test/em_real/'
out_dir = '/uufs/chpc.utah.edu/common/home/u0553130/public_html/MS/TDWR/'
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

""" #Full map
cen_lat = float(nc.CEN_LAT)
cen_lon = float(nc.CEN_LON)
truelat1 = float(nc.TRUELAT1)
truelat2 = float(nc.TRUELAT2)
standlon = float(nc.STAND_LON)

# Draw the base map behind it with the lats and
# lons calculated earlier
m = Basemap(resolution='i',projection='lcc',\
    width=width_meters,height=height_meters,\
    lat_0=cen_lat,lon_0=cen_lon,lat_1=truelat1,\
    lat_2=truelat2)
"""
# Define the map boundaries lat/lon
domain = get_domain('salt_lake_valley')
top_right_lat = domain['top_right_lat']+.3
top_right_lon = domain['top_right_lon']
bot_left_lat = domain['bot_left_lat']-.2
bot_left_lon = domain['bot_left_lon']-.2

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
for i in os.listdir('./'):
    if i[0:3]=='SLC': # get the file name of a TDWR file
        print i
        radar_time = i[8:23]
        
        DATETIME = datetime.datetime.strptime(radar_time,"%Y%m%d_%H%M%S")
        mesowest_time = DATETIME.strftime("%Y%m%d%H%M")
        
        
        ### TDWR Radar Data (converted from .nids to .asc grid)
        text = 'SLC_TV0_'+radar_time+'.asc'
        this = np.flipud(np.genfromtxt(text,skip_header=6)) #flip the array        
        
        # Data from .asc file header
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
        
        # Mask the zero values
        this = np.ma.masked_where(this == 0, this)
        
        # Array of lats and lons        
        lats = np.linspace(YLLCORNER,YLLCORNER+CELLSIZE*NROWS,NROWS)
        lons = np.linspace(XLLCORNER,XLLCORNER+CELLSIZE*NCOLS,NCOLS)
        
        ## Begin the Plot
        plt.figure(figsize=[12,15])

        # terrain and lake mask
        m.contourf(x,y,HGT,cmap=plt.get_cmap('binary'))        
        plt.contour(x,y,landmask, [0,1], linewidths=2, colors="b")        
        
        # radar data
        m.pcolormesh(lons,lats,this,cmap='BrBG',vmax=15,vmin=-15)
        cbar_loc = plt.colorbar(shrink=.8,pad=.01)
        cbar_loc.ax.set_ylabel('Radial Velocisy [m/s]')
        
        #m.drawcoastlines()
        m.drawstates()
                
        
        # Location of SLC Radar
        m.scatter(-111.93,40.9669, s=100, c='r')
        
        # Plot MesoWest wind data
        a = get_mesowest_radius_winds(mesowest_time,'10')
        u,v = wind_spddir_to_uv(a['WIND_SPEED'],a['WIND_DIR'])
        m.barbs(a['LON'],a['LAT'],u,v,
                barb_increments=dict(half=1, full=5, flag=10),
                sizes=dict(emptybarb=.1))
        
        plt.title('TDWR Radial Velocity and \nMesoWest Surface Winds\n'+radar_time)
        plt.xlabel('half= 1 m/s, full = 5 m/s, flag = 10 m/s')        
        
        plt.savefig(out_dir+radar_time+'.png', bbox_inches="tight", dpi=300)
        
        
# convert all files to a movie
os.system("ffmpeg -f image2 -pattern_type glob -framerate 12 -i '201506*.png' foo.avi")

