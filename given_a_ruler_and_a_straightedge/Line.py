import numpy as np
import math

from Point import *
""""
Class to create Euclidean Line objects

lines are defined by a start and an end point
"""
class Line:
    # instance variables
    __line = None
    __startPoint = None
    __endPoint = None

    __endPointPlot = None
    __startPointPlot = None

    def __init__(self):
        pass

    # plots the line in the given plot and updates the canvas
    def plotShape(self, plot, canvas):
        if self.__endPoint != None:
            x_data = np.linspace(self.__startPoint.getX(), self.__endPoint.getX(), 100)
            y_data = np.linspace(self.__startPoint.getY(), self.__endPoint.getY(),100)
            self.__line, = plot.plot(x_data,y_data, color = "black")

            #plots endpoints
            self.__endPointPlot = self.__endPoint.plotShape(plot,canvas)
            self.__startPointPlot = self.__startPoint.plotShape(plot,canvas)
            #self.__startPointPlot, = plot.plot(self.__startPoint.getX(),self.__startPoint.getY(), "o", color="blue")
            #self.__endPointPlot, = plot.plot(self.__endPoint.getX(),self.__endPoint.getY(), "o",color = "blue")

            canvas.draw()
    
    # removes the endpoints and lines associated with the plotted line
    def removeShape(self,canvas):
        if self.__line != None:
            # removes line and endPoint
            self.__line.remove()
            self.__startPointPlot.remove()
            self.__endPointPlot.remove()
            self.__line = None

            canvas.draw()

    # updates the plot of the shape to a new endpoint
    def draw(self,plot,canvas,endPoint):
        self.removeShape(canvas)
        self.setEndPoint(endPoint)
        self.plotShape(plot,canvas)

    # moves the entire line by a given amount
    def moveShape(self, deltaX,deltaY):
        newStart = Point(self.getStartPoint().getX() + deltaX, self.getStartPoint().getY() + deltaY)
        newEnd = Point(self.getEndPoint().getX() + deltaX, self.getEndPoint().getY() + deltaY)
        self.setEndPoint(newEnd)
        self.setStartPoint(newStart)

    # moves the endPoint to a new location
    def movePoint(self,point, newPoint):
        self.setEndPoint(newPoint)

    # mutators and accessors
    def setStartPoint(self, startPoint):
        self.__startPoint = startPoint

    def setEndPoint(self, endpoint):
        self.__endPoint = endpoint
    
    def getStartPoint(self):
        return self.__startPoint
    
    def getEndPoint(self):
        return self.__endPoint
    
    def getShape(self):
        return self.__line
    
    def getNumComponents(self):
        return 1
    
    # checks if either endpoint equals a given point
    # if so, forces the endPoint to be the given point (line itself doesn't change)
    def containsPoint(self, point):
        if point == None:
            return False
        if point.equals(self.__startPoint):
            # flips start and end points
            temp = self.getStartPoint()
            self.setStartPoint(self.getEndPoint())
            self.setEndPoint(temp)
            return True
        elif point.equals(self.__endPoint):
            return True
        else:
            return False
        
    # returns the exact point on the shape that is very close to the given point
    def getPoint(self,point):
        if (self.containsPoint(point)):
            return self.getEndPoint()

    
    # returns the euclidean distance between two endpoints using Euclid's fifth postulate (Pythagorean thm)
    def getLength(self):
        return math.sqrt(((self.getStartPoint().getX()-self.getEndPoint().getX()))**2+(self.getStartPoint().getY()-self.getEndPoint().getY())**2)
    
    # returns the slope of the line
    def getSlope(self):
        denom = (self.getEndPoint().getX() - self.getStartPoint().getX())
        if (denom == 0):
            return np.inf
        return (self.getEndPoint().getY() - self.getStartPoint().getY())/denom
    
    # returns the angle betweeen the line and another line
    def getAngle(self, line2slope):
        s1 = self.getSlope()
        s2 = line2slope
        angle = math.atan(abs((s1 - s2)/(1 + (s1 * s2))))
        angle = -1 * angle if s1<0 else angle
        return angle
    
    # returns details about the line
    def measure(self):
        returnString = "Length: {0}\nSlope: {1}".format(round(self.getLength(),3),round(self.getSlope(),3))
        return returnString

        
