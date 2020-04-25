import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma

def plot_polar_scatter(values, azimuths, zeniths, zeroloc, title, vmin, vmax):
    """ This function makes a polar plot using scatter particles
    Keyword arguments:
    values -- Values of the plot, related to the colors
    azimuths -- Radius (distance from origin)
    zeniths --  Angle of rotation
    """
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    plt.set_cmap('seismic_r')
    plt.title(title)
    values[values>=24] = np.nan
    values[values<=-24] = np.nan
    #cax = ax.scatter( np.radians(zeniths), azimuths, c=values, s = 6, facecolor='0.5', lw= 0, vmin = vmin, vmax = vmax)
    cax = ax.scatter( np.radians(zeniths), azimuths, c=values, s = 6, facecolor='0.5', lw= 0, vmin = vmin, vmax = vmax)
    # Set the zero position of the 0 degree location
    ax.set_theta_zero_location(zeroloc)

    # Direction of the degrees is counter clockwise
    ax.set_theta_direction(-1)
    ax.set_clip_box([-10,10])

    #colorBarTicks = np.arange(min(values),max(values)*1.1, (max(values)-min(values))/10)
    colorBarTicks = np.arange(vmin,vmax*1.1, (vmax-vmin)/10)
    radTicks = np.arange(values.min(),values.max(), (values.max()-values.min())/2)
    # ax.set_yticks(radTicks)
    ax.set_ylim([min(azimuths),max(azimuths)])

    # assign the colorbar
    #cb = fig.colorbar(cax,ticks=colorBarTicks)
    cb = fig.colorbar(cax,ticks=colorBarTicks, boundaries=range(-24,25), values=range(-24,25), extend='both')
    cb.set_label("Velocidad Radial")

    return plt

def plot_polar_contour(values, azimuths, zeniths, zeroloc):
    """ This function is used to plot a polar graph """
    # Converts data to radians
    rad_azimuths = np.radians(azimuths)
    rad_zeniths = np.array(zeniths)
    # Set color map
    values = np.array(values)
    values[values>=24] = np.nan
    values[values<=-24] = np.nan
    # Creates mesh grids from the rad_zeniths and azimuths 
    ZEN, AZI = np.meshgrid(rad_zeniths, rad_azimuths)

    # Define the polar plot
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    plt.set_cmap('seismic_r')

    # Set the zero position of the 0 degree location
    ax.set_theta_zero_location(zeroloc)
    # Direction of the degrees is counter clockwise
    ax.set_theta_direction(-1)

    # Set the contour plot (the plot)
    cax = ax.contourf(AZI, ZEN, values,500)

    # assign the colorbar
    cb = fig.colorbar(cax)
    cb.set_label("Velocidad Radial")
    plt.show()

    return fig, ax, cax


