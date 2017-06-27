"""
Read in dynamic surface temperature data and contour plot it.
"""
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
    print "Deleting all .png files in this directory..."
    SpawnCommand("rm *.png")

    # Read all the temperature values.
    temperatures = iris.load_cube('temperatures.pp')
    
    # Get the range of values.
    minTemp = np.amin(temperatures.data)
    maxTemp = np.amax(temperatures.data)
    print "Range of temperatures is", minTemp, "to", maxTemp

    # Add a new coordinate containing the year.
    icat.add_year(temperatures, 'time')
    
    # Set the limits for the loop over years, output them, and do the loop.
    minTime = 0
    maxTime = temperatures.shape[0]

    years = temperatures.coord('year')
    print "Making images from year", years[minTime].points[0], "to", years[maxTime-1].points[0]

    for time in range(minTime, maxTime):

       # Contour plot the temperatures and add the coastline.
       iplt.contourf(temperatures[time], 15, vmin=minTemp, vmax=maxTemp, cmap='hot')
       plt.gca().coastlines()

       # Extract the year value and display it (coordinates used in locating the text are
       # those of the data).
       year = years[time].points[0]
       plt.text(0, -60, year, horizontalalignment='center') 
       
       # Now save the plot in an image file.  The files are numbered sequentially, starting
       # from 000.png; this is so that the ffmpeg command can grok them.
       filename = "%03d.png" % time
       plt.savefig(filename, bbox_inches='tight', pad_inches=0)
       
       # Discard the figure (otherwise the text will be overwritten
       # by the next iteration).
       plt.close()

    # Now make the movie from the image files by spawning the ffmpeg command.
    # The options (of which there are many) are somewhat arcane, but these ones work.
    print "Converting images to movie..."
    options = "-r 5 -vcodec png -y -i %03d.png -r 5 -vcodec msmpeg4v2 -qblur 0.01 -qscale 5"
    SpawnCommand("ffmpeg " + options + " plotTemperatures.avi")

if __name__ == '__main__':
    main()

