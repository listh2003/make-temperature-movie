import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import iris

fig = plt.figure()
ax1 = plt.axes(xlim=(1850, 2100), ylim=(273, 280))
line, = ax1.plot([], [], lw=2)
plt.xlabel('Year')
plt.ylabel('Temperature (K)')

plotlays, plotcols = [3], ["blue","yellow", "red"]
lines = []
for i in range(3):
    lobj = ax1.plot([],[],lw=2,color=plotcols[i])[0]
    lines.append(lobj)


def init():
    for line in lines:
        line.set_data([],[])
    return lines

x1,y1 = [],[]
x2,y2 = [],[]
x3,y3 = [],[]


monthAverages = []
monthTime = []

yearAverages = []
yearTime = []

decadeAverages = []
decadeTime = []
thisDecadeYearAverages = []


months = {1:'jan', 2:'feb', 3:'mar', 4:'apr', 5:'may', 6:'jun', 7:'jul', 8:'aug', 9:'sep', 10:'oct', 11:'nov', 12:'dec'}
for i in range(1850, 2014):
    thisYearMonthAverages = []
    for month in range(1, 13):
        tempfile = 'tas_1850-2014/bc179a.p5' + str(i) + months[month] + '.nc'
        cube = iris.load_cube(tempfile)
        Temperatures = cube.data
        monthAverage = np.mean(Temperatures)
        monthAverages.append(monthAverage)
        thisYearMonthAverages.append(monthAverage)
        myTime = (12*i + month)/12.0
        monthTime.append(myTime)
    yearAverage = np.mean(thisYearMonthAverages)
    yearAverages.append(yearAverage)
    thisDecadeYearAverages.append(yearAverage)

    yearTime.append(i)
    if i % 10 == 0:
        decadeAverage = np.mean(thisDecadeYearAverages)
        decadeAverages.append(decadeAverage)
        thisDecadeYearAverages = []
        decadeTime.append(i)


def animate(i):

    x = monthTime[i - 1]
    y = monthAverages[i - 1]
    x1.append(x)
    y1.append(y)

    x = yearTime[(i -1)//12]
    y = yearAverages[(i -1)//12]
    x2.append(x)
    y2.append(y)

    x = decadeTime[(i-1)//120]
    y = decadeAverages[(i-1)//120]
    x3.append(x)
    y3.append(y)

    xlist = [x1, x2, x3]
    ylist = [y1, y2, y3]

    #for index in range(0,1):
    for lnum,line in enumerate(lines):
        line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 

    return lines

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init, blit=True,
                               frames=3012, interval=10)

anim.save('graphAnimation.mp4', fps=100, extra_args=['-vcodec', 'libx264'])

plt.show()
