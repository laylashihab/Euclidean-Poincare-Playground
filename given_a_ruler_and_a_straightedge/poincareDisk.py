import EventHandlers
import FrameSetUp
import constants as c
import matplotlib.patches as patches
from Shape import *

import math
import numpy as np

# TODO link references and citations
# TODO ensure that when moving lines in poincare mode, the distances are being appropriately updated

boundary = None

# maps a point in the euclidean plane to a point in the poincare disc based on a stereographic projection of a hyperboloid
def euclideanToPoincareFunc(Xe,Ye):
    s = (Xe**2 + Ye **2 + 1)

    Xp = Xe / (1 + np.sqrt(s))
    Yp = Ye / (1 + np.sqrt(s))

    return (Xp,Yp)

# maps a point in the poincare plane to a point in the euclidean place based on a stereographic projection of a hyperboloid
def poincareToEuclideanFunc(Xp,Yp):
    d = (Xp**2 + Yp**2 -1)

    Ye = -(2 * Yp) / d 
    Xe =  -(2 * Xp) / d 

    return Xe, Ye

def findPQPrime(Px,Py, Qx,Qy):
    r,Cx,Cy = findConnectingCircle(Px,Py,Qx,Qy)

    # https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
    d = np.sqrt((Cx)**2+(Cy)**2)
    l = (1 - (r**2) + d**2)/ (2 * d)
    h = np.sqrt(1-l**2)

    x1 = (l/d) * (Cx) + (h/d) * (Cy)
    x2 = (l/d) * (Cx) - (h/d) * (Cy)
    y1 = (l/d) * (Cy) - (h/d) * (Cx)
    y2 = (l/d) * (Cy) + (h/d) * (Cx)

    pPrime = Point.Point(x1,y1)
    qPrime = Point.Point(x2,y2)

    return pPrime, qPrime

def findHyperbolicDistance(P,Q):
    #https://math.stackexchange.com/questions/3910376/how-to-determine-distance-between-two-points-in-poincare
    pPrime, qPrime = findPQPrime(P.getX(),P.getY(),Q.getX(),Q.getY())

    PQprime = P.getDistance(qPrime)
    QPprime = Q.getDistance(pPrime)
    PPprime = P.getDistance(pPrime)
    QQprime = Q.getDistance(qPrime)

    distance = np.log((PQprime * QPprime)/(PPprime * QQprime))

    return distance

# given the two endpoints and radius of the disc, returns the radius and center points of the Euclidean circle connecting them
def findConnectingCircle(x0,y0,x1,y1, radius = 1):
    numX = y0 * (x1**2 + y1**2 + radius**2)-y1 * (x0**2 + y0**2 + radius**2)
    numY = x1 * (x0**2 + y0**2 + radius**2)-x0 * (x1**2 + y1**2 + radius**2)
    denom = 2 * ( (x1 * y0) - (x0 * y1))
    if denom == 0:
        return np.inf, np.inf,np.inf
    centerX = numX/denom
    centerY = numY/denom
    r = math.sqrt(centerX**2 + centerY ** 2 - radius**2)
    return r,centerX,centerY
    
def run(poincareOn):
    if poincareOn:    
        euclideanToPoincare()
    else:
        poincareToEuclidean()

def drawBoundary():
    # draws the poincare disc boundaries
    global boundary
    boundary = patches.Circle((0,0), radius=1, edgecolor='pink', facecolor = 'None')
    EventHandlers.PLOT.add_patch(boundary)   

def euclideanToPoincare():
    EventHandlers.poincareMode = True
    EventHandlers.clearCurrentShape()

    FrameSetUp.PLOT.set_xlim(-1,1)
    FrameSetUp.PLOT.set_ylim(-1,1)
    FrameSetUp.PLOT.grid(False)
    FrameSetUp.zoomSlider.set(100)
    Point.Point.setEpsilon(c.POINCAREEPSILON)

    # updates data display
    FrameSetUp.dataDisplay.config(text="")
    FrameSetUp.dataDisplay.update()

    # finds mapping of each point into poincare disc
    for shape in EventHandlers.getShapeList():
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

    EventHandlers.clearCurrentShape()

    for shape in EventHandlers.shapeList:
        shape.removeShape()
        shape.convertToEuclidean()
        shape.plotShape(plot,poincare=False)

    plotBounds = EventHandlers.plotBounds
    EventHandlers.PLOT.set_xlim(- plotBounds + EventHandlers.xBoundDelta,plotBounds + EventHandlers.xBoundDelta)
    EventHandlers.PLOT.set_ylim(- plotBounds + EventHandlers.yBoundDelta,plotBounds + EventHandlers.yBoundDelta)
    Point.Point.setEpsilon(c.EPSILON)

    if FrameSetUp.anglesOn:
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.showAngles(EventHandlers.PLOT)
    
    if FrameSetUp.metricsOn:
        for shape in EventHandlers.shapeList:
            shape.showMetrics(EventHandlers.PLOT)

    EventHandlers.CANVAS.draw()
