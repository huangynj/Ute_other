### Brian Blaylock

## View NEXRAD Level II Data

## Download NEXRAD II data from Amazon Web Service
## https://s3.amazonaws.com/noaa-nexrad-level2/index.html
## Download URL Example: https://noaa-nexrad-level2.s3.amazonaws.com/2016/08/05/KCBX/KCBX20160805_205859_V06
## Boise: KCBX

## Personal Reminder: Use the Local Version of python on Meso3 or Meso4: /usr/local/bin/python


import numpy as np
from numpy import ma
from datetime import datetime
import matplotlib.pyplot as plt

# link to personal modules (this is where my version of MetPy is located)
import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB')  #for running on CHPC boxes
sys.path.append('B:\pyBKB')  # local path for testing on my machine 

# These are my versions of MetPy. I have an old pre-release. The newest version of MetPy should work
from MetPy_BB.io.nexrad import Level2File
from MetPy_BB.plots import ctables

from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from pyproj import Geod #this is used to convert range/azimuth to lat/lon
from mpl_toolkits.basemap import Basemap

radar = 'KCBX'
date = datetime(2016,8,5,20,58,59)

#file name example: KCBX20160805_205859_V06
filename = '%s%04d%02d%02d_%02d%02d%02d_V06' % (radar, date.year,date.month,date.day,date.hour,date.minute,date.second)

f = Level2File(filename)

# get some basic infor from radar file
rLAT = f.sweeps[0][0][1].lat
rLON = f.sweeps[0][0][1].lon
rDT = f.dt # this is in local time

f.sweeps[0][0] # just to look at

