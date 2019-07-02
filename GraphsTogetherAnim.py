import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import iris

fig = plt.figure()
ax1 = plt.axes(xlim=(1850, 2100), ylim=(273, 280))
line, = ax1.plot([], [], lw=2)
plt.xlabel('Year')
plt.ylabel('Temperature (K)')

lines = []

def init():
    
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

def animate(i):
    global lines, plotlays 
    if i < 1980:
        x = histmonthTime[i-1]
        y = histmonthAverages[i-1]
        x1.append(x)
        y1.append(y)

        x = histyearTime[(i-1)//12]
        y = histyearAverages[(i-1)//12]
        x2.append(x)
        y2.append(y)

        x = histdecadeTime[(i-1)//120]
        y = histdecadeAverages[(i-1)//120]
        x3.append(x)
        y3.append(y)

        plotlays, plotcols = [3], ["mocassin", "sandybrown", "peru"]
        
        for i in range(3):
            lobj = ax1.plot([],[],lw=2,color=plotcols[i])[0]
            lines.append(lobj)
        print('historical data animated')

    elif i < 3012:
        x = bestmonthTime[i-1]
        y = bestmonthAverages[i-1]
        x1.append(x)
        y1.append(y)

        x = bestyearTime[(i-1)//12]
        y = bestyearAverages[(i-1)//12]
        x2.append(x)
        y2.append(y)

        x = bestdecadeTime[(i-1)//120]
        y = bestdecadeAverages[(i-1)//120]
        x3.append(x)
        y3.append(y)

        

        plotlays, plotcols = [3], ["palegreen", "chartreuse", "darkgreen"]
        
        for i in range(3):
            lobj = ax1.plot([],[],lw=2,color=plotcols[i])[0]
            lines.append(lobj)
        print('best case scenario animated')

    elif i < 4044:
        x = worstmonthTime[i-1]
        y = worstmonthAverages[i-1]
        x1.append(x)
        y1.append(y)

        x = worstyearTime[(i-1)//12]
        y = worstyearAverages[(i-1)//12]
        x2.append(x)
        y2.append(y)

        x = worstdecadeTime[(i-1)//120]
        y = worstdecadeAverages[(i-1)//120]
        x3.append(x)
        y3.append(y)

        plotlays, plotcols = [3], ["lightcoral", "firebrick", "red"]
        
        for i in range(3):
            lobj = ax1.plot([],[],lw=2,color=plotcols[i])[0]
            lines.append(lobj)
        print('worst case scenario animated')
    elif i < 4776:
        x = OSmonthTime[i-1]
        y = OSmonthAverages[i-1]
        x1.append(x)
        y1.append(y)

        x = OSyearTime[(i-1)//12]
        y = OSyearAverages[(i-1)//12]
        x2.append(x)
        y2.append(y)

        x = OSdecadeTime[(i-1)//120]
        y = OSdecadeAverages[(i-1)//120]
        x3.append(x)
        y3.append(y)

        plotlays, plotcols = [3], ["lightblue", "dodgerblue", "blue"]
        
        for i in range(3):
            lobj = ax1.plot([],[],lw=2,color=plotcols[i])[0]
            lines.append(lobj)
        print('overshoot scenario animated')
    xlist = [x1, x2, x3]
    ylist = [y1, y2, y3]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 

    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
print('loading')
anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True,
                               frames=3012, interval=10)

print('saving')
anim.save('graphAnimation.mp4', fps=100, extra_args=['-vcodec', 'libx264'])

plt.show()