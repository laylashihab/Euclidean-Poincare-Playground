import EventHandlers
import FrameSetUp
import constants as c
import matplotlib.patches as patches

from Point import *
from Line import *
from Circle import *
from Shape import *

import numpy as np
import math

roundVal = 3
boundary = None
poincareShapePlots = []

# maps a point in the euclidean plane to a point in the poincare disc
def euclideanToPoincareFunc(Xe,Ye):
    denom = math.sqrt(1 + Xe**2+Ye**2)
    numerator = Xe
    if denom == 0:
        return None
    Xp = round(numerator/denom,roundVal)
    numerator = Ye
    Yp = round(numerator/denom,roundVal)

    return (Xp,Yp)

def run(button):
    if button.cget("text") == "Poincare Disc":
        button.config(text = "Euclidean Plane")
        euclideanToPoincare()
    else:
        button.config(text = "Poincare Disc")
        poincareToEuclidean()


def euclideanToPoincare():
    shapeList = EventHandlers.shapeList
    plot = EventHandlers.PLOT
    canvas = EventHandlers.CANVAS

    # finds mapping of each point into poincare disc
    for shape in shapeList:
        shape.removeShape()
        (x_data,y_data) = shape.getEuclideanPlotPoints()
        x_dataNew = []
        y_dataNew = []
        for i in range(0,len(x_data)):
            (x,y) = euclideanToPoincareFunc(x_data[i],y_data[i])
            x_dataNew.append(x)
            y_dataNew.append(y)
        shape, = plot.plot(x_dataNew,y_dataNew, color = "black")
        poincareShapePlots.append(shape)
        
    # sets the plot limit to the poincare disc
    plot.set_xlim(-1,1)
    plot.set_ylim(-1,1)
    plot.set_axis_off()

    # draws the poincare disc boundaries
    global boundary
    boundary = patches.Circle((0,0), radius=1, edgecolor='pink', facecolor = 'None')
    plot.add_patch(boundary)   
    canvas.draw()
        
# reverts all plotted shapes and the plot itself to standards for euclidean display
def poincareToEuclidean():
    global poincareShapePlots
    if boundary != None:
        boundary.remove()

    for plot in poincareShapePlots:
        plot.remove()

    poincareShapePlots = []

    # resets plot limits to normal
    plot = EventHandlers.PLOT
    plot.set_xlim(-c.PLOTBOUNDS,c.PLOTBOUNDS)
    plot.set_ylim(-c.PLOTBOUNDS,c.PLOTBOUNDS)
    plot.set_axis_off()

    for shape in EventHandlers.shapeList:
        shape.plotShape(plot)

    EventHandlers.CANVAS.draw()
