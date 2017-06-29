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


def scaleBar(minVal, maxVal):
    degreeStep = 1
    barArray = []
    currentValue = minVal
    while(currentValue <= maxVal):
        barArray.append(currentValue)
        currentValue += degreeStep
    return barArray

def getlimits(cube):
    maxTempDifftime = cube.collapsed('time', iris.analysis.MAX)
    maxTempDifflat = maxTempDifftime.collapsed('latitude',iris.analysis.MAX)
    maxTempDiff = maxTempDifflat.collapsed('longitude',iris.analysis.MAX)

    minTempDifftime = cube.collapsed('time', iris.analysis.MIN)
    minTempDifflat = minTempDifftime.collapsed('latitude',iris.analysis.MIN)
    minTempDiff = minTempDifflat.collapsed('longitude',iris.analysis.MIN)

    lowerBound = math.floor(minTempDiff.data)
    upperBound = math.ceil(maxTempDiff.data)

    limits = [lowerBound,upperBound]

    return limits

def plotrun(cube, foldername, scaleLBound, scaleUBound):
    # Add a new coordinate containing the year.
    icat.add_year(cube, 'time')

    # Set the end index for the loop over years, and do the loop.
    tmin = 0
    tmax = cube.shape[0]

    #scaleBarArray = scaleBar(lowerBound, upperBound)
    for time in range(tmin, tmax):

        fig = plt.figure(figsize=(6,3), dpi=200)
        rect = 0,0,1200,600
        fig.add_axes(rect)
        geo_axes = plt.axes(projection=ccrs.PlateCarree())
        geo_axes.outline_patch.set_visible(False)
        plt.margins(0,0)
        fig.subplots_adjust(left=0, right=1, bottom=0, top=1)



        iplt.contourf(cube[time], 15, vmin=scaleLBound, vmax=scaleUBound, cmap='RdBu_r')
        plt.gca().coastlines()
        # plt.figure(frameon=False)

        # Extract the year value and display it (coordinates used are
        # those of the data).
        year = cube.coord('year')[time].points[0]

        # plt.title('Temperature Anomaly From Pre-Industrial Mean')
        plt.text(0, -60, year, horizontalalignment='center')
        filename = str(foldername) + '/' + str(year) + '.png'
        print('Now plotting: ',filename)
        plt.savefig(filename, dpi=200)
        plt.close()

def main():
    # Read all the temperature values.
    worstfilenames=('temperatures.pp','temp-rcp85.pp')
    bestfilenames = ('temperatures.pp', 'temp-rcp26.pp')
    # Load a cube with both the historical and future prediction (worst case) data as a single cube
    worstcase = iris.load_cube(worstfilenames)
    bestcase = iris.load_cube(bestfilenames)

    preindustrial = worstcase[100:129, :, :]
    #Calculate the mean over 30 time steps from 1960
    meanindustrial = preindustrial.collapsed('time',iris.analysis.MEAN)
    # Calculate the difference in annual mean temperature from the mean industrial baseline (returns a cube)
    worstdiff = worstcase - meanindustrial
    bestdiff = bestcase - meanindustrial

    worstbounds = getlimits(worstdiff)
    bestbounds = getlimits(bestdiff)

    lowerBound = min(worstbounds[0],bestbounds[0])
    upperBound = max(worstbounds[1],bestbounds[1])

    print('Scale set to Min:',lowerBound,'K')
    print('Scale set to Max:',upperBound,'K')

    #Run both cubes
    plotcubes = [worstdiff,bestdiff]
    plotfldrname = ['rcp85','rcp26']
    #Run one cube
    #plotcubes = [bestdiff]
    #plotfldrname = ['rcp26']

    for val, curcube in enumerate(plotcubes):
        plotrun(curcube, plotfldrname[val],lowerBound,upperBound)


if __name__ == '__main__':
    main()

