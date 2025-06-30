import math
import matplotlib.patches as patches

""""
class to create Euclidean Circle objects

Cirles are defined by a center point and radius
"""

from Point import *

class Circle:
    __circle = None
    __centerPoint = None
    __radius = None

    __centerPointPlot = None
    __moveCenter = False
    

    def __init__(self):
        pass

    # plots the circle and center point in a given plot and updates canvas
    def plotShape(self, plot, canvas, linewidth):
        if self.__centerPoint != None:
            self.__circle = patches.Circle((self.__centerPoint.getX(), self.__centerPoint.getY()), radius=self.__radius, edgecolor='black', facecolor = 'None', linewidth= linewidth)

            #plots circle and radius point
            plot.add_patch(self.__circle)
            self.__centerPointPlot = self.__centerPoint.plotShape(plot,canvas,linewidth)
            canvas.draw()

    # removes circle and center point associated with the plotted circle
    def removeShape(self,canvas):
        if self.__circle != None:
            # removes line and endPoint
            self.__circle.remove()
            self.__circle = None
            self.__centerPointPlot.remove()

            canvas.draw()

    # moves the entire shape by a given amount
    def moveShape(self, deltaX, deltaY):
        self.__centerPoint = Point(self.getCenterPoint().getX()+deltaX, self.getCenterPoint().getY() + deltaY)
    
    def showMetrics(self,plot, canvas):
        pass

    def hideMetrics(self, canvas):
        pass

    # mutators and accessors
    def setStartPoint(self, centerPoint):
        self.__centerPoint = centerPoint

    def setCenterPoint(self, centerPoint):
        self.__centerPoint = centerPoint
    
    def movePoint(self, point, newPoint):
        self.setEndPoint(newPoint)

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
    
    def getEndPoint(self):
        return self.__centerPoint
    
    def getNumComponents(self):
        return 1
    
    def isClosedFigure(self):
        return True
    
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
