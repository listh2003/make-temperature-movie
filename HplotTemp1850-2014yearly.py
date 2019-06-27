"""
Read in dynamic surface temperature data and contour plot it.
Harry's Version for new data.
"""
import time as myTime

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np

import iris
import iris.plot as iplt
import iris.quickplot as qplt
import iris.coord_categorisation as icat

from spawnCommand import SpawnCommand

def main():

    # Delete all the image files in the current directory to ensure that only those
    # created in the loop end up in the movie.
    print ("\nDeleting all .png files in this directory...")
    SpawnCommand("rm -f *.png")
    print("Deleting all .mp4 files in this directory...")
    SpawnCommand("rm -f *.mp4")
    
    
    # Read all the temperature values and create a single cube containing this data
    print("Loading the data...")
    
    cubes = iris.cube.CubeList([])
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    for i in range(1850, 2015):
        monthCubes = iris.cube.CubeList([])
        for month in months:
            tempfile = 'tas_1850-2014/bc179a.p5' + str(i) + month + '.nc'
            monthCubes.append(iris.load_cube(tempfile))
        yearCube = monthCubes.merge_cube()
        yearTemp = yearCube.collapsed('time', iris.analysis.MEAN)
        cubes.append(yearTemp)
        
    temperatures = cubes.merge_cube()
    print("Data downloaded! Now Processing...")

    # Get the range of values.


    minTemp = np.amin(temperatures.data)
    maxTemp = np.amax(temperatures.data)

    

    print ("Range of temperatures is ", minTemp, "K to ", maxTemp, "K.")

    # Add a new coordinate containing the year.
    icat.add_year(temperatures, 'time')
    years = temperatures.coord('year')
    
    # Set the limits for the loop over years.  
    minTime = 0
    maxTime = temperatures.shape[0]

    print ("Making images from year", years[minTime].points[0], "to", years[maxTime-1].points[0], "...")

    for time in range(minTime, maxTime):

        # Contour plot the temperatures and add the coastline.
        iplt.contourf(temperatures[time], 10, vmin=minTemp, vmax=maxTemp, cmap='RdBu_r')
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
    
    SpawnCommand("ffmpeg -i image-%04d.png TemperatureVideo1.mp4")
    SpawnCommand('ffmpeg -i TemperatureVideo1.mp4 -filter:v "setpts=5.0*PTS" TemperatureVideo.mp4')
    print ("Deleting the unneeded images...")
    SpawnCommand("rm -f *.png")
    SpawnCommand("rm -f TemperatureVideo1.mp4")
    print("Opening video...")
    myTime.sleep(5)
    SpawnCommand("open TemperatureVideo.mp4")


if __name__ == '__main__':
    main()
