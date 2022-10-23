#Assignment 2
#import libraries
import pandas as pd
import numpy as np
import pylab as plt
import matplotlib.colors as mcolors


#create function to return average monthly radiation , area and min area required
def assign2(url):
    f = pd.read_csv(url,skiprows=[*range(75)]) #skip to row where data begins
    f = f[['ob_end_time','glbl_irad_amt','ob_hour_count']] # only keep columns with data
    f = f.drop(f.index[f.shape[0]-1]) # delete last row 
    f = f[f.ob_hour_count == 1] # only keep hourly solar radiation 
    
    f['ob_end_time'] = pd.to_datetime(f.ob_end_time, format = '%Y/%m/%d %H:%M') # define ob_end_time as a date time in this format       
    f['timestamp'] = f['ob_end_time'].dt.strftime('%m/%Y') # define timestamp as month and year to be used later
    f['timestamp2'] = f['ob_end_time'].dt.strftime('%d/%m/%Y') #as above but for d/m/y
    months = pd.date_range(start=str(f.ob_end_time.dt.date[0]), #start from inital given date to final date
                           end=str(f.ob_end_time.dt.date[f.shape[0]-1]), 
                           freq='MS').strftime('%m/%Y')
    
    meanRads = []
    dftmp = pd.DataFrame() # temp vairable
    for month in months: #iterate for all months
        isMonth = f['timestamp'] == month 
        dftmp = f[isMonth] #temp variable 
        dates = pd.unique(dftmp['ob_end_time'].dt.strftime('%d/%m/%Y')) #assign dates
        sumDaily = []
        for date in dates:
            sumDaily.append(f.loc[f['timestamp2']==date, 'glbl_irad_amt'].sum())   # an individual day's summed radiation for each day in a month
        meanRads.append(np.mean(sumDaily))   #mean of each day in a month, taking average of every month (kJ/m2 day)
  
    minMeanRads = min(meanRads) # min monthly radiation in given year kJ/m^2 
    
    H = 24; #time in hours
    t = 60*60*H; # time in seconds
    aec = 5000; #annual energy consumption kWh
    
    avgRads = np.array(meanRads) #convert to array (kJ/m^2)
    avgRadsAct = (avgRads *0.15)/t #calculate actual avg gen energy based on given efficiency (kW/m^2)
    minMeanRadsAct = (minMeanRads *0.15)/t # min energy gen (kW/m^2)
    
    at = 1*365*24; #convert year to hours
    he = aec/at; # convert annual consumption from kWh to kW
    
    a = he / avgRadsAct; #calculate area for each month in a given year (m2)
    a1 = np.mean(a); #take average to find avg area for year (m2)
    
    minE = minMeanRadsAct*a1 #min energy gen in a month kW
    s = (he-minE)*30.437*24 #storage required based on mim monthly gen (kWh)
    return meanRads,a1, s

#utilise function for 3 most recent years
meanRads2021, area2021, storage2021 = assign2('midas-open_uk-radiation-obs_dv-202207_greater-london_00708_heathrow_qcv-1_2021.csv')
meanRads2020, area2020,storage2020 = assign2('midas-open_uk-radiation-obs_dv-202107_greater-london_00708_heathrow_qcv-1_2020.csv')
meanRads2019, area2019,storage2019 = assign2('midas-open_uk-radiation-obs_dv-202207_greater-london_00708_heathrow_qcv-1_2019.csv')
month_str = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#calculate average radiation based on 3 years
meanYearlyRads = pd.DataFrame(zip(meanRads2021,meanRads2020,meanRads2019),columns = ['2021','2020','2019'])
Totavg = np.mean(meanYearlyRads, axis=1)

#plot data
fig,ax = plt.subplots()

w = 0.25
bar1 = np.arange(len(month_str))
bar2 = [i+w for i in bar1]
bar3 = [i+w for i in bar2]

ax.bar(bar1,meanRads2021,w,label = '2021',color='lightsalmon')
ax.bar(bar2,meanRads2020,w,label = '2020',color='orangered')
ax.bar(bar3,meanRads2019,w,label = '2019',color='darkred')
ax.plot(month_str,Totavg, '--*',label= "Average", color = 'black')

plt.legend()
plt.xticks(rotation=45)
plt.xticks(bar1+w,month_str)
plt.ylabel(r'Global solar irradiation amount / kJ $m^{-2}$')
plt.show()
