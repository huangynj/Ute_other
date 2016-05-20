## Brian Blaylock
## 20 May 2016

## Download HRRR file from ncep nomads server

import urllib
from datetime import datetime, timedelta
import os
from numpy import mod

def reporthook_all(count, block_size, total_size):
    # Prints percentage downloaded after downloaded every block
    if int(count * block_size * 100 / total_size) == 100:
        print 'Download completed!'
    else:
        print '%2.2f percent complete' % (count * block_size * 100. / total_size)

def reporthook_10(count, block_size, total_size):
    #prints percentage when downloaded approx. every 10% chuncks
    if int(count * block_size * 100. / total_size) == 100:
        print 'Download completed!'
    elif mod(round(count * block_size * 100. / total_size,2),10)==0 :
        print (count * block_size * 100 / total_size),"% complete"


def download_hrrr(request_date,fields=['prs', 'sfc','nat'],hour=range(0,24),forecast=range(0,16),outpath='./'):
    """
    Downloads HRRR grib2 files from the nomads server
    http://nomads.ncep.noaa.gov/
    
    request_date = a datetime object for which you wish to download
    fields= list of fields you want to download
             Default is all fields ['prs', 'sfc','nat']
             pressure fields (~350 MB), surface fields (~6 MB), Native fields(??) (~510 MB)
    hour = a list of hours you want to download
           Default all hours in the day
    forecast = a list of forecast hour you wish to download
               Default all forecast hours (0,15)
    outpath = the outpath directory you wish to save the files.
              Default to current directory but will create a new
              directory in that path for each field (prs or sfc)
    """
    # We'll store the URLs we download from and return them for troubleshooting
    URL_list = []    
    
    year     = request_date.year
    month    = request_date.month
    day      = request_date.day

    # Build the URL string we want to download. One for each field, hour, and forecast
    URL = 'http://nomads.ncep.noaa.gov/pub/data/nccf/nonoperational/com/hrrr/prod/hrrr.%04d%02d%02d/' % (year,month,day)
    for field in fields:
      # Create a new directory for each field to keep things organized
      outdir = outpath +'%s/' % (field) # the path we want to save the file. Put pressure and surface field in different directory
      if not os.path.exists(outdir):
          os.makedirs(outdir)
        for h in hour:
            for f in forecast:
                FileName = 'hrrr.t%02dz.wrf%sf%02d.grib2' % (h,field,f) 

                # Download and save the file
                print 'Downloading:', FileName                
                urllib.urlretrieve(URL+FileName,outdir+FileName,reporthook_10) # if you don't want to print the progress get rid of third argument 'reporthook'
                print 'Saved:', outdir+FileName
                URL_list.append(URL+FileName)
    # Return the list of URLs we downloaded from for troubleshooting    
    return URL_list


if __name__ == '__main__':
    
    ## download HRRR files from yesterday
    yesterday = datetime.now()-timedelta(days=1)
    
    ## download everything (all hours, all fields, all forecasts)    
    #URLs = download_hrrr(yesterday)
    
    ## download only surface fields for analysis hours
    URLs = download_hrrr(yesterday,fields=['sfc'],forecast=[0])
    
