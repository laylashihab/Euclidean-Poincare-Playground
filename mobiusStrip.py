# file to visualize a mobius strip in 3 dimensional space using matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter

# variables
radius = 1

#may be able to remove later 
from mpl_toolkits import mplot3d

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# sets scope
m = 3
ax.set_xlim(-m,m)
ax.set_ylim(-m,m)
ax.set_zlim(-m,m)


# Make data
theta = np.linspace(0,4*np.pi,100)
t = np.linspace(0, radius, 100)
theta_grid, t_grid = np.meshgrid(theta,t)

a,b,c,d,e = 1,1,1,1,1

X = a * np.cos(theta_grid)*(radius + b * (t_grid * np.cos(c* 0.5 * theta_grid)))
Y = a * np.sin(theta_grid)*(radius + b * (t_grid * np.cos(c* 0.5 * theta_grid)))
Z = d* t_grid * np.sin(e * 0.5 * theta_grid)


ax.plot_surface(X,Y,Z, cmap="gnuplot") # coloring the surface, other color maps available


plt.show()

