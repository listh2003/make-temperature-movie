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



   
'''
def create_video():

    #creating the video
    SpawnCommand("ffmpeg -i image-%04d.png Temporary.mp4")
    SpawnCommand('ffmpeg -i Temporary.mp4 -filter:v "setpts=2.5*PTS" 1850_Rainfall.mp4')
    print ("Deleting the unneeded images...")
    SpawnCommand("rm -f *.png")
    SpawnCommand("rm -f TemperatureVideo1.mp4")
    
'''

def main():
    '''
    # Delete all the image files in the current directory to ensure that only those
    # created in the loop end up in the movie.
    print ("\nDeleting all .png files in this directory...")
    SpawnCommand("rm -f *.png")
    
    print("Loading the data...")
    '''
    # Read all the temperature values and create a single cube containing this data
    cubeList = iris.cube.CubeList([])

    for i in range(1, 11, 3):
        QuarterCube = iris.load_cube('tpr_1850/bc179a.pj1850'+ str('{:02}'.format(i))+ '01.nc')
        for sub_cube in QuarterCube.slices(['latitude', 'longitude']):
            cubeList.append(sub_cube)
    mydata = []
    
    equalise_attributes(cubeList)
    wholecube = cubeList.merge_cube()
    
    for myint in wholecube.slices_over(['latitude', 'longitude', 'time']):
        myint = myint.data
        mydata.append(myint)
    #for sub_cube in whole_cube.slices('latitude, longitude')

    
    plt.hist(mydata)
    plt.show
    
    '''
    yearData = cubeList.merge_cube()
    print(yearData)
    
    print("Data downloaded! Now Processing...")

    # Get the range of values.
    maxRain = np.amax(yearData.data)
    print(maxRain)
    #0.013547399
       
    # Add a new coordinate containing the year.
    icat.add_day_of_year(yearData, 'time')
    
    days = yearData.coord('time')
    
    # Set the limits for the loop over years.  
    minTime = 0
    maxTime = 360

    #print ("Making images from year", days[minTime].points[0], "to", days[maxTime-1].points[0], "...")

    
    for time in range(minTime, maxTime):
        iplt.contourf(cubeList[time], vmin = 0.0, vmax = 0.001354799, cmap = 'RdBu_r')
        plt.gca().coastlines()
       
        # We need to fix the boundary of the figure (otherwise we get a black border at left & top).
        # Cartopy removes matplotlib's axes.patch (which normally defines the boundary) and
        # replaces it with outline_patch and background_patch.  It's the former which is causing
        # the black border.  Get the axis object and make its outline patch invisible.
        ax = plt.gca()
        ax.outline_patch.set_visible(False)

        # Extract the year value and display it (coordinates used in locating the text are
        # those of the data).
        
        day = days[time].points[0]
        plt.text(0, -60, day, horizontalalignment='center') 
       
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
    SpawnCommand('open 1850_Rainfall.mp4')
    
'''
if __name__ == '__main__':
    main()
