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
Scenario = Best-case, Worst-case, overshoot
'''
def load_cubes_month_to_year(startYear, endYear, scenario):

    cubes = iris.cube.CubeList([])
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    for i in range(startYear, endYear + 1):
        monthCubes = iris.cube.CubeList([])

        #locates and loads the correct file into monthCubes
        for month in months:
            if i < 2015:
                tempfile = 'tas_1850-2014/bc179a.p5' + str(i) + month + '.nc'
            else:
                if scenario == 'BestCase':
                    tempfile = 'tas_2015-2100-ssp119/bh409a.p5'+ str(i) + month + '.nc'
                elif scenario == 'WorstCase':
                    tempfile = 'tas_2015-2100-ssp585/be653a.p5'+ str(i) + month + '.nc'
                elif scenario == 'Overshoot':
                    if i < 2040:
                        tempfile = 'tas_2015-2100-ssp585/be653a.p5'+ str(i) + month + '.nc'
                    else:
                        tempfile = 'tas_2040-2100-ssp534OS/bh456a.p5'+ str(i) + month + '.nc'
            monthCubes.append(iris.load_cube(tempfile))
        
        #creates a 3-d cube for the year, and then collapses it back to 2-d
        yearCube = monthCubes.merge_cube()
        yearTemp = yearCube.collapsed('time', iris.analysis.MEAN)

        cubes.append(yearTemp)
    equalise_attributes(cubes)
    return(cubes.merge_cube())

def max_min(type, cube):

    if type == 'AnomolousColour':
        #Calculate the mean over 30 time steps from 1960
        baseYears = cube[100:129, :, :]
        
        baseYearsMean = baseYears.collapsed('time',iris.analysis.MEAN)
        # Calculate the difference in annual mean temperature from the mean  baseline (returns a cube)
        cube = cube - baseYearsMean


    minTemp = math.floor(np.amin(cube.data))
    maxTemp = math.ceil(np.amax(cube.data))

    return[minTemp, maxTemp]

def create_video():

    #creating the video
    SpawnCommand("ffmpeg -i image-%04d.png TemperatureVideo1.mp4")
    SpawnCommand('ffmpeg -i TemperatureVideo1.mp4 -filter:v "setpts=5.0*PTS" ' + sys.argv[1] + '_scenario_' + sys.argv[2] + '.mp4')
    print ("Deleting the unneeded images...")
    SpawnCommand("rm -f *.png")
    SpawnCommand("rm -f TemperatureVideo1.mp4")
    


def main():

    # Delete all the image files in the current directory to ensure that only those
    # created in the loop end up in the movie.
    print ("\nDeleting all .png files in this directory...")
    SpawnCommand("rm -f *.png")
    print("Deleting all .mp4 files in this directory...")
    SpawnCommand("rm -f *.mp4")
    
    # Read all the temperature values and create a single cube containing this data
    print("Loading the data...")

    temperatures = load_cubes_month_to_year(sys.argv[3], sys.argv[4], sys.argv[1])
    print("Data downloaded! Now Processing...")

    # Get the range of values.
    bounds = max_min(sys.argv[2], temperatures)

    print ("Range of temperatures is ", bounds[0], "K to ", bounds[1], "K.")

    # Add a new coordinate containing the year.
    icat.add_year(temperatures, 'time')
    years = temperatures.coord('year')
    
    # Set the limits for the loop over years.  
    minTime = 0
    maxTime = temperatures.shape[0]

    print ("Making images from year", years[minTime].points[0], "to", years[maxTime-1].points[0], "...")

    for time in range(minTime, maxTime):

        # Contour plot the temperatures and add the coastline.
        iplt.contourf(temperatures[time], 10, vmin = bounds[0], vmax=bounds[1], cmap='RdBu_r')
        plt.gca().coastlines()
       
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
    print("images made! Now converting to .mp4...")
    create_video()
    print("Opening video...")
    myTime.sleep(5)
    SpawnCommand('open ' + sys.argv[1] + '_scenario_' + sys.argv[2] + '.mp4')


if __name__ == '__main__':
    main()
