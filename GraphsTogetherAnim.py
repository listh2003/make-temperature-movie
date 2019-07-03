import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import iris

fig = plt.figure()
ax1 = plt.axes(xlim=(1850, 2100), ylim=(273, 280))
line, = ax1.plot([], [], lw=2)
plt.xlabel('Year')
plt.ylabel('Temperature (K)')

plotcols = ["moccasin", "sandybrown", "peru"]
lines = []
for i in range(3):
    lobj = ax1.plot([],[],lw=2,color=plotcols[i])[0]
    lines.append(lobj)

def init():
    global lines
    for line in lines:
        line.set_data([],[])
    return lines

x1,y1 = [],[]
x2,y2 = [],[]
x3,y3 = [],[]

histmonthAverages = []
histmonthTime = []
bestmonthAverages = []
bestmonthTime = []
worstmonthAverages = []
worstmonthTime = []
OSmonthAverages = []
OSmonthTime = []

histyearAverages = []
histyearTime = []
bestyearAverages = []
bestyearTime = []
worstyearAverages = []
worstyearTime = []
OSyearAverages = []
OSyearTime = []

histdecadeAverages = []
histdecadeTime = []
bestdecadeAverages = []
bestdecadeTime = []
worstdecadeAverages = []
worstdecadeTime = []
OSdecadeAverages = []
OSdecadeTime = []

thisDecadeYearAverages = []

print('starting to load')
months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
for i in range(1850, 2014):
    thisYearMonthAverages = []
    for month in range(1, 13):
        
        tempfile = 'tas_1850-2014/bc179a.p5' + str(i) + months[month] + '.nc'
        cube = iris.load_cube(tempfile)
        Temperatures = cube.data
        histmonthAverage = np.mean(Temperatures)
        histmonthAverages.append(histmonthAverage)
        thisYearMonthAverages.append(histmonthAverage)
        myTime = (12*i + month)/12.0
        histmonthTime.append(myTime)
    histyearAverage = np.mean(thisYearMonthAverages)
    histyearAverages.append(histyearAverage)
    thisDecadeYearAverages.append(histyearAverage)

    histyearTime.append(i)
    if i % 10 == 0:
        histdecadeAverage = np.mean(thisDecadeYearAverages)
        histdecadeAverages.append(histdecadeAverage)
        thisDecadeYearAverages = []
        histdecadeTime.append(i)
        print('another decade done')
thisDecadeYearAverages = []
print('1850-2014 done')
for i in range(2015, 2101):
    thisYearMonthAverages = []
    for month in range(1, 13):
        tempfile = 'tas_2015-2100-ssp119/bh409a.p5' + str(i) + months[month] + '.nc'
        cube = iris.load_cube(tempfile)
        Temperatures = cube.data
        bestmonthAverage = np.mean(Temperatures)
        bestmonthAverages.append(bestmonthAverage)
        thisYearMonthAverages.append(bestmonthAverage)
        myTime = (12*i + month)/12.0
        bestmonthTime.append(myTime)
    bestyearAverage = np.mean(thisYearMonthAverages)
    bestyearAverages.append(bestyearAverage)
    thisDecadeYearAverages.append(bestyearAverage)

    bestyearTime.append(i)
    if i % 10 == 0:
        bestdecadeAverage = np.mean(thisDecadeYearAverages)
        bestdecadeAverages.append(bestdecadeAverage)
        thisDecadeYearAverages = []
        bestdecadeTime.append(i)
        print('another decade done')

print('best case scenario done')

for i in range(2015, 2101):
    thisYearMonthAverages = []
    for month in range(1, 13):
        tempfile = 'tas_2015-2100-ssp585/be653a.p5' + str(i) + months[month] + '.nc'
        cube = iris.load_cube(tempfile)
        Temperatures = cube.data
        worstmonthAverage = np.mean(Temperatures)
        worstmonthAverages.append(worstmonthAverage)
        thisYearMonthAverages.append(worstmonthAverage)
        myTime = (12*i + month)/12.0
        worstmonthTime.append(myTime)
    worstyearAverage = np.mean(thisYearMonthAverages)
    worstyearAverages.append(worstyearAverage)
    thisDecadeYearAverages.append(worstyearAverage)

    worstyearTime.append(i)
    if i % 10 == 0:
        worstdecadeAverage = np.mean(thisDecadeYearAverages)
        worstdecadeAverages.append(worstdecadeAverage)
        thisDecadeYearAverages = []
        worstdecadeTime.append(i)
        print('another decade done')
