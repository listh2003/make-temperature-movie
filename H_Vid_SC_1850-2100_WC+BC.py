"""
Read in dynamic surface temperature data and contour plot it.
"""
import iris
import iris.plot as iplt
import iris.coord_categorisation as icat
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from cartopy import config
import cartopy.crs as ccrs
import math

from iris.experimental.equalise_cubes import equalise_attributes
import numpy as np
from spawnCommand import SpawnCommand

def scaleBar(minVal, maxVal):
    degreeStep = 1
    barArray = []
    currentValue = minVal
    while(currentValue <= maxVal):
        barArray.append(currentValue)
        currentValue += degreeStep
    return barArray


def getlimits(cube):

    minTemp = np.amin(cube.data)
    maxTemp = np.amax(cube.data)

    lowerBound = math.floor(minTemp)
    upperBound = math.ceil(maxTemp)

    limits = [lowerBound,upperBound]

    return limits


def plotrun(cube, foldername, scaleLBound, scaleUBound):

    # Delete all the image files in the directory to ensure that only those
    # created in the loop end up in the movie.
    print ("Deleting all .png files in the " + foldername + " directory...")
    SpawnCommand("rm " + foldername +"/*.png")

    # Add a new coordinate containing the year.
    icat.add_year(cube, 'time')

    # Set the end index for the loop over years, and do the loop.
    tmin = 0
    tmax = cube.shape[0]

    # We want the files to be numbered sequentially, starting
    # from 000.png; this is so that the ffmpeg command can grok them.
    index = 0
    #scaleBarArray = scaleBar(lowerBound, upperBound)
    for time in range(tmin, tmax):

        fig = plt.figure(figsize=(6,3), dpi=200)
        rect = 0,0,1200,600
        fig.add_axes(rect)
        geo_axes = plt.axes(projection=ccrs.PlateCarree())
        geo_axes.outline_patch.set_visible(False)
        plt.margins(0,0)
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

        iplt.contourf(cube[time], 10, vmin=scaleLBound, vmax=scaleUBound, cmap='YlOrRd')
        plt.gca().coastlines(color='b')
        # plt.figure(frameon=False)

        # Extract the year value and display it (coordinates used are
        # those of the data).
        year = cube.coord('year')[time].points[0]

        plt.text(-160, 0, year, horizontalalignment='center', size='large',
	         fontdict={'family' : 'monospace'}, color='b')
        filename = str(foldername) + '/' + "%03d.png" % index
        print('Now plotting: ',filename)
        plt.savefig(filename, dpi=200)
        plt.close()
        index += 1

    # Now make the movie from the image files by spawning the ffmpeg command.
    # The options (of which there are many) are somewhat arcane, but these ones work.
    print ("Converting images to movie...")
    options = ("-r 5 -vcodec png -y -i " + foldername
             + "/%03d.png -r 5 -vcodec msmpeg4v2 -qblur 0.01 -qscale 5 ")
    SpawnCommand("ffmpeg " + options + foldername + ".mp4")


def main():
    # Read all the temperature values.
    worstcubes = iris.cube.CubeList([])
    
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

    for i in range(1850, 2015):
        monthCubes = iris.cube.CubeList([])
        for month in months:
            tempfile = 'tas_1850-2014/bc179a.p5' + str(i) + month + '.nc'
            monthCubes.append(iris.load_cube(tempfile))
        worstyearCube = monthCubes.merge_cube()
        worstyearTemp = worstyearCube.collapsed('time', iris.analysis.MEAN)
        worstcubes.append(worstyearTemp)
    for i in range(2015, 2101):
        monthCubes = iris.cube.CubeList([])
        for month in months:
            tempfile = 'tas_2015-2100-ssp119/bh409a.p5' + str(i) + month + '.nc'
            monthCubes.append(iris.load_cube(tempfile))
        worstyearCube = monthCubes.merge_cube()
        worstyearTemp = worstyearCube.collapsed('time', iris.analysis.MEAN)
        worstcubes.append(worstyearTemp)

    equalise_attributes(worstcubes)
    temperatures = worstcubes.merge_cube

    preindustrial = temperatures[100:129, :, :]
    #Calculate the mean over 30 time steps from 1960
    meanindustrial = preindustrial.collapsed('time',iris.analysis.MEAN)
    # Calculate the difference in annual mean temperature from the mean industrial baseline (returns a cube)
    diff = temperatures - meanindustrial
    

    # Truncate the datasets so they both start in 1960.
    diff = diff[100:, :, :]
    

    bounds = getlimits(diff)
    

    lowerBound = min(bounds[0])
    upperBound = max(bounds[1])

    print('Scale set to Min:',lowerBound,'K')
    print('Scale set to Max:',upperBound,'K')

    #Run both cubes
    
    plotfldrname = ['H_SC_1850-2100_WC']

    plotrun(curcube, plotfldrname, lowerBound, upperBound)


if __name__ == '__main__':
    main()