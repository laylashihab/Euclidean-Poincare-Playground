import EventHandlers
import constants as c
import matplotlib.patches as patches

from Point import *
import Line
from Circle import *
from Shape import *

import math

boundary = None
# takes poincare tuples as keys and euclidean tuples as values
poincareToEuclideanDict = {}

# maps a point in the euclidean plane to a point in the poincare disc
def euclideanToPoincareFunc(Xe,Ye):
    t = 0.5 * EventHandlers.plotbounds**2 - (Xe**2 + Ye**2)
    if (t < 0):
        return Xe,Ye
    denom = math.sqrt(t)
    if denom == 0:
        return None
    Xp = Xe /denom
    Yp = Ye/denom

    poincareToEuclideanDict[(Xp,Yp)]=(Xe,Ye)

    return (Xp,Yp)

def poincareToEuclideanFunc(Xp,Yp):
    t = EventHandlers.plotbounds**2 - (Xe**2 + Ye**2)

# given the two endpoints and radius of the disc, returns the radius and center points of the Euclidean circle connecting them
def findConnectingCircle(x0,y0,x1,y1, radius = EventHandlers.plotbounds):
    numX = y0 * (x1**2 + y1**2 + radius**2)-y1 * (x0**2 + y0**2 + radius**2)
    numY = x1 * (x0**2 + y0**2 + radius**2)-x0 * (x1**2 + y1**2 + radius**2)
    denom = 2 * ( (x1 * y0) - (x0 * y1))
    centerX = numX/denom
    centerY = numY/denom
    r = math.sqrt(centerX**2 + centerY ** 2 - radius**2)
    return r,centerX,centerY
    
def run(button):
    if button.cget("text") == "Poincare Disc":
        button.config(text = "Euclidean Plane")
        euclideanToPoincare()
    else:
        button.config(text = "Poincare Disc")
        poincareToEuclidean()


def euclideanToPoincare():
    EventHandlers.poincareMode = True
    Point.epsilon = c.EPSILON 
    plot = EventHandlers.PLOT

    # finds mapping of each point into poincare disc
    for shape in EventHandlers.shapeList:
        shape.removeShape()
        # moves endpoints
        if type(shape) == Line.Line:
            newEndPointX,newEndPointY = euclideanToPoincareFunc(shape.getEndPoint().getX(), shape.getEndPoint().getY())
            newEnd = Point(newEndPointX,newEndPointY)
            newStartPointX,newStartPointY = euclideanToPoincareFunc(shape.getStartPoint().getX(), shape.getStartPoint().getY())
            newStart = Point(newStartPointX,newStartPointY)

            shape.setEndPoint(newEnd)
            shape.setStartPoint(newStart)

        elif type(shape) == Circle:
            newCenterPointX,newCenterPointY = euclideanToPoincareFunc(shape.getCenterPoint().getX(), shape.getCenterPoint().getY())
            newCenter = Point(newCenterPointX,newCenterPointY)

            shape.setPoincareEndPoint(newCenter)
        else:
            newX,newY = euclideanToPoincareFunc(shape.getX(), shape.getY())
            shape.setX(newX)
            shape.setY(newY)
        shape.plotShape(plot,poincare=True)
        
    plotbounds = EventHandlers.plotbounds
    # draws the poincare disc boundaries
    global boundary
    boundary = patches.Circle((0,0), radius=plotbounds, edgecolor='pink', facecolor = 'None')
    plot.add_patch(boundary)   
    EventHandlers.CANVAS.draw()
        
# reverts all plotted shapes and the plot itself to standards for euclidean display
def poincareToEuclidean():
    Point.epsilon = c.EPSILON
    EventHandlers.poincareMode = False
    if boundary != None:
        boundary.remove()

    plot = EventHandlers.PLOT

    for shape in EventHandlers.shapeList:
        shape.removeShape()
        # moves endpoints
        if type(shape) == Line.Line:
            newEndPointX,newEndPointY = poincareToEuclideanDict[shape.getEndPoint().getX(),shape.getEndPoint().getY()]
            newEnd = Point(newEndPointX,newEndPointY)
            newStartPointX,newStartPointY = poincareToEuclideanDict[shape.getStartPoint().getX(),shape.getStartPoint().getY()]
            newStart = Point(newStartPointX,newStartPointY)

            shape.setEndPoint(newEnd)
            shape.setStartPoint(newStart)

        elif type(shape) == Circle:
            newCenterX,newCenterY = poincareToEuclideanDict[shape.getCenterPoint().getX(),shape.getCenterPoint().getY()]
            newCenter = Point(newCenterX,newCenterY)

            shape.setCenterPoint(newCenter)
        else:
            newX,newY = euclideanToPoincareFunc(shape.getX(), shape.getY())
            shape.setX(newX)
            shape.setY(newY)
        shape.plotShape(plot,poincare=False)

    EventHandlers.CANVAS.draw()
