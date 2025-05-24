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

# interpolates between two figures
i1X = interpolate(numPoints, planeX, cylX)
i1Y = interpolate(numPoints, planeY, cylY)
i1Z = interpolate(numPoints, planeZ, cylZ)

i2X = interpolate(numPoints, cylX, torusX)
i2Y = interpolate(numPoints, cylY, torusY)
i2Z = interpolate(numPoints, cylZ, torusZ)

iX = np.concatenate((i1X, i2X), axis = 0)
iY = np.concatenate((i1Y, i2Y), axis = 0)
iZ = np.concatenate((i1Z, i2Z), axis = 0)

#animation
metadata = dict(title='Movie',artist="me")
writer = PillowWriter(fps = 15, metadata=metadata)


with writer.saving(fig, "animations/torus.gif", 100):
    for i in range(0,len(iX)):
        # sets scope
        ax.set_xlim(-scope,scope)
        ax.set_ylim(-scope,scope)
        ax.set_zlim(-scope,scope)

        X = iX[i]
        Y = iY[i]
        Z = iZ[i]

        ax.plot_surface(X,Y,Z) # coloring the surface, other color maps available

        writer.grab_frame()
    
        ax.cla() # clears the previous frame