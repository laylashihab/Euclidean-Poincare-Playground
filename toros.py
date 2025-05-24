import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter
import pandas as pd

"""
Creates a 3 dimensional array containing arrays that smoothly transition from the start matrix to the end

Parameters:
numPoints: the number of steps (includes the start and end)
start: two dimensional array containing the starting matrix
end: two dimensional array containing the ending matrix

Returns:
A 3 dimensional array where each element is a surface between the start and end surface (inclusive)
"""
def interpolate(numPoints, start, end):
    interpolatedArrays = [[] for _ in range(numPoints)]

    # iterates through each line in startY
    for i in range(len(start)):
        tempArray = []

        # iterates through each point in the line
        for j in range(len(start[i])):
            tempArray.append(np.linspace(start[i][j], end[i][j],numPoints))

        # tempArray stores a list of lists with the innermost list being points
        tempArray = np.array(tempArray, dtype=np.float64)
        df = pd.DataFrame(tempArray)
        df = df.T
        tempArray = df.to_numpy()

        for k in range(numPoints):
            interpolatedArrays[k].append(tempArray[k])

    return np.array(interpolatedArrays, dtype=np.float64)

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
    
    final = interpolate(numPoints, surfaces[0], surfaces[1])

    for i in range(1,len(surfaces)-1):
        # interpolates between two figures
        temp = interpolate(numPoints, surfaces[i], surfaces[i+1])

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

with writer.saving(fig, "animations/torus.gif", 100):
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