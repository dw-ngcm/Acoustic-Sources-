# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:14:53 2018

Class definitions of acoustic sources and environment
Initially, in 2D only

@author: djw1g12
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class env(object):
    """ 2D environment

    METHODS
    -------
    __init__ : initialise internal variables
    pressure : plot pressure amplitude
    spl : plot sound pressure level """

    def __init__(self, xlim, ylim, resolution, c):
        """ Initialise internal variables
        INPUTS
        ------
        x = 2-tuple (xmin, xmax)
        y = 2-tuple (ymin, ymax)
        resolution = scalar number of points per linear metre
        c = scalar speed of sound

        """
        assert len(list(xlim)) == 2, 'Usage: xlim = [xmin, xmax]'
        assert len(list(ylim)) == 2, 'Usage: ylim = [ymin, ymax]'
        xmin, xmax = xlim
        ymin, ymax = ylim
        x = np.linspace(xmin, xmax, np.int(np.floor((xmax-xmin)*resolution)))
        y = np.linspace(ymin, ymax, np.int(np.floor((ymax-ymin)*resolution)))
        self.X, self.Y = np.meshgrid(x, y)  # set X and Y coordinate grids
        self.p = np.zeros_like(self.X, dtype=np.complex128)  # pressure grid
        self.sourceList = []
        self.c = c

    def pressure(self):
        """ Plot pressure in the environment at t = 0 """
        plt.figure()
        plt.imshow(np.real(self.p), extent=(self.X.min(), self.X.max(),
                                            self.Y.min(), self.Y.max()))
        plt.colorbar()
        plt.clim(-5, 5)

    def spl(self):
        """ Plot sound pressure level in the environment at t = 0 """
        plt.figure()
        plt.imshow(20*np.log10(np.abs(self.p)/20*10**-6),
                   extent=(self.X.min(), self.X.max(),
                   self.Y.min(), self.Y.max()))
        plt.colorbar()

    def addSource(self, source):
        """ Adds a source to the environment
        INPUTS
        ------
        source - object of superclass source
            could be a monopole
        """
        self.sourceList.append(source)
        r = np.sqrt((self.X-source.x)**2+(self.Y-source.y)**2)
        pAdd = source.func(r, self.c)
        self.p = self.p+pAdd


class monopole(object):
    """ monopole source

    METHODS
    -------
    __init__ : generate source

    """
    def __init__(self, coords, amp, freq, phase):
        self.x, self.y = coords
        self.amp = amp
        self.freq = freq
        self.phase = phase
        self.func = lambda r, c: amp*np.exp(
                1j*(2*np.pi*freq/c)*r)*np.exp(1j*phase)/(4*np.pi*r)


if __name__ == '__main__':  # if run from the command line or IDE
    E = env(xlim=[-0.5, 1], ylim=[-1., 1.], resolution=200, c=343)
    n = 10
    xcoords = np.linspace(-0.3, 0.3, n)
    ycoords = np.sin
    phases = np.linspace(0, np.pi, n)
    for xCoord, theta in zip(xcoords, phases):
        M = monopole([xCoord, 0], 1, 1000, theta)
        E.addSource(M)
    E.pressure()
    E.spl()

    E2 = env(xlim=[-1., 1.], ylim=[-1., 1.], resolution=200, c=343)
    n = 3
    r = 0.5
    angles = np.linspace(0, 2*np.pi, n+1)[0:-1]
    xcoords = np.cos(angles)*r
    ycoords = np.sin(angles)*r
    phases = np.linspace(0, np.pi, n+1)[0:-1]
    for xCoord, yCoord, theta in zip(xcoords, ycoords, phases):
        M = monopole([xCoord, yCoord], 1, 1000, theta)
        E2.addSource(M)
    E2.pressure()
    E2.spl()
