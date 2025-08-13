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
    """A class used to represent a Line object defined a start Point and end Point

    Attributes
    ----------
    __startPoint : Point
        the starting point of the line
    __endPoint : Point
        the ending point of the line - if the line is being adjusted, this point will move.
    __startPointPlot : obj
        the plotted startPoint object in the graph
    __endPointPlot : obj
        the plotted endPoint object in the graph
    __line: obj
        the plotted line object in the graph
    __measurementText: obj 
        the plotted measurement descriptor for the line in the graph
    __poincare: boolean
        boolean determining whether the line is in poincare mode or not

    Methods
    -------
    plotShape(plot,linewidth = c.THINLINE, poincare = False)
        Plots the endpoints and line in the given plot

    plotShapePoincare(plot,linewidth=c.THINLINE)
        Plots the endpoints and line in the given plot. Draws a hyperbolic line between two endpoints

    plotShapeScaledPlotsize(plot,oldPlotSize, newPlotSize)
        Plots the endpoints and Euclidean line in the given plot, adjusting the pointsize based on the old/new plot sizes

    convertToPoincare()
        Converts the start and end points of the line to their poincare mapping, sets poincare boolean to True

    convertToEuclidean()
        Converts the start and end points of the line to their Euclidean mapping, sets poincare boolean to False

    scale(scaleVal,plot, poincare = False)
        Scales the entire shape by the scaleVal AND plots the new scaled value AND converts the points back to their original values after plotting

    confirmScaleSize(scaleVal,plot, poincare = False)
        Scales the entire shape by the scaleVal AND plots the new scaled value

    removeShape()
        removes the endpoint, startpoint, and line plots from the canvas. Also hides the metrics of the line

    moveShape(deltaX,deltaY)
        moves both start and end points by the given delta amounts

    moveShapePoincare(primaryPoint,newPrimaryPoint)
        moves line to a new location. The primary point is moved to a new location, the other endpoint the same distance

    showMetrics(plot)
        creates, places, and plots text in the center of the line displaying the length of the line

    hideMetrics()
        removes any measurement displays

    movePoint(pointToMove, newPoint)
        Sets a given point to a new point

    setStartPoint(startPoint)
        Sets the start point of the line to a new point 

    setEndPoint(endpoint)
        Sets the end point of the line to a new point

    getStartPoint()
        Returns the Line's start point

    setEndPoint(endpoint)
        Returns the Line's end point

    getShape()
        Returns the line plot of the object

    getPoincare()
        Returns the Line's poincare value

    containsPoint(point)
        Determines if the line contains the given point (the given point can be off by an epsilon value associated with the Point class)

    exactContainsPoint(point)
        Determines if the line contains the given EXACT point (no epsilon allowance)

    getPoint(point)
        Finds the exact Point that is found with .containsPoint(point)

    getLength()
        Finds the Euclidean distance between the start and end points using the Pythagorean thm

    getSlope(reference)
        Finds the Euclidean slope of the line

    getTerminalAngle(point)
        Finds the angle (in degrees) between the line and a horizontal line

    measure()
        Returns a string of details about the line including its length and slope

    print()
        Prints information about the line including the line's memory address in addition to details about the start and end point
    """

    # stores the start and endpoints
    __startPoint = None
    __endPoint = None

    # stores the plots of the points and line and measurement label
    __endPointPlot = None
    __startPointPlot = None
    __line = None
    __measurementText = None 

    # boolean determining whether the line is in poincare mode or not
    __poincare = False

    def __init__(self, poincare = False):
        """
        Parameters
        ----------
        poincare : boolean
            True if the points are in poincare mode
        """
        self.__poincare = poincare

    def plotShape(self, plot,linewidth = c.THINLINE, poincare = False):
        """ Plots the endpoints and line in the given plot
        When poincare is false, draws a euclidean line between the two endpoints

        Parameters
        ----------
        plot : obj
            the plot to draw the shape in 
        linewidth: int, optional
            width of the line connecting the two points
        poincare: boolean, optional
            whether or not the Line is in poincare mode - used to ensure correct type of plotting 
        """

        # checks if the shape must be drawn in poincare style
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
        """ Plots the endpoints and line in the given plot. Draws a hyperbolic line between two endpoints

        Parameters
        ----------
        plot : obj
            the plot to draw the shape in 
        linewidth: int, optional
            width of the line connecting the two points
        """

        if self.__endPoint != None:
            x0 = self.getEndPoint().getX()
            x1 = self.getStartPoint().getX()
            y0 = self.getEndPoint().getY()
            y1 = self.getStartPoint().getY()
            r,Xc,Yc = poincareDisk.findConnectingCircle(x0,y0,x1,y1)
            if r == np.inf:
                # if the radius is infinite, plot a straight line
                x_data = np.linspace(x0,x1,100)
                y_data = np.linspace(y0,y1,100)
                self.__line, = plot.plot(x_data,y_data,color = "black", lw= linewidth)
            else:
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
        """ Plots the endpoints and Euclidean line in the given plot, adjusting the pointsize based on the old/new plot sizes 

        Parameters
        ----------
        plot : obj
            the plot to draw the shape in 
        oldPlotSize: int
            size of the old plot
        newPltSize: int
            size of the new plot
        """

        # calculates scalefactor
        scaleFactor = newPlotSize / oldPlotSize

        # ensures that the shape is not mutated
        figure = copy.deepcopy(self)

        figure.getStartPoint().setPointSize(c.DEFAULTPOINTSIZE*scaleFactor)
        figure.getEndPoint().setPointSize(c.DEFAULTPOINTSIZE*scaleFactor)
        figure.plotShape(plot,c.THINLINE)

    def convertToPoincare(self):
        """ Converts the start and end points of the line to their poincare mapping, sets poincare boolean to True
        """
        if self.__poincare == False:
            self.getEndPoint().convertToPoincare()
            self.getStartPoint().convertToPoincare()
            self.__poincare = True

    def convertToEuclidean(self):
        """ Converts the start and end points of the line to their Euclidean mapping, sets poincare boolean to False
        """

        if self.__poincare == True:
            self.getEndPoint().convertToEuclidean()
            self.getStartPoint().convertToEuclidean()
            self.__poincare = False

    def scale(self,scaleVal,plot, poincare = False):
        """ Scales the entire shape by the scaleVal AND plots the new scaled shape AND converts the points back to their original values after plotting.
        The scaled change is NOT permanent (original point values are restored). This is done to ensure that when dragging the slider, the shape is being 
        scaled based on its original length, not the already scaled length. 

        Parameters
        ----------
        scaleVal : float
            The value by which to scale the length of the shape
        plot: obj
            the plot for the shape to appear in
        poincare: boolean, optional
            whether or not the object is in poincare mode
        """

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
        """ Scales the entire shape by the scaleVal AND plots the new scaled value.
        The scaled change IS permanent. To be called when a scaling is complete (the user is no longer adjusting the scale size).

        Parameters
        ----------
        scaleVal : float
            The value by which to scale the length of the shape
        plot: obj
            the plot for the shape to appear in
        poincare: boolean, optional
            whether or not the object is in poincare mode
        """
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
            
    def removeShape(self):
        """ removes the endpoint, startpoint, and line plots from the canvas. Also hides the metrics of the line.
        """
        if self.__line != None:
            # removes line and endPoint
            self.__line.remove()
            self.__startPointPlot.remove()
            self.__endPointPlot.remove()
            self.__line = None

        self.hideMetrics()

    def moveShape(self, deltaX,deltaY):
        """ moves both start and end points by the given delta amounts. 

        Parameters
        ----------
        deltaX : float
            the Euclidean horizontal distance for the shape to move
        deltaY: float
            the Euclidean vertical distance for the shape to move
        """
        newStart = Point.Point(self.getStartPoint().getX() + deltaX, self.getStartPoint().getY() + deltaY)
        newEnd = Point.Point(self.getEndPoint().getX() + deltaX, self.getEndPoint().getY() + deltaY)
        self.setEndPoint(newEnd)
        self.setStartPoint(newStart)


    def showMetrics(self,plot):
        """ creates, places, and plots text in the center of the line displaying the length of the line
        """
        textX = (self.getEndPoint().getX() + self.getStartPoint().getX())/ 2
        textY = (self.getEndPoint().getY() + self.getStartPoint().getY())/ 2
        angle = self.getTerminalAngle(self.getStartPoint())
        # ensures angles are right way up
        while angle > 90 and angle < 270:
            angle -= 180
        lengthText = plot.text(textX, textY, round(self.getLength(),3), fontsize=10, color='red', rotation = angle, horizontalalignment = 'center',verticalalignment = 'top')

        # store the plots
        self.__measurementText = lengthText

    def hideMetrics(self):
        """ removes any measurement displays
        """
        if self.__measurementText != None:
            self.__measurementText.remove()

        self.__measurementText = None

    def movePoint(self,pointToMove, newPoint):
        """ Sets a given point within the shape to a new point

        Parameters
        ----------
        pointToMove : Point
            the point within the shape to move
        newPoint : Point
            the point to set as the new point, replacing pointToMove

        Returns
        ----------
        boolean
            True when pointToMove can be moved and stays within the boundaries, False otherwise
        """
        if self.getEndPoint().exactEquals(pointToMove):
            bool = self.getEndPoint().movePoint(pointToMove,newPoint)
        elif self.getStartPoint().exactEquals(pointToMove):
            bool = self.getStartPoint().movePoint(pointToMove,newPoint)
        else:
            print("Error: given point is not in shape")
            bool = False
        return bool

    def moveShapePoincare(self, primaryPoint, newPrimaryPoint):
        """ moves line to a new location. Calculates Euclidean distance to move, performs transformations in Euclidean mode, then converts to Poincare

        Parameters
        ----------
        primaryPoint : Point
            the point to move 
        newPrimaryPoint: Point
            new location for center point to move
        """

        # finds the EUCLIDEAN distance the point was moved
        primaryPoint.convertToEuclidean()
        newPrimaryPoint.convertToEuclidean()
        deltaX = newPrimaryPoint.getX() - primaryPoint.getX()
        deltaY = newPrimaryPoint.getY() - primaryPoint.getY()
        primaryPoint.convertToPoincare()
        newPrimaryPoint.convertToPoincare()

        # moves points
        self.getEndPoint().convertToEuclidean()
        self.getStartPoint().convertToEuclidean()
        self.getEndPoint().moveShape(deltaX,deltaY)
        self.getStartPoint().moveShape(deltaX,deltaY)
        self.getEndPoint().convertToPoincare()
        self.getStartPoint().convertToPoincare()


    def setStartPoint(self, startPoint):
        """ Sets the start point of the line to a new point

        Parameters
        ----------
        startPoint : Point
            the new start point
        """
        if self.__poincare == True:
            startPoint.setPoincare(True)


        self.__startPoint = startPoint

    def setEndPoint(self, endPoint):
        """ Sets the end point of the line to a new point

        Parameters
        ----------
        endPoint : Point
            the new end point
        """
        if self.__poincare == True:
            endPoint.setPoincare(True)

        self.__endPoint = endPoint
    
    def getStartPoint(self):
        """ Returns the Line's start point
        
        Returns
        ----------
        Point
            the start point of the line

        """
        return self.__startPoint
    
    
    def getEndPoint(self):
        """ Returns the Line's end point
        
        Returns
        ----------
        Point
            the end point of the line
        """

        return self.__endPoint
    
    def getShape(self):
        """ Returns the line plot of the object

        Returns
        ----------
        obj
            the line plot 
        """
        return self.__line
            
    def getPoincare(self):
        """ Returns the Line's poincare value

        Returns
        ----------
        boolean
            whether or not the line is in poincare mode 
        """
        return self.__poincare
    
    def containsPoint(self, point):
        """ Determines if the line contains the given point (the given point can be off by an epsilon value associated with the Point class)
        If the line DOES contain the point, the point is forced to be the endpoint (line itself doesn't change)

        Parameters 
        ----------
        point : Point
            the point to check if the Line contains

        Returns
        ----------
        boolean
            whether or not the given point is found within the line
        """
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
        
    def exactContainsPoint(self,point):
        """ Determines if the line contains the given EXACT point (no epsilon allowance)
        start/endpoints do NOT change

        Parameters 
        ----------
        point : Point
            the point to check if the Line contains

        Returns
        ----------
        boolean
            whether or not the given point is found within the line
        """
        if (self.getStartPoint().getX() == point.getX() and self.getStartPoint().getY() == point.getY()):
            return True
        elif (self.getEndPoint().getX() == point.getX() and self.getEndPoint().getY() == point.getY()):
            return True
        else:
            return False
        
    def getPoint(self,point):
        """ Finds the exact Point that is found with self.containsPoint(point)

        essentially removes the epsilon value associated with a contained point for smoother joining of shapes

        Parameters 
        ----------
        point : Point
            the point used to find the exact Line point

        Returns
        ----------
        Point
            the point contained in the Line that is within an epsilon value of the given point
        """
        if (self.containsPoint(point)):
            return self.getEndPoint()

    def getLength(self):
        """ Finds the Euclidean distance between the start and end points using the Pythagorean thm. DOES NOT CONVERT POINTS FOR CALCULATION

        Returns
        ----------
        float
            the Euclidean distance between the start and end points
        """

        return math.sqrt(((self.getStartPoint().getX()-self.getEndPoint().getX()))**2+(self.getStartPoint().getY()-self.getEndPoint().getY())**2)
            
    def getSlope(self, reference):
        """ Finds the Euclidean slope of the line

        Parameters
        ----------
        reference: Point
            the point of reference for which to find the slope (helps determine positive or negative)
            usually the line's start point

        Returns
        ----------
        tuple
            dx : float 
                the x component of the slope of the line
            dy : float
                the y component of the slope of the line
        """

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
    
    def getTerminalAngle(self,point):
        """ Finds the angle (in degrees) between the line and a horizontal line 

        Returns
        ----------
        float
            the angle in degrees
        """
        dx,dy = self.getSlope(point)
        angle = math.atan2(dy,dx)
        angle_deg = math.degrees(angle) % 360
        return angle_deg
    
    def measure(self):
        """ Returns a string of details about the line including its length and slope

        Returns
        ----------
        String
            a string containing details about the line
        """
        dx,dy = self.getSlope(self.getStartPoint())
        if dx ==0:
            dx = 0.00000001
        returnString = "Length: {0}\nSlope: {1}".format(round(self.getLength(),3),round(dy/dx,3))
        return returnString
    
    def print(self):
        """ Prints information about the line including the line's memory address in addition to details about the start and end point 
        """

        string = "Line: " + str(self)
        string += "\n\t Start Point: " + str(self.getStartPoint())
        string += "\n\t End Point: " + str(self.getEndPoint())
        print(string)

        
