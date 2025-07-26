import EventHandlers
import FrameSetUp
import constants as c
import matplotlib.patches as patches
from Shape import *

import math
import numpy as np

# TODO link references and citations

boundary = None

# maps a point in the euclidean plane to a point in the poincare disc
def euclideanToPoincareFunc(Xe,Ye, scaler = c.PLOTBOUNDS):
    theta = np.atan2(Ye,Xe)
    # finds the euclidean distance to origin such that the original euclidean distance and new hyperbolic distance are equal
    d = math.sqrt(Xe**2 + Ye**2) 
    numerator = math.e**(2*d) - 1
    denominator = math.e**(2*d) + 1
    r = numerator/denominator
    r /= scaler

    Xp = r * np.cos(theta)
    Yp = r * np.sin(theta)

    return (Xp,Yp)

def poincareToEuclideanFunc(Xp,Yp, scaler = c.PLOTBOUNDS):
    theta = np.atan2(Yp,Xp)
    # finds the new euclidean distance to origin such that the original hyperbolic distance and new euclidean distances are equal
    d = math.sqrt(Xp**2 + Yp**2) 
    d *= scaler
    # caps d so that there are no floating point errors leading to domain error
    d = min(max(d, 1e-10), 0.999999)
    r = 0.5 * math.log(((1+d)/(1-d)))

    Xe = r * np.cos(theta)
    Ye = r * np.sin(theta)

    return (Xe,Ye)

# given the two endpoints and radius of the disc, returns the radius and center points of the Euclidean circle connecting them
def findConnectingCircle(x0,y0,x1,y1, radius = 1):
    numX = y0 * (x1**2 + y1**2 + radius**2)-y1 * (x0**2 + y0**2 + radius**2)
    numY = x1 * (x0**2 + y0**2 + radius**2)-x0 * (x1**2 + y1**2 + radius**2)
    denom = 2 * ( (x1 * y0) - (x0 * y1))
    centerX = numX/denom
    centerY = numY/denom
    r = math.sqrt(centerX**2 + centerY ** 2 - radius**2)
    return r,centerX,centerY
    
def run():
    poincareButton = FrameSetUp.poincareButton
    showAnglesButton = FrameSetUp.showAnglesButton
    showMetricsButton = FrameSetUp.showMetricsButton
    if poincareButton.cget("text") == "Poincare Disc":
        # transforms to poincare disc
        poincareButton.config(text = "Euclidean Plane")
        showAnglesButton.grid_remove()
        showMetricsButton.grid_remove()
                
        euclideanToPoincare()
    else:
        poincareButton.config(text = "Poincare Disc")
        showAnglesButton.grid()
        showMetricsButton.grid()

        poincareToEuclidean()



def drawBoundary():
    # draws the poincare disc boundaries
    global boundary
    boundary = patches.Circle((0,0), radius=1, edgecolor='pink', facecolor = 'None')
    EventHandlers.PLOT.add_patch(boundary)   

def euclideanToPoincare():
    EventHandlers.poincareMode = True

    FrameSetUp.PLOT.set_xlim(-1,1)
    FrameSetUp.PLOT.set_ylim(-1,1)
    FrameSetUp.zoomSlider.set(100)
    Point.epsilon = (0.05)


    # finds mapping of each point into poincare disc
    for shape in EventHandlers.shapeList:
        shape.hideMetrics()
        if type(shape) == Shape:
            shape.hideAngles()
        shape.removeShape()
        shape.convertToPoincare()
        shape.plotShape(EventHandlers.PLOT,poincare=True)
    
    drawBoundary()

    EventHandlers.CANVAS.draw()
        
# reverts all plotted shapes and the plot itself to standards for euclidean display
def poincareToEuclidean():
    EventHandlers.poincareMode = False
    if boundary != None:
        boundary.remove()

    plot = EventHandlers.PLOT

    for shape in EventHandlers.shapeList:
        shape.removeShape()
        shape.convertToEuclidean()
        shape.plotShape(plot,poincare=False)

    plotBounds = EventHandlers.plotBounds
    EventHandlers.PLOT.set_xlim(- plotBounds + EventHandlers.xBoundDelta,plotBounds + EventHandlers.xBoundDelta)
    EventHandlers.PLOT.set_ylim(- plotBounds + EventHandlers.yBoundDelta,plotBounds + EventHandlers.yBoundDelta)
    Point.epsilon = (c.EPSILON)

    if FrameSetUp.showAnglesButton.cget("text") == "Hide Angles":
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.showAngles(EventHandlers.PLOT)
    
    if FrameSetUp.showMetricsButton.cget("text") == "Hide Metrics":
        for shape in EventHandlers.shapeList:
            shape.showMetrics(EventHandlers.PLOT)

    EventHandlers.CANVAS.draw()