print('worst case scenario done')
for i in range(2040, 2101):
    thisYearMonthAverages = []
    for month in range(1, 13):
        tempfile = 'tas_2040-2100-ssp534OS/bh456a.p5' + str(i) + months[month] + '.nc'
        cube = iris.load_cube(tempfile)
        Temperatures = cube.data
        OSmonthAverage = np.mean(Temperatures)
        OSmonthAverages.append(OSmonthAverage)
        thisYearMonthAverages.append(OSmonthAverage)
        myTime = (12*i + month)/12.0
        OSmonthTime.append(myTime)
    OSyearAverage = np.mean(thisYearMonthAverages)
    OSyearAverages.append(OSyearAverage)
    thisDecadeYearAverages.append(OSyearAverage)

    worstyearTime.append(i)
    if i % 10 == 0:
        OSdecadeAverage = np.mean(thisDecadeYearAverages)
        OSdecadeAverages.append(OSdecadeAverage)
        thisDecadeYearAverages = []
        OSdecadeTime.append(i)
        print('another decade done')
print('all data loaded')



counter = -1

def animate(i):
    global lines, counter
    lines = []
    counter += 1
    if counter < 1980:
        x = histmonthTime[counter]
        y = histmonthAverages[counter]
        x1.append(x)
        y1.append(y)

        x = histyearTime[(counter)//12]
        y = histyearAverages[(counter)//12]
        x2.append(x)
        y2.append(y)

        x = histdecadeTime[(counter)//120]
        y = histdecadeAverages[(counter)//120]
        x3.append(x)
        y3.append(y)

        plotcols = ["moccasin", "sandybrown", "peru"]
        
        


    elif counter < 3012:
        x = bestmonthTime[counter]
        y = bestmonthAverages[counter]
        x1.append(x)
        y1.append(y)

        x = bestyearTime[(counter)//12]
        y = bestyearAverages[(counter)//12]
        x2.append(x)
        y2.append(y)

        x = bestdecadeTime[(counter)//120]
        y = bestdecadeAverages[(counter)//120]
        x3.append(x)
        y3.append(y)

        

        plotcols = ["palegreen", "chartreuse", "darkgreen"]
    
        for i in range(3):
            lobj = ax1.plot([],[],lw=2,color=plotcols[i])[0]
            lines.append(lobj)
        

    elif i < 4044:
        x = worstmonthTime[counter]
        y = worstmonthAverages[counter]
        x1.append(x)
        y1.append(y)

        x = worstyearTime[(counter)//12]
        y = worstyearAverages[(counter)//12]
        x2.append(x)
        y2.append(y)

        x = worstdecadeTime[(counter)//120]
        y = worstdecadeAverages[(counter)//120]
        x3.append(x)
        y3.append(y)

        plotcols = ["lightcoral", "firebrick", "red"]
        
        
        
    elif i < 4776:
        x = OSmonthTime[counter]
        y = OSmonthAverages[counter]
        x1.append(x)
        y1.append(y)

        x = OSyearTime[(counter)//12]
        y = OSyearAverages[(counter)//12]
        x2.append(x)
        y2.append(y)

        x = OSdecadeTime[(counter)//120]
        y = OSdecadeAverages[(counter)//120]
        x3.append(x)
        y3.append(y)

        plotcols =["lightblue", "dodgerblue", "blue"]
        
        for index in range(0, 3):
            lobj = ax1.plot([],[],lw=2,color=plotcols[index])[0]
            lines.append(lobj)
    
    if counter == 1980:
        print('historic data animated')
    elif counter == 3012:
        print('ssp119 data animated')
    elif counter == 4044:
        print('ssp585 data animated')
    
    xlist = [x1, x2, x3]
    ylist = [y1, y2, y3]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 

    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
print('ssp534OS data animated. Now loading')
anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True,
                               frames=4776, interval=10)

print('saving')
anim.save('graphAnimation.mp4', fps=100, extra_args=['-vcodec', 'libx264'])

plt.show()