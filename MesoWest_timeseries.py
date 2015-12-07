# Brian Blaylock
# 7 December 2015

# Function for getting MesoWest time series from the API for one station

import numpy as np
import datetime
import json
import urllib2

token = '0123456789' #Request your own token at http://mesowest.org/api/signup/

variables = 'wind_direction,wind_speed,wind_gust,air_temp,dew_point_temperature,relative_humidity'

def get_mesowest_ts(stationID,start_time,end_time):
    """
    Makes a time series query from the MesoWest API
    
    Input:
        stationID  : string of the station ID
        start_time : datetime object of the start time in UTC
        end_time   : datetime object of the end time in UTC
        
    Output:
        a dictionary of the data
    """

    # convert the start and end time to the string format requried by the API
    start = start_time.strftime("%Y%m%d%H%M")
    end = end_time.strftime("%Y%m%d%H%M")
    
    # The API request URL
    URL = 'http://api.mesowest.net/v2/stations/timeseries?stid='+stationID+'&start='+start+'&end='+end+'&vars='+variables+'&obtimezone=utc&token='+token
    
    ##Open URL and read the content
    f = urllib2.urlopen(URL)
    data = f.read()
    
    ##Convert that json string into some python readable format
    data = json.loads(data)
    
    stn_name = str(data['STATION'][0]['NAME'])
    stn_id   = str(data['STATION'][0]['STID'])
    temp     = np.array(data['STATION'][0]["OBSERVATIONS"]["air_temp_set_1"]) 
    rh       = np.array(data['STATION'][0]["OBSERVATIONS"]["relative_humidity_set_1"])
    wd       = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_direction_set_1"])
    ws	   = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_speed_set_1"])
    wg	   = np.array(data['STATION'][0]["OBSERVATIONS"]["wind_gust_set_1"])
    
    # Need to do some special stuff with the dates
    ##Get date and times
    dates = data["STATION"][0]["OBSERVATIONS"]["date_time"]
    ##Convert to datetime and put into a numpy array
    DATES = np.array([]) #initialize the array to store converted datetimes
    
    ##Loop through each date. Convert into datetime format and put into DATES array
    ## NOTE: only works for MDT which is 6 hours behind UTC
    for j in dates:
    	try:
    		converted_time = datetime.datetime.strptime(j,'%Y-%m-%dT%H:%M:%SZ')
    		DATES = np.append(DATES,converted_time)
    		#print 'Times are in UTC'
    	except:
    		converted_time = datetime.datetime.strptime(j,'%Y-%m-%dT%H:%M:%S-0600')
    		DATES = np.append(DATES,converted_time)
    		#print 'Times are in Local Time'
    
    data_dict = {
                'station name':stn_name,
                'station id':stn_id,
                'datetimes':DATES,                
                'temperature':temp,
                'relative humidity':rh,
                'wind direction':wd,
                'wind speed':ws,
                'wing gust':wg
                }
                
    return data_dict
    
    
#--- Example -----------------------------------------------------------------#
if __name__ == "__main__":
    
    import matplotlib.pyplot as plt
    from matplotlib.dates import DateFormatter, YearLocator, MonthLocator, DayLocator, HourLocator
    
    # Get MesoWest data from functin above
    station = 'UKBKB'
    start_time = datetime.datetime(2015,5,1)
    end_time = datetime.datetime(2015,5,2)
    
    a = get_mesowest_ts(station,start_time,end_time)
    
    # Make a quick temperature plot
    temp = a['temperature']
    RH = a['relative humidity']
    dates = a['datetimes']
    
    #convert dates from UTC to mountain time (-6 hours)
    dates = dates - datetime.timedelta(hours=6)
    
    fig = plt.figure(figsize=(8,4))
    plt.title(station)    
    plt.xlabel('Date Time MDT')
    ax1 = fig.add_subplot(111)
    ax1.plot(dates,temp, 'r')
    ax1.set_ylabel('Temperature (c)')
    ax2 = ax1.twinx()
    ax2.plot(dates,RH,'g')
    ax2.set_ylabel('Relative Humidity (%)')    

    
    ##Format Ticks##
    ##----------------------------------
    # Find months
    months = MonthLocator()
    # Find days
    days = DayLocator()
    # Find each 0 and 12 hours
    hours = HourLocator(byhour=[0,6,12,18])
    # Find all hours
    hours_each = HourLocator()
    # Tick label format style
    dateFmt = DateFormatter('%b %d, %Y\n%H:%M')
    # Set the x-axis major tick marks
    ax1.xaxis.set_major_locator(hours)
    # Set the x-axis labels
    ax1.xaxis.set_major_formatter(dateFmt)
    # For additional, unlabeled ticks, set x-axis minor axis
    ax1.xaxis.set_minor_locator(hours_each)

    
    
