import math
import matplotlib.patches as patches
import copy
import constants as c
import numpy as np
import poincareDisk

""""
class to create Euclidean Circle objects

Cirles are defined by a center point and radius
"""

import Point

class Circle:
    __circle = None
    __centerPoint = None
    __radius = None

    __centerPointPlot = None
    __moveCenter = False
    
    __poincare = False # boolean flag for if points are poincare versions

    def __init__(self, poincare = False):
        self.__poincare = poincare

    # plots the circle and center point in a given plot and updates canvas
    def plotShape(self, plot, linewidth = c.THINLINE, poincare = False):
        if poincare == True:
            self.plotShapePoincare(plot, linewidth=linewidth)
            return            
        if self.__centerPoint != None:
            self.__circle = patches.Circle((self.__centerPoint.getX(), self.__centerPoint.getY()), radius=self.__radius, edgecolor='black', facecolor = 'None', linewidth= linewidth)

            #plots circle and radius point
            plot.add_patch(self.__circle)
            self.__centerPointPlot = self.__centerPoint.plotShape(plot,linewidth)

    def plotShapePoincare(self,plot,linewidth=c.THINLINE):
        if self.__centerPoint != None:
            r = self.getRadius()
            x0 = self.getCenterPoint().getX()
            y0 = self.getCenterPoint().getY()
            const = (1 - x0**2 - y0**2)

            xrange = np.linspace(-1, 1, 500)
            yrange = np.linspace(-1, 1, 500)
            X, Y = np.meshgrid(xrange,yrange)
            
            mask = (X**2 + Y**2 >= 1)

            F = 4 * ((x0 - X)**2 + (y0 - Y)**2)
            G = const * (1 - X**2 - Y**2)

            # creates an array of np.nan with the same shape as X
            Z = np.full_like(X, np.nan)
            # fills the array when the inputs are inside the unit circle
            Z[~mask] = F[~mask] / G[~mask] - r

            self.__circle = plot.contour(X,Y,Z,[0], colors="black")
            self.__centerPointPlot = self.__centerPoint.plotShape(plot)

    def convertToPoincare(self):
        if self.__poincare == False:
            self.getCenterPoint().convertToPoincare()
            self.__poincare = True

    def convertToEuclidean(self):
        if self.__poincare == True:
            self.getCenterPoint().convertToEuclidean()
            self.__poincare = False

    #plots the line on a scaled canvas
    def plotShapeScaledPlotsize(self,plot,oldPlotSize, newPlotSize):
        # calculates scalefactor
        scaleFactor = newPlotSize / oldPlotSize

        # ensures that the shape is not mutated
        figure = copy.deepcopy(self)

        figure.getCenterPoint().setPointSize(c.DEFAULTPOINTSIZE*scaleFactor)
        figure.plotShape(plot,c.THINLINE)

    #scales the whole circle by a given amount, but preserves original radius
    def scale(self,scaleVal,plot,poincare = False):
        self.removeShape()
        oldRadius = self.getRadius()
        newRadius = scaleVal * oldRadius
        self.setRadius(newRadius)
        self.plotShape(plot,c.THICKLINE, poincare=poincare)
        self.setRadius(oldRadius)

    # modifies original radius and scales
    def confirmScaleSize(self,scaleVal,plot, poincare = False):
        self.removeShape()
        oldRadius = self.getRadius()
        newRadius = scaleVal * oldRadius
        self.setRadius(newRadius)
        self.plotShape(plot,c.THICKLINE, poincare=poincare)

    # removes circle and center point associated with the plotted circle
    def removeShape(self):
        if self.__circle != None:
            # removes line and endPoint
            self.__circle.remove()
            self.__circle = None
            self.__centerPointPlot.remove()

    # moves the entire shape by a given amount
    def moveShape(self, deltaX, deltaY):
        self.__centerPoint =Point.Point(self.getCenterPoint().getX()+deltaX, self.getCenterPoint().getY() + deltaY)
    
    # takes a euclidean x and y to move 
    def moveShapePoincare(self,deltaX=0,deltaY=0):
        self.getCenterPoint().moveShapePoincare(deltaX,deltaY)

    def showMetrics(self,plot):
        pass

    def hideMetrics(self):
        pass

    # mutators and accessors
    def setStartPoint(self, centerPoint):
        self.__centerPoint = centerPoint

    def setCenterPoint(self, centerPoint):
        self.__centerPoint = centerPoint
    
    def movePoint(self, pointToMove, newPoint):
        self.setCenterPoint(newPoint)

    # updates the part of the circle that moves (either radius or center point)
    def setEndPoint(self, endPoint):
        # if setting radius for first time, set radius. Else move the center point
        if (self.__moveCenter):
            self.__centerPoint = endPoint
        else:
            self.__radius = math.sqrt(((self.__centerPoint.getX()-endPoint.getX()))**2+(self.__centerPoint.getY()-endPoint.getY())**2)

    def setRadius(self,radius):
        self.__radius = radius

    def getCenterPoint(self):
        return self.__centerPoint
    
    def getRadius(self):
        return self.__radius
    
    def getShape(self):
        return self.__circle
    
    def getStartPoint(self):
        return self.__centerPoint
    
    def getEndPoint(self):
        return self.__centerPoint
    
    def isClosedFigure(self):
        return True
    
    def getPoincare(self):
        return self.__poincare
    
    # checks if a given point is the center point
    # if so, marks that the center will be move (radius will not be adjusted)
    def containsPoint(self, point):
        if point.equals(self.__centerPoint):
            self.__moveCenter = True #implies that circle is fully drawn and can only be moved now (radius will not change)
            return True
        else: 
            return False
        
    # checks if the exact given point is contained in the figure
    def exactContainsPoint(self,point):
        if (self.getCenterPoint().getX() == point.getX() or self.getCenterPoint().getY() == point.getY()):
            return True
        else:
            return False

    # gets the exact point associated with the circle given the point is contained in the circle
    # essentially removes the epsilon value associated with a contained point for smoother joining of shapes
    def getPoint(self,point):
        if (self.containsPoint(point)):
            return self.getEndPoint()

    # returns the circumference
    def getLength(self):
        return self.getCircumference()
        
    # returns the euclidean distance around the circle
    def getCircumference(self):
        return math.pi * 2 * self.__radius
    
    # returns the euclidean area of the circle
    def getArea(self):
        return math.pi * (self.__radius ** 2)
    
    # annotates various measurements on the circle
    def measure(self):
        label = "Radius: {0}\nCircumference: {1}\nArea: {2}".format(round(self.getRadius(), 3), round(self.getCircumference(),3),round(self.getArea(),3))
        return label

    def print(self):
        string = "Circle: " + str(self)
        string += "\n\tCenterPoint: " + str(self.getCenterPoint()) 
        print(string)
