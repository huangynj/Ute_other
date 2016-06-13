## Brian Blaylock

# June 13, 2016

### Download a sounding file from University of Wyoming Site,
### save that file to my computer, and
### return a dictionary of the values

from datetime import datetime
import urllib2
from bs4 import BeautifulSoup
import numpy as np

import sys
sys.path.append('/uufs/chpc.utah.edu/common/home/u0553130/pyBKB') #pyBKB on server boxes
sys.path.append('B:\pyBKB')                                       #pyBKB on PC

def wind_spddir_to_uv(wspd,wdir):
    """
    calculated the u and v wind components from wind speed and direction
    Input:
        wspd: wind speed
        wdir: wind direction
    Output:
        u: u wind component
        v: v wind component
    """    
    
    rad = 4.0*np.arctan(1)/180.
    u = -wspd*np.sin(rad*wdir)
    v = -wspd*np.cos(rad*wdir)

    return u,v

def get_sounding(request_date,station='slc'):
    """
    Input
        request_date: a datetime object in UTC. Hour must be 
                      either 0 or 12
        station:      defaults to slc, the salt lake city, or use 
                      a number for the stion identier
                      
    Return
        a dictionary of the data
    """
    
    if station=='slc':
        stn = '72572' # this is the id number for KSLC
    else:
        stn = str(station)
    year = str(request_date.year).zfill(4)
    month= str(request_date.month).zfill(2)
    day  = str(request_date.day).zfill(2)
    hour = str(request_date.hour).zfill(2) # hour in UTC, 00 and 12 z usually available  
    
        
    # Download, process and add to plot the Wyoming Data
    # 1)
    # Wyoming URL to download Sounding from
    url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR='+year+'&MONTH='+month+'&FROM='+day+hour+'&TO='+day+hour+'&STNM='+stn
    content = urllib2.urlopen(url).read()
    
    # 2)
    # Remove the html tags
    soup = BeautifulSoup(content, "html.parser")
    data_text = soup.get_text()
    
    # 3)
    # Split the content by new line.
    splitted = data_text.split("\n",data_text.count("\n"))
    
    #4)
    # Must save the processed data as a .txt file to be read in by the skewt module. https://pypi.python.org/pypi/SkewT
    # Write this splitted text to a .txt document. Save in current directory.
    Sounding_dir = './'
    Sounding_filename = str(stn)+'.'+str(year)+str(month)+str(day)+str(hour)+'.txt'
    f = open(Sounding_dir+Sounding_filename,'w')
    for line in splitted[4:]:
        f.write(line+'\n')
    f.close()   
    
    #5) Read the observed sounding file
    
    # Figure out where the footer is so we can skip it in np.genfromtxt
    lookup = 'Station information and sounding indices' # this is the line the data ends
    with open(Sounding_filename) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                end_data_line = num
    last_line = sum(1 for line in open(Sounding_filename))
    foot = last_line-end_data_line-14 #not entirely sure why we need to subtract 14, but it works.
    print last_line
    print end_data_line
    
    sounding = np.genfromtxt(Sounding_filename,skip_header=8,skip_footer=foot)
    obs_press = sounding[:,0]         # hPa
    obs_hght = sounding[:,1]          # m
    obs_temp = sounding[:,2]          # C          
    obs_dwpt = sounding[:,3]          # C
    obs_rh = sounding[:,4]            # %    
    obs_mixing = sounding[:,5]/1000   # kg/kg                
    obs_wdir = sounding[:,6]          # degrees
    obs_wspd = sounding[:,7]*0.51444  # m/s
    obs_theta = sounding[:,8]         # K
    obs_u,obs_v = wind_calcs.wind_spddir_to_uv(obs_wspd,obs_wdir) #m/s
    
    # 6) Would be nice to return a diction of the station information from the sounding file
    #    such as the Station identified, latitude, longitude, calculated indexes, etc.    
    
    a = {
        'url':url,                  #This is the URL the data is retrived from
        'file':Sounding_filename,   #This is the path to the file we created 
        'DATE':request_date,        #This is the date you requested (datetime object)
        'station':str(station),              #This is the requested station
        'press':obs_press,          #The rest is the data converted to SI units for the profile
        'height':obs_hght,
        'temp':obs_temp,
        'dwpt':obs_dwpt,
        'rh':obs_rh,        
        'mixing ratio':obs_mixing,
        'wdir':obs_wdir,
        'wspd':obs_wspd,
        'theta': obs_theta,
        'u':obs_u,
        'v':obs_v
        }    
    return a
    
if __name__=="__main__":
    
    
    import matplotlib.pyplot as plt

    request_date = datetime(2016,6,13,0)
    a = get_sounding(request_date)
    
    
    # plot a simple vertical profile    
    plt.grid()
    plt.plot(a['temp'],a['height'], c='r', label='Temp')
    plt.plot(a['dwpt'],a['height'], c='g', label='Dwpt')
    plt.barbs(np.zeros_like(a['temp'])[::5],a['height'][::5],a['u'][::5],a['v'][::5], label='Wind')
    plt.legend()    
    
    plt.title("%s    %s" % (a['station'],a['DATE']))
    plt.xlabel('Temperture (C)')
    plt.ylabel('Height (m)')
    
