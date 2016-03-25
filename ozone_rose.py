"""
Ozone Rose

requires windrose module from --> https://pypi.python.org/pypi/windrose/1.5

Creates a polar plot of ozone concentration with wind direction. Shown as a
frequency of occurance.
Shows the ozone concentration and the wind direction for the corresponding
times.

Original: http://youarealegend.blogspot.com/2008/09/windrose.html

Modified: by Brian Blaylock
Date: June 24, 2015

"""


from windrose import WindroseAxes
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from numpy.random import random
from numpy import arange
import numpy as np
from datetime import datetime

import json
import urllib2


# Import data from MesoWest API
## API Query
#---------------------------------------------------------------------------
token = '1234567890' #Get your own mesowest token from http://mesowest.org/api/


##Lake Stations
#station = 'bgrut,o3s08,o3s07,snx,gslm,o3s01,qsy,o3s03,o3s02,qsa,'

##Urban Stations
station = 'qh3,naa,o3s05,qhw,mtmet,qbv,qbr,qsf,qnp,qhv,qo2'

##All in-situ stations
station = 'bgrut,qbv,qbr,fwp,o3s08,gslm,qhv,qhw,qh3,lms,ql4,naa,qnp,qo2,qsa,qsf,mtmet'





## dateformat YYYYMMDDHHMM
start_time = '201506010000'
end_time =   '201509010000'
variables = 'ozone_concentration,wind_direction,wind_speed'
time_option = 'utc'
URL = 'http://api.mesowest.net/v2/stations/timeseries?stid='+station+'&start='+start_time+'&end='+end_time+'&vars='+variables+'&obtimezone='+time_option+'&token='+token

##Open URL and read the content
f = urllib2.urlopen(URL)
data = f.read()

##Convert that json string into some python readable format
data = json.loads(data)


## Loop through all stations: process, plot, and store ozone data.
for i in np.arange(0,len(data['STATION'])):
    
    print data['STATION'][i]['STID']    
    plt.cla()
    plt.clf()
    plt.close()
    ##Get station name and id
    stn_name = data['STATION'][i]['NAME']
    stn_id = data['STATION'][i]['STID']
    
    wind_dir_raw = data['STATION'][i]["OBSERVATIONS"]["wind_direction_set_1"]
    wind_spd_raw = data['STATION'][i]["OBSERVATIONS"]["wind_speed_set_1"]
    if (id == 'fwp') or (id =='qhw') or (id =='lms') or (id =='gslm') or (id =='qh3'):
        ozone_raw    = data['STATION'][0]["OBSERVATIONS"]["ozone_concentration_set_2"]
    else:
        ozone_raw    = data['STATION'][0]["OBSERVATIONS"]["ozone_concentration_set_1"]
    ##Look for blank data and replace with None
    for v in np.arange(0,len(ozone_raw)):
        if ozone_raw[v]=='':
            ozone_raw[v]=None    
    
    
    wind_dir = np.array(wind_dir_raw,dtype=float)
    wind_spd = np.array(wind_spd_raw,dtype=float)
    ozone = np.array(ozone_raw,dtype=float)
    
    ##Get date and times
    dates = data["STATION"][i]["OBSERVATIONS"]["date_time"]
    ##Convert to datetime and put into a numpy array
    DATES = np.array([]) #initialize the array to store converted datetimes
    
    ##Loop through each date. Convert into datetime format and put into DATES array
    for j in dates:
    	try:
    		converted_time = datetime.strptime(j,'%Y-%m-%dT%H:%M:%SZ')
    		DATES = np.append(DATES,converted_time)
    		#print 'Times are in UTC'
    	except:
    		converted_time = datetime.strptime(j,'%Y-%m-%dT%H:%M:%S-0600')
    		DATES = np.append(DATES,converted_time)
    		#print 'Times are in Local Time'
    
    # Create DateString for plot title
    s_datestring = datetime.strftime(DATES[0],"%b %d, %Y %H:%M:%S")
    e_datestring = datetime.strftime(DATES[-1],"%b %d, %Y %H:%M:%S")
    
    #Create wind speed and direction variables
    ws = ozone
    wd = wind_dir
    
        
    
    #A quick way to create new windrose axes...
    def new_axes():
        fig = plt.figure(figsize=(6,8), dpi=80, facecolor='w', edgecolor='w')
        rect = [0.1, 0.1, 0.8, 0.8]
        ax = WindroseAxes(fig, rect, axisbg='w')
        fig.add_axes(ax)
        return ax
    
    #...and adjust the legend box
    def set_legend(ax):
        l = ax.legend()
        plt.setp(l.get_texts())
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),prop={'size':15})
        
        
    #A stacked histogram with normed (displayed in percent) results :
    ax = new_axes()
    ax.bar(wd, ws, nsector = 16, \
                   bins = [0,60,75,95,115], normed=True, \
                   opening=.95, edgecolor='w', \
                   colors = ('green','yellow','orange', 'red', 'purple'))
    #set_legend(ax)
    plt.title("Ozone Rose "+stn_name+"\n"+s_datestring+" - "+e_datestring+ "\n", fontsize=20)
    
    
    plt.grid(True)
    plt.yticks(np.arange(0,105,5))
    ax.set_yticklabels(['','5%','10%','15%', '20%','25%','30%','','40%'], fontsize = 15)
    ax.set_rmax(25)
    fig = plt.gcf()
    #fig.set_size_inches(17.5, 15.5)
    fig.set_size_inches(7,8.5)
    plt.savefig("./Morning_Hours_08-20local/OzoneRose_"+stn_name+"_"+start_time+"-"+end_time+ ".png",type="png")
    plt.show()
    
    
        
        
