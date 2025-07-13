import numpy as np
import math
import copy 

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

    __measurementText = []


    def __init__(self):
        pass

    # plots the line in the given plot and updates the canvas
    def plotShape(self, plot, canvas,linewidth):
        if self.__endPoint != None:
            x_data = np.linspace(self.__startPoint.getX(), self.__endPoint.getX(), 100)
            y_data = np.linspace(self.__startPoint.getY(), self.__endPoint.getY(),100)
            self.__line, = plot.plot(x_data,y_data, color = "black", lw= linewidth)

            #plots endpoints
            self.__endPointPlot = self.__endPoint.plotShape(plot,canvas,linewidth)
            self.__startPointPlot = self.__startPoint.plotShape(plot,canvas,linewidth)

            canvas.draw()

    #plots the line on a scaled canvas
    def plotShapeScaledPlotsize(self,plot,canvas,oldPlotSize, newPlotSize):
        # calculates scalefactor
        scaleFactor = newPlotSize / oldPlotSize

        # ensures that the shape is not mutated
        figure = copy.deepcopy(self)

        startPoint = Point(figure.getStartPoint().getX() *scaleFactor,figure.getStartPoint().getY() *scaleFactor)
        startPoint.setPointSize(Point.getDPS()*scaleFactor)
        endPoint = Point(figure.getEndPoint().getX()*scaleFactor,self.getEndPoint().getY() *scaleFactor)
        endPoint.setPointSize(Point.getDPS()*scaleFactor)
        figure.setStartPoint(startPoint)
        figure.setEndPoint(endPoint)
        figure.plotShape(plot,canvas,1)

    def scale(self,scaleVal,plot,canvas):
        scaler = scaleVal / 100
        dx,dy = self.getSlope()
        if (dx != 0):
            slope = dy/dx
        else:
            slope = np.inf
        oldStart = self.getStartPoint()
        oldEnd = self.getEndPoint()

        # determines which point is on the left
        if (oldStart.getX() < oldEnd.getX()):
            leftPoint = oldStart
            rightPoint = oldEnd
        else:
            leftPoint = oldEnd
            rightPoint = oldStart

        # determines the new length
        oldLength = self.getLength()
        newLength = oldLength * scaler

        # determines how much to add to either side of the line
        halfLength = (newLength - oldLength)/2

        if slope < 0:
            halfLength *= -1

        # finds the angle
        angle = math.atan(dx/dy)     
        deltaX = halfLength * math.sin(angle)

        newLeftX = leftPoint.getX() - deltaX
        newLeftY = leftPoint.getY() + (slope * (newLeftX-leftPoint.getX()))

        newRightX = rightPoint.getX() + deltaX
        newRightY = rightPoint.getY() + (slope * (newRightX-rightPoint.getX()))

        newLeft = Point(newLeftX,newLeftY)

        newRight = Point(newRightX,newRightY)

        # ensures the points aren't flipping sides
        if newLeft.getX() >= newRight.getX():
            return

        self.removeShape(canvas)
        self.setStartPoint(newLeft)
        self.setEndPoint(newRight)
        self.plotShape(plot,canvas,1)
        self.setStartPoint(oldStart)
        self.setEndPoint(oldEnd)


    def confirmScaleSize(self,scaleVal,plot,canvas):
        scaler = scaleVal / 100
        dx,dy = self.getSlope()
        if (dx != 0):
            slope = dy/dx
        else:
            slope = np.inf
        oldStart = self.getStartPoint()
        oldEnd = self.getEndPoint()

        # determines which point is on the left
        if (oldStart.getX() < oldEnd.getX()):
            leftPoint = oldStart
            rightPoint = oldEnd
        else:
            leftPoint = oldEnd
            rightPoint = oldStart

        # determines the new length
        oldLength = self.getLength()
        newLength = oldLength * scaler

        # determines how much to add to either side of the line
        halfLength = (newLength - oldLength)/2

        if slope < 0:
            halfLength *= -1

        # finds the angle
        angle = math.atan(dx/dy)     
        deltaX = halfLength * math.sin(angle)

        newLeftX = leftPoint.getX() - deltaX
        newLeftY = leftPoint.getY() + (slope * (newLeftX-leftPoint.getX()))

        newRightX = rightPoint.getX() + deltaX
        newRightY = rightPoint.getY() + (slope * (newRightX-rightPoint.getX()))

        newLeft = Point(newLeftX,newLeftY)

        newRight = Point(newRightX,newRightY)

        # ensures the points aren't flipping sides
        if newLeft.getX() >= newRight.getX():
            return

        self.removeShape(canvas)
        # ensures start and end points are not altered in relative position
        if oldStart.getX() < oldEnd.getX():
            self.setStartPoint(newLeft)
            self.setEndPoint(newRight)
        else:
            self.setStartPoint(newRight)
            self.setEndPoint(newLeft)
            
        self.plotShape(plot,canvas,1)
            
    # removes the endpoints and lines associated with the plotted line
    def removeShape(self,canvas):
        if self.__line != None:
            # removes line and endPoint
            self.__line.remove()
            self.__startPointPlot.remove()
            self.__endPointPlot.remove()
            self.__line = None

        self.hideMetrics(canvas)

        canvas.draw()

    # moves the entire line by a given amount
    def moveShape(self, deltaX,deltaY):
        newStart = Point(self.getStartPoint().getX() + deltaX, self.getStartPoint().getY() + deltaY)
        newEnd = Point(self.getEndPoint().getX() + deltaX, self.getEndPoint().getY() + deltaY)
        self.setEndPoint(newEnd)
        self.setStartPoint(newStart)

    def showMetrics(self,plot,canvas):
        textX = (self.getEndPoint().getX() + self.getStartPoint().getX())/ 2
        textY = (self.getEndPoint().getY() + self.getStartPoint().getY())/ 2
        lengthText = plot.text(textX, textY, round(self.getLength(),3), fontsize=10, color='red', rotation = self.getTerminalAngle(), horizontalalignment = 'center',verticalalignment = 'top')

        # store the plots
        self.__measurementText.append(lengthText)
        canvas.draw()

    def hideMetrics(self, canvas):
        for measurement in self.__measurementText:
            measurement.remove()

        self.__measurementText = []
        canvas.draw()

    # moves the given point to a new location
    def movePoint(self,point, newPoint):
        if self.getEndPoint() == point:
            self.setEndPoint(newPoint)
        else:
            self.setStartPoint(newPoint)

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
    
    def isClosedFigure(self):
        return False
    
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
        
    # checks if the exact given point is contained in the figure
    def exactContainsPoint(self,point):
        if (self.getStartPoint().getX() == point.getX() and self.getStartPoint().getY() == point.getY()):
            return True
        elif (self.getEndPoint().getX() == point.getX() and self.getEndPoint().getY() == point.getY()):
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
            
    # returns the components of the slope of the line
    def getSlope(self, origin = Point(0,0)):
        if (self.getEndPoint() == None or self.getStartPoint() == None):
            return 0
        if (self.getStartPoint().equals(origin)):
            firstPoint = self.getStartPoint()
            secondPoint = self.getEndPoint()
        elif (self.getEndPoint().equals(origin)):
            firstPoint = self.getEndPoint()
            secondPoint = self.getStartPoint()
        # ensures the slope is calculated correctly by having the first point as the point with the smallest x value
        elif (self.getStartPoint().getX() < self.getEndPoint().getX()):
            firstPoint = self.getStartPoint()
            secondPoint = self.getEndPoint()
        else: 
            firstPoint = self.getEndPoint()
            secondPoint = self.getStartPoint()

        dx = (secondPoint.getX() - firstPoint.getX())
        dy = (secondPoint.getY() - firstPoint.getY())
        return dx,dy
    
    # returns the angle betweeen the line the terminal angle
    def getTerminalAngle(self, reference = Point(0,0)):
        dx,dy = self.getSlope(reference)
        angle = math.atan2(dy,dx)
        angle_deg = math.degrees(angle) % 360
        return angle_deg
    
    # returns details about the line
    def measure(self):
        dx,dy = self.getSlope()
        if dx ==0:
            dx = 0.00000001
        returnString = "Length: {0}\nSlope: {1}".format(round(self.getLength(),3),round(dy/dx,3))
        return returnString
    
    def print(self):
        string = "Line: " + str(self)
        string += "\n\t Start Point: " + str(self.getStartPoint())
        string += "\n\t End Point: " + str(self.getEndPoint())
        print(string)

        
