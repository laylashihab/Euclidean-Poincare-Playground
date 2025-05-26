import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter
import pandas as pd

"""
provides an array of surface plots that linearly interpolate between two plots

parameters:
numPoints: the number of arrays to get from start to end (inclusive)
start: the start plot
end: the end plot

returns:
an array of surface plots
"""
def linearInterpolation(numPoints,start,end):
    interpolatedArrays = []

    t_range = np.linspace(0,1,numPoints)
    for t in t_range:
        interpolatedArrays.append((1-t) * start + t*end)
    return interpolatedArrays


"""
Combines multiple transformations between a number of surfaces for one dimension (X, Y,Z)

Parameters:
surfaces: a list of all the surfaces to transform between (len >= 2)
numPoints: the number of steps to take between any two surfaces

Returns:
A 3 dimensional array that smoothly transitions between each provided surface for one dimension
"""
def combineSurfaceTransformations(surfaces, numPoints):
    if (len(surfaces) < 2):
        raise Exception("Please provide at least two shapes")
    
    final = linearInterpolation(numPoints, surfaces[0], surfaces[1])

    for i in range(1,len(surfaces)-1):
        # interpolates between two figures
        temp = linearInterpolation(numPoints, surfaces[i], surfaces[i+1])

        final = np.concatenate((final,temp), axis = 0)

    return final

#variables 
radius = 3 / (2 * np.pi)
numPoints = 50
scope = 2

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

x_data = np.linspace(0,3,100)
y_data = np.linspace(0,3,100)

# flat plane
planeX, planeY = np.meshgrid(x_data, y_data)
planeZ = planeX * 0

# cylinder
theta = np.linspace(0,4*np.pi,100)
t = np.linspace(0, 3, 100)
theta_grid, t_grid = np.meshgrid(theta,t)

cylX = t_grid
cylY = radius * np.cos(theta_grid)
cylZ = radius * np.sin(theta_grid) + 1.5

#torus 
theta = np.linspace(0, 2.*np.pi, 100)
phi = np.linspace(0, 2.*np.pi, 100)
theta, phi = np.meshgrid(theta, phi)
c = 1
torusX = (c + radius*np.cos(theta)) * np.cos(phi)
torusY = (c + radius*np.cos(theta)) * np.sin(phi)
torusZ = radius * np.sin(theta)

#combines the shapes together
XArray = combineSurfaceTransformations([planeX,cylX,torusX,planeX], 30)
YArray = combineSurfaceTransformations([planeY,cylY,torusY,planeY], 30)
ZArray = combineSurfaceTransformations([planeZ,cylZ,torusZ,planeZ], 30)

#animation
metadata = dict(title='Movie',artist="me")
writer = PillowWriter(fps = 15, metadata=metadata)

with writer.saving(fig, "animations/LinearTransformationTorus.gif", 100):
    for i in range(0,len(XArray)):
        # sets scope
        ax.set_xlim(-scope,scope)
        ax.set_ylim(-scope,scope)
        ax.set_zlim(-scope,scope)

        X = XArray[i]
        Y = YArray[i]
        Z = ZArray[i]

        ax.plot_surface(X,Y,Z) # coloring the surface, other color maps available

        writer.grab_frame()
    
        ax.cla() # clears the previous frame