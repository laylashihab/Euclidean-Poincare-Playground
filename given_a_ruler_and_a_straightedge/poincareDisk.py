import EventHandlers
import constants as c
import matplotlib.patches as patches

from Point import *
from Line import *
from Circle import *
from Shape import *

import numpy as np
import math

boundary = None

# maps a point in the euclidean plane to a point in the poincare disc
def euclideanToPoincareFunc(Xe,Ye):
    denom = math.sqrt(1 + Xe**2+Ye**2)
    numerator = Xe
    if denom == 0:
        return None
    Xp = numerator/denom
    numerator = Ye
    Yp = numerator/denom

    return (Xp,Yp)

def run(button):
    if button.cget("text") == "Poincare Disc":
        button.config(text = "Euclidean Plane")
        euclideanToPoincare()
    else:
        button.config(text = "Poincare Disc")
        poincareToEuclidean()


def euclideanToPoincare():
    EventHandlers.poincareMode = True
    plot = EventHandlers.PLOT

    # finds mapping of each point into poincare disc
    for shape in EventHandlers.shapeList:
        shape.removeShape()
        shape.plotShape(plot,poincare=True)
        
    # sets the plot limit to the poincare disc
    plot.set_xlim(-1,1)
    plot.set_ylim(-1,1)
    plot.set_axis_off()

    # draws the poincare disc boundaries
    global boundary
    boundary = patches.Circle((0,0), radius=1, edgecolor='pink', facecolor = 'None')
    plot.add_patch(boundary)   
    EventHandlers.CANVAS.draw()
        
# reverts all plotted shapes and the plot itself to standards for euclidean display
def poincareToEuclidean():
    EventHandlers.poincareMode = False
    if boundary != None:
        boundary.remove()

    # resets plot limits to normal
    plot = EventHandlers.PLOT
    plot.set_xlim(-c.PLOTBOUNDS,c.PLOTBOUNDS)
    plot.set_ylim(-c.PLOTBOUNDS,c.PLOTBOUNDS)
    plot.set_axis_off()

    for shape in EventHandlers.shapeList:
        shape.removeShape()
        shape.plotShape(plot)

    EventHandlers.CANVAS.draw()
