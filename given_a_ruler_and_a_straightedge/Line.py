import numpy as np
import math
import copy 
import constants as c
import poincareDisk

import Point
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

    # plots the line in the given plot 
    def plotShape(self, plot,linewidth = c.THINLINE, poincare = False):
        if poincare == True:
            self.plotShapePoincare(plot, linewidth=linewidth)
            return
        if self.__endPoint != None:
            x_data = np.linspace(self.__startPoint.getX(), self.__endPoint.getX(), 100)
            y_data = np.linspace(self.__startPoint.getY(), self.__endPoint.getY(),100)
            self.__line, = plot.plot(x_data,y_data, color = "black", lw= linewidth)

            #plots endpoints
            self.__endPointPlot = self.__endPoint.plotShape(plot,linewidth)
            self.__startPointPlot = self.__startPoint.plotShape(plot,linewidth)

    def plotShapePoincare(self,plot,linewidth=c.THINLINE):
        if self.__endPoint != None:
            r,Xc,Yc = self.getEndPoint().findConnectingCircle(self.getStartPoint(), radius = 1)
            angle1 = np.atan2(self.getEndPoint().getY() - Yc, self.getEndPoint().getX() - Xc)
            angle2 = np.atan2(self.getStartPoint().getY() - Yc, self.getStartPoint().getX() - Xc) 
            
            # calculate ccw and cw sweep
            sweep1 = (angle2 - angle1) % (2 * np.pi)
            sweep2 = (angle1 - angle2) % (2 * np.pi)

            # select the smallest sweep
            if sweep1 < sweep2:
                start = angle1
                sweep = sweep1
            else:
                start = angle2
                sweep = sweep2

            # plot the arc
            angles = np.linspace(start,start+sweep,100)
            arc_x = Xc + (r * np.cos(angles))
            arc_y = Yc + (r * np.sin(angles))
            self.__line, = plot.plot(arc_x,arc_y, color = "black", lw= linewidth)

            #plots endpoints
            self.__endPointPlot = self.__endPoint.plotShape(plot,linewidth)
            self.__startPointPlot = self.__startPoint.plotShape(plot,linewidth)

    #plots the line on a scaled canvas
    def plotShapeScaledPlotsize(self,plot,oldPlotSize, newPlotSize):
        # calculates scalefactor
        scaleFactor = newPlotSize / oldPlotSize

        # ensures that the shape is not mutated
        figure = copy.deepcopy(self)

        startPoint = Point.Point(figure.getStartPoint().getX() *scaleFactor,figure.getStartPoint().getY() *scaleFactor)
        startPoint.setPointSize(Point.getDPS()*scaleFactor)
        endPoint = Point.Point(figure.getEndPoint().getX()*scaleFactor,self.getEndPoint().getY() *scaleFactor)
        endPoint.setPointSize(Point.getDPS()*scaleFactor)
        figure.setStartPoint(startPoint)
        figure.setEndPoint(endPoint)
        figure.plotShape(plot,c.THINLINE)

    def convertToPoincare(self):
        self.getEndPoint().convertToPoincare()
        self.getStartPoint().convertToPoincare()

    def convertToEuclidean(self):
        self.getEndPoint().convertToEuclidean()
        self.getStartPoint().convertToEuclidean()

    def scale(self,scaleVal,plot, poincare = False):
        if poincare == True:
            self.convertToEuclidean()

        dx,dy = self.getSlope(self.getStartPoint())
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
        newLength = oldLength * scaleVal

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

        newLeft = Point.Point(newLeftX,newLeftY)

        newRight = Point.Point(newRightX,newRightY)

        # ensures the points aren't flipping sides
        if newLeft.getX() >= newRight.getX():
            return
        
        self.removeShape()
        self.setStartPoint(newLeft)
        self.setEndPoint(newRight)

        if poincare == True:
            self.convertToPoincare()

        self.plotShape(plot,c.THICKLINE, poincare=poincare)
        self.setStartPoint(oldStart)
        self.setEndPoint(oldEnd)

        if poincare == True:
            self.convertToPoincare()

    def confirmScaleSize(self,scaleVal,plot, poincare = False):
        if poincare == True:
            self.convertToEuclidean()

        dx,dy = self.getSlope(self.getStartPoint())
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
        newLength = oldLength * scaleVal

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

        newLeft = Point.Point(newLeftX,newLeftY)

        newRight = Point.Point(newRightX,newRightY)

        # ensures the points aren't flipping sides
        if newLeft.getX() >= newRight.getX():
            return

        self.removeShape()
        # ensures start and end points are not altered in relative position
        if oldStart.getX() < oldEnd.getX():
            self.setStartPoint(newLeft)
            self.setEndPoint(newRight)
        else:
            self.setStartPoint(newRight)
            self.setEndPoint(newLeft)
            
        if poincare == True:
            self.convertToPoincare()

        self.plotShape(plot,c.THICKLINE, poincare=poincare)
            
    # removes the endpoints and lines associated with the plotted line
    def removeShape(self):
        if self.__line != None:
            # removes line and endPoint
            self.__line.remove()
            self.__startPointPlot.remove()
            self.__endPointPlot.remove()
            self.__line = None

        self.hideMetrics()

    # moves the entire line by a given amount
    def moveShape(self, deltaX,deltaY):
        newStart = Point.Point(self.getStartPoint().getX() + deltaX, self.getStartPoint().getY() + deltaY)
        newEnd = Point.Point(self.getEndPoint().getX() + deltaX, self.getEndPoint().getY() + deltaY)
        self.setEndPoint(newEnd)
        self.setStartPoint(newStart)

    # takes a euclidean x and y to move 
    def moveShapePoincare(self,deltaX=0,deltaY=0):
        self.getStartPoint().moveShapePoincare(deltaX,deltaY)
        self.getEndPoint().moveShapePoincare(deltaX,deltaY)

    def showMetrics(self,plot):
        textX = (self.getEndPoint().getX() + self.getStartPoint().getX())/ 2
        textY = (self.getEndPoint().getY() + self.getStartPoint().getY())/ 2
        lengthText = plot.text(textX, textY, round(self.getLength(),3), fontsize=10, color='red', rotation = self.getTerminalAngle(self.getStartPoint()), horizontalalignment = 'center',verticalalignment = 'top')

        # store the plots
        self.__measurementText.append(lengthText)

    def hideMetrics(self):
        for measurement in self.__measurementText:
            measurement.remove()

        self.__measurementText = []

    # moves the given point to a new location
    def movePoint(self,pointToMove, newPoint):
        if self.getEndPoint().exactEquals(pointToMove):
            self.setEndPoint(newPoint)
        elif self.getStartPoint().exactEquals(pointToMove):
            self.setStartPoint(newPoint)
        else:
            print("Error: given point is not in shape")

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
    def getSlope(self, reference):
        if (self.getEndPoint() == None or self.getStartPoint() == None):
            return 0
        if (self.getStartPoint().equals(reference)):
            firstPoint = self.getStartPoint()
            secondPoint = self.getEndPoint()
        elif (self.getEndPoint().equals(reference)):
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
    def getTerminalAngle(self,point):
        dx,dy = self.getSlope(point)
        angle = math.atan2(dy,dx)
        angle_deg = math.degrees(angle) % 360
        return angle_deg
    
    # returns details about the line
    def measure(self):
        dx,dy = self.getSlope(self.getStartPoint())
        if dx ==0:
            dx = 0.00000001
        returnString = "Length: {0}\nSlope: {1}".format(round(self.getLength(),3),round(dy/dx,3))
        return returnString
    
    def print(self):
        string = "Line: " + str(self)
        string += "\n\t Start Point: " + str(self.getStartPoint())
        string += "\n\t End Point: " + str(self.getEndPoint())
        print(string)

        
