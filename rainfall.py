#Assignment 2

#import libraries
import pandas as pd
import numpy as np
import pylab as plt
import matplotlib.colors as mcolors


#create function to return average monthly radiation , area and min area required
def assign2(url):
    f = pd.read_csv(url,skiprows=[*range(61)]) #skip to row where data begins
    f = f[['ob_end_time','prcp_amt','ob_hour_count']] # only keep columns with data
    f = f.drop(f.index[f.shape[0]-1]) # delete last row 
    f = f[f.ob_hour_count == 1] # only keep hourly rainfall
    
    f['ob_end_time'] = pd.to_datetime(f.ob_end_time, format = '%Y/%m/%d %H:%M') # define ob_end_time as a date time in this format       
    f['timestamp'] = f['ob_end_time'].dt.strftime('%m/%Y') # define timestamp as month and year to be used later
    f['timestamp2'] = f['ob_end_time'].dt.strftime('%d/%m/%Y') #as above but for d/m/y
    months = pd.date_range(start=str(f.ob_end_time.dt.date[0]), #start from inital given date to final date
                           end=str(f.ob_end_time.dt.date[f.shape[0]-1]), 
                           freq='MS').strftime('%m/%Y')
    
    meanRain = []
    dftmp = pd.DataFrame() # temp vairable
    for month in months: #iterate for all months
        isMonth = f['timestamp'] == month 
        dftmp = f[isMonth] #temp variable 
        dates = pd.unique(dftmp['ob_end_time'].dt.strftime('%d/%m/%Y')) #assign dates
        sumDaily = []
        for date in dates:
            sumDaily.append(f.loc[f['timestamp2']==date, 'prcp_amt'].sum())   # an individual day's summed rainfall for each day in a month
        meanRain.append(sum(sumDaily))   #mean of each day in a month, taking average of every month (mean rain collected per hour in mm)
    
    avgRain = np.array(meanRain) #convert to array
    minMeanRain = min(meanRain)*1e-3 # min monthly rainfall in given year (m)
    
    
    v = 200; #average annual consumption of water (m^3)
    a = v/(avgRain*24*30.437*1e-3) # calc area (m^2)
    a1 = np.mean(a)
    s = (v - (minMeanRain*a1*24*30.437)) # storage (m^3)
    
    return meanRain, a1,s

#utilise function for 3 most recent years
meanRain2021, area2021, s2021 = assign2('midas-open_uk-hourly-rain-obs_dv-202207_greater-london_00708_heathrow_qcv-1_2021.csv')
meanRain2020, area2020, s2020 = assign2('midas-open_uk-hourly-rain-obs_dv-202207_greater-london_00708_heathrow_qcv-1_2020.csv')
meanRain2019, area2019, s2019 = assign2('midas-open_uk-hourly-rain-obs_dv-202207_greater-london_00708_heathrow_qcv-1_2019.csv')
month_str = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#calculate average radiation based on 3 years
meanYearlyRain = pd.DataFrame(zip(meanRain2021,meanRain2020,meanRain2019),columns = ['2021','2020','2019'])
Totavg = np.mean(meanYearlyRain, axis=1)

#plot data
fig,ax = plt.subplots()

w = 0.25
bar1 = np.arange(len(month_str))
bar2 = [i+w for i in bar1]
bar3 = [i+w for i in bar2]

ax.bar(bar1,meanRain2021,w,label = '2021',color='paleturquoise')
ax.bar(bar2,meanRain2020,w,label = '2020',color='deepskyblue')
ax.bar(bar3,meanRain2019,w,label = '2019',color='darkblue')
ax.plot(month_str,Totavg, '--*',label= "Average", color = 'black')

plt.legend()
plt.xticks(rotation=45)
plt.xticks(bar1+w,month_str)
plt.ylabel(r'Precipitation amount / mm')
plt.show()