# Pull data out of the file
# sweep reprsents the elevation angle. 
# to get the elevation angle try: f.sweeps[x][0][0].el_angle where x is your sweep index
#sweep = 0
s = range(0,22) # make plots for all sweeps (in this file there are 21 sweeps)
#s = [1]
for sweep in s:
        elv_angle = f.sweeps[sweep][0][0].el_angle
        plt.clf() #clear figures so you don't have a million colorbars added to the plot
        plt.cla()
        try:
            plt.clf()
            plt.cla()
            
            ## some of what follows is found in the metpy docs. 
            ## http://metpy.readthedocs.io/en/stable/examples/generated/NEXRAD_Level_2_File.html
            
            # First item in "ray" is a header, which has the azimuth angle, az
            az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])
                        
            # 5th item is a dict mapping a var name (byte string) to a tuple
            # of (header, data array)
            
            ## Level II data contains these variables: 'REF','RHO','PHI','ZDR','SW','VEL'
              ## REF = Reflectivity
              ## RHO = ?
              ## PHI = ?
              ## ZDR = Differential Reflectivity in vertical or horizontal direction, tells you how spherical or elongated particals are (used to detect snow and rain)
              ## SW  = ?
              ## VEL = Radial Velocity
            ## Note, not every sweep has every variable. REF should be in all sweeps, but we'll try each of the others
            
            ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
            ref_range = np.arange(ref_hdr.num_gates) * ref_hdr.gate_width + ref_hdr.first_gate
            ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])
            try:
                vel_hdr = f.sweeps[sweep][0][4][b'VEL'][0]
                vel_range = (np.arange(vel_hdr.num_gates + 1) - 0.5) * vel_hdr.gate_width + vel_hdr.first_gate
                vel = np.array([ray[4][b'VEL'][1] for ray in f.sweeps[sweep]])
            except:
                pass
            try:
                sw_hdr = f.sweeps[sweep][0][4][b'SW'][0]
                sw_range = (np.arange(sw_hdr.num_gates + 1) - 0.5) * sw_hdr.gate_width + sw_hdr.first_gate
                sw = np.array([ray[4][b'SW'][1] for ray in f.sweeps[sweep]])
            except:
                pass
            try:
                rho_hdr = f.sweeps[sweep][0][4][b'RHO'][0]
                rho_range = (np.arange(rho_hdr.num_gates + 1) - 0.5) * rho_hdr.gate_width + rho_hdr.first_gate
                rho = np.array([ray[4][b'RHO'][1] for ray in f.sweeps[sweep]])
            except:
                pass
            try:
                phi_hdr = f.sweeps[sweep][0][4][b'PHI'][0]
                phi_range = (np.arange(phi_hdr.num_gates + 1) - 0.5) * phi_hdr.gate_width + phi_hdr.first_gate
                phi = np.array([ray[4][b'PHI'][1] for ray in f.sweeps[sweep]])
            except:
                pass
            try:
                zdr_hdr = f.sweeps[sweep][0][4][b'ZDR'][0]
                zdr_range = (np.arange(zdr_hdr.num_gates + 1) - 0.5) * zdr_hdr.gate_width + zdr_hdr.first_gate
                zdr = np.array([ray[4][b'ZDR'][1] for ray in f.sweeps[sweep]])                        
            except:
                pass
                        
            if len(f.sweeps[sweep][0][4])==4:
                get_these = (ref,rho,phi,zdr)
                get_these_r = (ref_range,rho_range,phi_range,zdr_range)
                fignum = [1,2,3,4]
                names = ('REF','RHO','PHI','ZDR')
            elif len(f.sweeps[sweep][0][4])==3:
                get_these = (ref,sw,vel)
                get_these_r = (ref_range,sw_range,vel_range,)
                fignum = [1,2,3]
                names = ('REF','SW','VEL')
            else:
                get_these = (ref,rho,phi,zdr,sw,vel)
                get_these_r = (ref_range,rho_range,phi_range,zdr_range,sw_range,vel_range)
                fignum = [1,2,3,4,5,6]
                names = ('REF','RHO','PHI','ZDR','SW','VEL')
           
            ## Create a plot for each of the available variables
            for var_data, var_range, num, name in zip(get_these, get_these_r, fignum,names):
                plt.clf()
                plt.cla()                
                print name
                # Create Basemap
                fig = plt.figure(num)
                ax  = fig.add_subplot(111)
                
                # define the plotting box (mess around with these to focus on area you are interested in)
                top_right_lat = rLAT+1.25
                top_right_lon = rLON+1.25
                bot_left_lat = rLAT-1
                bot_left_lon = rLON-1
                
                ## Map in cylindrical projection
                m = Basemap(resolution='i',projection='cyl',\
                    llcrnrlon=bot_left_lon,llcrnrlat=bot_left_lat,\
                    urcrnrlon=top_right_lon,urcrnrlat=top_right_lat,)
                maps = [
                    'ESRI_Imagery_World_2D',    # 0
                    'ESRI_StreetMap_World_2D',  # 1
                    'NatGeo_World_Map',         # 2
                    'NGS_Topo_US_2D',           # 3
                    'Ocean_Basemap',            # 4
                    'USA_Topo_Maps',            # 5
                    'World_Imagery',            # 6
                    'World_Physical_Map',       # 7
                    'World_Shaded_Relief',      # 8
                    'World_Street_Map',         # 9
                    'World_Terrain_Base',       # 10
                    'World_Topo_Map'            # 11
                    ]
                     
                ## Instead of using blank background, get an image from ESRI
                m.arcgisimage(service=maps[8], xpixels = 500, verbose= True)
                m.drawcoastlines()
                m.drawstates()    
                
                # Turn data into an array, then mask
                data = ma.array(var_data)
                data[np.isnan(data)] = ma.masked
            
                #rngs = np.array([ray[0].rad_length for ray in f.sweeps[sweep]]) 
                rng = np.linspace(0, var_range[-1], data.shape[-1] + 1)
                print len(rng)
            
                ## We want to plot the radar data on a map. This part is not in the MetPy documentation.
                # Convert az, range to a lat/lon
                g = Geod(ellps='clrk66') # This is the type of ellipse the earth is projected on. 
                                         # There are other types of ellipses you can use,
                                         # but the differences will be small
                center_lat = np.ones([len(az),len(rng)])*rLAT    
                center_lon = np.ones([len(az),len(rng)])*rLON
                az2D = np.ones_like(center_lat)*az[:,None]
                rng2D = np.ones_like(center_lat)*np.transpose(rng[:,None])*1000
                lon,lat,back=g.fwd(center_lon,center_lat,az2D,rng2D)
            
            
                # Convert az,range to x,y
                xlocs = var_range * np.sin(np.deg2rad(az[:, np.newaxis]))
                ylocs = var_range * np.cos(np.deg2rad(az[:, np.newaxis]))
            
                # Plot the data
                cmap = ctables.registry.get_colortable('viridis') # viridis means green in Latin
                                                                  # and will be the new matplotlib default color map
                
                #p = ax.pcolormesh(xlocs, ylocs, data, cmap=cmap)
                if name=='VEL':
                    # use different colormap for the radial velocity plots
                    p = m.pcolormesh(lon,lat,data,cmap='BrBG_r',vmax=10,vmin=-10)
                else:
                    p = m.pcolormesh(lon,lat,data,cmap=cmap)
                #m.set_aspect('equal', 'datalim')
                #ax.set_xlim(-40, 20)
                #ax.set_ylim(-30, 30)
                
                plt.colorbar(p,orientation='horizontal',shrink=.8,pad=.01,
                               label='Units: ??') # I still need to confirm the units for each variable

                ## My file 
                # Plot Fire Perimeter                               
                perimiter = '160806'
                p4 = m.readshapefile('path/fire_shape/perim_'+perimiter,'perim',drawbounds=False)
                           
                patches   = []
                for info, shape in zip(m.perim_info, m.perim):
                    if info['FIRENAME'] == 'PIONEER' and info['SHAPENUM']==1772:
                        x, y = zip(*shape) 
                        #print info
                        #m.plot(x, y, marker=None,color='maroon',linewidth=2)
                        patches.append(Polygon(np.array(shape), True) )
                ax.add_collection(PatchCollection(patches, facecolor= 'maroon', alpha=.65, edgecolor='k', linewidths=1.5, zorder=1))
            
                plt.title('sweep_%s_ElvAngle_%.2f_%s.png'%(sweep,elv_angle,name))
                plt.savefig('sweep_%s_ElvAngle_%.2f_%s.png'%(sweep,elv_angle,name),bbox_inches='tight')
        except:
            print "failed sweep", sweep
#plt.show()
