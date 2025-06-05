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
    def plotShape(self, plot, canvas):
        if self.__centerPoint != None:
            self.__circle = patches.Circle((self.__centerPoint.getX(), self.__centerPoint.getY()), radius=self.__radius, edgecolor='black', facecolor = 'None')

            #plots circle and radius point
            plot.add_patch(self.__circle)
            self.__centerPointPlot, = plot.plot(self.__centerPoint.getX(),self.__centerPoint.getY(), "o", color = "blue")
            canvas.draw()

    # removes circle and center point associated with the plotted circle
    def removeShape(self,canvas):
        if self.__circle != None:
            # removes line and endPoint
            self.__circle.remove()
            self.__centerPointPlot.remove()

            canvas.draw()


    # mutators and accessors

    def setStartPoint(self, centerPoint):
        self.__centerPoint = centerPoint
    
    def movePoint(self, newPoint):
        self.setEndPoint(newPoint)

    # updates the part of the circle that moves (either radius or center point)
    def setEndPoint(self, endPoint):
        # if setting radius for first time, set radius. Else move the center point
        if (self.__moveCenter):
            self.moveShape(endPoint)
        else:
            self.__radius = math.sqrt(((self.__centerPoint.getX()-endPoint.getX()))**2+(self.__centerPoint.getY()-endPoint.getY())**2)

    def moveShape(self, deltaX, deltaY):
        newPoint = Point(self.getCenterPoint().getX()+deltaX, self.getCenterPoint().getY() + deltaY)
        self.__centerPoint = newPoint
        #self.__circle = None

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
    
    # checks if a given point is the center point
    # if so, marks that the center will be move (radius will not be adjusted)
    def containsPoint(self, point):
        if point.equals(self.__centerPoint):
            self.__moveCenter = True #implies that circle is fully drawn and can only be moved now (radius will not change)
            return True
        else: 
            return False
        
    def getPoint(self,point):
        if (self.containsPoint(point)):
            return self.getEndPoint()

        
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
