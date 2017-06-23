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

def main():
    # Read all the temperature values.
    temperatures = iris.load_cube('temperatures.pp')
    
    # Get the range of values.
    minTemp = np.amin(temperatures.data)
    maxTemp = np.amax(temperatures.data)

    # Add a new coordinate containing the year.
    icat.add_year(temperatures, 'time')
    
    # Set the end index for the loop over years, and do the loop.
    tmax = 146
    for time in range(0, tmax):

       # Contour plot the temperatures and add the coastline.
       iplt.contourf(temperatures[time], 15, vmin=minTemp, vmax=maxTemp, cmap='hot')
       plt.gca().coastlines()

       # Extract the year value and display it (coordinates used are
       # those of the data).
       year = temperatures.coord('year')[time].points[0]
       plt.text(0, -60, year, horizontalalignment='center') 
       
       # Now save the plot in an image file.
       filename = "%s.png" % year
       plt.savefig(filename, bbox_inches='tight', pad_inches=0)
       
       # Discard the figure (otherwise the text will be overwritten
       # by the next iteration).
       plt.close()

if __name__ == '__main__':
    main()

