import EventHandlers
import constants as c
import matplotlib.patches as patches

import math
import numpy as np

# TODO: link references and credits

boundary = None
# takes poincare tuples as keys and euclidean tuples as values
poincareToEuclideanDict = {}

# maps a point in the euclidean plane to a point in the poincare disc
def euclideanToPoincareFunc(Xe,Ye):
    theta = np.atan2(Ye,Xe)
    # finds the euclidean distance to origin such that the original euclidean distance and new hyperbolic distance are equal
    d = math.sqrt(Xe**2 + Ye**2) / EventHandlers.plotbounds # scales to plotbounds
    numerator = math.e**(2*d) - 1
    denominator = math.e**(2*d) + 1
    r = numerator/denominator

    # scale by disc radius 
    r = r * EventHandlers.plotbounds

    Xp = r * np.cos(theta)
    Yp = r * np.sin(theta)

    return (Xp,Yp)

def poincareToEuclideanFunc(Xp,Yp):
    theta = np.atan2(Yp,Xp)
    # finds the new euclidean distance to origin such that the original hyperbolic distance and new euclidean distances are equal
    d = math.sqrt(Xp**2 + Yp**2) / EventHandlers.plotbounds # scales to plotbounds
    # caps d so that there are no floating point errors leading to domain error
    d = min(max(d, 1e-10), 0.999999)
    r = 0.5 * math.log(((1+d)/(1-d)))

    # scale by disc radius 
    r = r * EventHandlers.plotbounds

    Xe = r * np.cos(theta)
    Ye = r * np.sin(theta)

    return (Xe,Ye)

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
    plot = EventHandlers.PLOT

    # finds mapping of each point into poincare disc
    for shape in EventHandlers.shapeList:
        shape.removeShape()
        shape.convertToPoincare()
        shape.plotShape(plot,poincare=True)

    # draws the poincare disc boundaries
    global boundary
    boundary = patches.Circle((0,0), radius=EventHandlers.plotbounds, edgecolor='pink', facecolor = 'None')
    plot.add_patch(boundary)   
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

    EventHandlers.CANVAS.draw()
