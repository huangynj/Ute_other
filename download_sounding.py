## Brian Blaylock
## Script for downloading sounding data from SLC from the UWyoming site

import numpy as np
from numpy import ma
import linecache
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
from matplotlib.dates import DateFormatter, YearLocator, MonthLocator, DayLocator, HourLocator, MinuteLocator
import matplotlib as mpl
from scipy.io import netcdf
from functions import functions_domains_models
import os
import urllib2
from bs4 import BeautifulSoup
from mesowest_stations_radius import get_mesowest_radius_winds, wind_spddir_to_uv



def download_sounding(year,month,day,hour):
    stn = '72572' # this is the id number for KSLC
    year = str(year).zfill(4)
    month= str(month).zfill(2)
    day  = str(day).zfill(2)
    hour = str(hour).zfill(2) # hour in UTC, 00 and 12 z usually available
    
    
    # Download, process and add to plot the Wyoming Data
    # 1)
    # Wyoming URL to download Sounding from
    url = 'http://weather.uwyo.edu/cgi-bin/sounding?region=naconf&TYPE=TEXT%3ALIST&YEAR='+year+'&MONTH='+month+'&FROM='+day+hour+'&TO='+day+hour+'&STNM='+stn
    content = urllib2.urlopen(url).read()
   
    
    # 2)
    # Remove the html tags
    soup = BeautifulSoup(content,"html.parser")
    data_text = soup.get_text()
    
    # 3)
    # Split the content by new line.
    splitted = data_text.split("\n",data_text.count("\n"))
    
    
    #4)
    # Must save the processed data as a .txt file to be read in by the skewt module.
    # Write this splitted text to a .txt document. Save in current directory.
    Sounding_dir = './'
    Sounding_filename = str(stn)+'.'+str(year)+str(month)+str(day)+str(hour)+'.txt'
    f = open(Sounding_dir+Sounding_filename,'w')
    for line in splitted[4:]:
        f.write(line+'\n')
    f.close()
    
    return Sounding_dir+Sounding_filename
