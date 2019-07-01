"""
Read in dynamic surface temperature data and contour plot it.
Harry's Version for new data.
"""

import sys
import math
import time as myTime

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import iris.coord_categorisation as icat

from iris.experimental.equalise_cubes import equalise_attributes

from spawnCommand import SpawnCommand
'''
StartYear and endYear must be between 1850 and 2100
Scenario = BestCase, WorstCase, Overshoot
'''
def myload(start, end, string):

    cubes = iris.cube.CubeList([])
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
   
    for i in range(start, end + 1):
        monthlyList = iris.cube.CubeList([])
        
        for month in range(0, 12):

            tempfile = string + str(i) + months[month] + '.nc'
            cube = iris.load_cube(tempfile)
            monthlyList.append(cube)
        
        yearCube = monthlyList.merge_cube()
        yearTemp = yearCube.collapsed('time', iris.analysis.MEAN)

        #adds each year's 2-d cube into a cubelist, which is then merged into a 3-d cube.
        cubes.append(yearTemp)
    equalise_attributes(cubes)
   
    return(cubes)



def create_video():

    #creating the video
    SpawnCommand("ffmpeg -i image-%04d.png TemperatureVideo1.mp4")
    SpawnCommand('ffmpeg -i TemperatureVideo1.mp4 -filter:v "setpts=5.0*PTS" ssp585.mp4')
    print ("Deleting the unneeded images...")
    SpawnCommand("rm -f *.png")
    SpawnCommand("rm -f TemperatureVideo1.mp4")
    


def main():

    # Delete all the image files in the current directory to ensure that only those
    # created in the loop end up in the movie.
    print ("\nDeleting all .png files in this directory...")
    SpawnCommand("rm -f *.png")
    
    print("Loading the data...")

    # Read all the temperature values and create a single cube containing this data
    cubeList = iris.cube.CubeList([])

    if sys.argv[1] == 'ssp585':
        cubeList.extend(myload(1960, 2014, 'tas_1850-2014/bc179a.p5'))
        cubeList.extend(myload(2015, 2100, 'tas_2015-2100-ssp585/be653a.p5'))
    elif sys.argv[1] == 'ssp119':
        cubeList.extend(myload(1960, 2014, 'tas_1850-2014/bc179a.p5'))
        cubeList.extend(myload(2015, 2100, 'tas_2015-2100-ssp119/bh409a.p5'))
    elif sys.argv[1] == 'ssp534OS':
        cubeList.extend(myload(1960, 2014, 'tas_1850-2014/bc179a.p5'))
        cubeList.extend(myload(2015, 2039, 'tas_2015-2100/be653a.p5'))
        cubeList.extend(myload(2040, 2100, 'tas_2015-2100-ssp534OS/bh409a.p5'))
    else:
        sys.exit("argument must be ssp119, ssp585 or ssp534OS")

    equalise_attributes(cubeList)
    temperatures = cubeList.merge_cube()
    baseYears = temperatures[ :29, :, :]
    baseYearsMean = baseYears.collapsed('time',iris.analysis.MEAN)
    # Calculate the difference in annual mean temperature from the mean  baseline (returns a cube)
    anomaly = temperatures - baseYearsMean
    print("Data downloaded! Now Processing...")

    # Get the range of values.

    # Add a new coordinate containing the year.
    icat.add_year(anomaly, 'time')
    years = anomaly.coord('year')
    
    # Set the limits for the loop over years.  
    minTime = 0
    maxTime = temperatures.shape[0]

    print ("Making images from year", years[minTime].points[0], "to", years[maxTime-1].points[0], "...")

    for time in range(minTime, maxTime):

        # Contour plot the temperatures and add the coastline.
        
        iplt.contourf(anomaly[time], levels = (-6, -3, 0, 4, 8, 12, 17, 22, 28), colors = ('darkblue', 'blue', 'cyan', 'lightyellow', 'yellow', 'orange', 'darkorange', 'red'))
        #-6.4358826, 27.94899
        plt.gca().coastlines()
        #plt.colorbar(boundaries = (-6, -3, 0, 4, 8, 12, 16, 20, 25), values = (-6, -3, 0, 4, 8, 12, 16, 20))
        # We need to fix the boundary of the figure (otherwise we get a black border at left & top).
        # Cartopy removes matplotlib's axes.patch (which normally defines the boundary) and
        # replaces it with outline_patch and background_patch.  It's the former which is causing
        # the black border.  Get the axis object and make its outline patch invisible.
        ax = plt.gca()
        ax.outline_patch.set_visible(False)

        # Extract the year value and display it (coordinates used in locating the text are
        # those of the data).
        year = years[time].points[0]
        plt.text(0, -60, year, horizontalalignment='center') 
        
       
        # Now save the plot in an image file.  The files are numbered sequentially, starting
        # from 000.png; this is so that the ffmpeg command can grok them.
        filename = "image-%04d.png" % time
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        
        # Discard the figure (otherwise the text will be overwritten
        # by the next iteration).
        plt.close()
        print('boundaries for colour = -6, -3, 0, 4, 8, 12, 16, 20, 25')
    print("images made! Now converting to .mp4...")
    create_video()
    print("Opening video...")
    myTime.sleep(5)
    
    

if __name__ == '__main__':
    main()
