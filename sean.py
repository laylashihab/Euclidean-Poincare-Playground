import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

def linearInterpolation(numPoints,start,end):
    interpolatedArrays = []

    t_range = np.linspace(0,1,numPoints)
    for t in t_range:
        interpolatedArrays.append((1-t) * start + t*end)
    return interpolatedArrays


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

x = np.linspace(0, 3)
y = np.linspace(0, 3)

def f(x,y):
    return 0.5 * (x**2 - y**2)

X,Y = np.meshgrid(x,y)
a,b = 1,1

flatPlaneX = X
flatPlaneY = Y
flatPlaneZ = X*0

hyperbolicPlaneX = X
hyperbolicPlaneY = Y
hyperbolicPlaneZ = f(X,Y)

for y_val in y:
    ax.plot(X,y_val,f(X,y_val))

ax.plot_surface(hyperbolicPlaneX,hyperbolicPlaneY,hyperbolicPlaneZ, alpha=0.4)

plt.show()

xArrays = linearInterpolation(20, flatPlaneX, hyperbolicPlaneX)
yArrays = linearInterpolation(20, flatPlaneY, hyperbolicPlaneY)
zArrays = linearInterpolation(20, flatPlaneZ, hyperbolicPlaneZ)

metadata = dict(title='Movie',artist="me")
writer = PillowWriter(fps = 15, metadata=metadata)

scope = 5

"""with writer.saving(fig, "animations/sean.gif", 100):
    for i in range(0,len(xArrays)):
        X = xArrays[i]
        Y = yArrays[i]
        Z = zArrays[i]

        # sets scope
        ax.set_xlim(0,scope)
        ax.set_ylim(0,scope)
        ax.set_zlim(0,scope)

        ax.plot_surface(X,Y,Z) 
        ax.plot(X, 1, f(X,1))

        writer.grab_frame()
    
        ax.cla() # clears the previous frame"""