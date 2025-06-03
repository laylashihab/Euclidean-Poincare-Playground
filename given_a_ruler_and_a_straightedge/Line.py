import numpy as np
import math
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
            line, = plot.plot(x_data,y_data)
            self.__line = line

            #plots endpoints
            self.__startPointPlot, = plot.plot(self.__startPoint.getX(),self.__startPoint.getY(), "o")
            self.__endPointPlot, = plot.plot(self.__endPoint.getX(),self.__endPoint.getY(), "o")
            canvas.draw()
    
    # removes the endpoints and lines associated with the plotted line
    def removeShape(self,canvas):
        if self.__endPointPlot != None:
            # removes line and endPoint
            self.__line.remove()
            self.__startPointPlot.remove()
            self.__endPointPlot.remove()
            canvas.draw()

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
    
    # checks if either endpoint equals a given point
    # if so, forces the endPoint to be the given point (line itself doesn't change)
    def containsPoint(self, point):
        if point.equals(self.__startPoint):
            # flips start and end points
            self.setStartPoint(self.getEndPoint())
            self.setEndPoint(point)
            return True
        elif point.equals(self.__endPoint):
            return True
        else:
            return False
    
    # returns the euclidean distance between two endpoints using Euclid's fifth postulate (Pythagorean thm)
    def getLength(self):
        return math.sqrt(((self.__centerPoint.getX()-self.__endPoint.getX()))**2+(self.__centerPoint.getY()-self.__endPoint.getY())**2)
