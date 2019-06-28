import iris
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np 

    
monthlyAverages = []
monthTime = []

yearlyAverages = []
yearTime = []

decadeAverages = []
decadeTime = []
thisDecadeYearlyAverages = []


endYear = 2014


months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
for i in range(1850, endYear + 1):
    thisYearMonthlyAverages = []
    for month in range(1, 13):
        tempfile = 'tas_1850-2014/bc179a.p5' + str(i) + months[month] + '.nc'
        cube = iris.load_cube(tempfile)
        Temperatures = cube.data
        monthlyAverage = np.mean(Temperatures)
        monthlyAverages.append(monthlyAverage)
        thisYearMonthlyAverages.append(monthlyAverage)
        myTime = (12*i + month)/12.0
        monthTime.append(myTime)

    yearlyAverage = np.mean(thisYearMonthlyAverages)
    yearlyAverages.append(yearlyAverage)
    thisDecadeYearlyAverages.append(yearlyAverage)

    yearTime.append(i)

    if i % 10 == 0:
        decadeAverage = np.mean(thisDecadeYearlyAverages)
        decadeAverages.append(decadeAverage)
        thisDecadeYearlyAverages = []
        decadeTime.append(i)




plt.figure()
plt.title('Average temperatures from 1850 to ' + str(endYear))
plt.xlabel('Year')
plt.ylabel('Average temperature (ºK)')
plt.plot(monthTime, monthlyAverages, label = 'monthly averages')
plt.plot(yearTime, yearlyAverages, label = 'yearly averages')
plt.plot(decadeTime, decadeAverages, label = 'averages per decade')


plt.legend()
plt.show()


#print(Averages)
#print(Time)