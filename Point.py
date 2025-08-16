import math
import constants as c
import poincareDisk
import copy 

""""
Class to define a point in a graph
Points are defined by an x and y value
"""

class Point:
    """A class used to represent a Point object defined by an x and y value

    Attributes
    ----------
    __x : float
        x value of the Point
    __y : float
        y value of the Point
    __plot : obj
        the plotted object
    __pointSize : int
        the size the point will appear on the plot

    Methods
    -------
    setX(x)
        sets the X value of the Point

    setY(y)
        sets the Y value of the Point

    setPoincare(poincare)
        sets the boolean value of if the point is in poincare mode

    getPoincare()
        gets the boolean value of if the point is in poincare mode

    setPointSize(newPointSize)
        sets the size the point will appear when plotted

    equals(otherPoint)
        returns a boolean determining if a point is equivalent in x and y values to within the epsilon value

    exactEquals(otherPoint)
        returns a boolean determining if a point is exactly equivalent in x and y values

    getDistance(otherPoint)
        returns the distance between the Point object and another point object USING EUCLIDEAN METRIC FORMULAS

    plotShape(plot, linewidth = c.THINLINE)
        plots the Point on the given plot

    moveShape(deltaX,deltaY)
        shifts the Point's X and Y values by given delta values

    removeShape()
        removes the Point's plot 

    movePoint(point, newPoint)
        moves the Point to a new location specified by another given point

    getX()
        returns the current X value of the Point
        
    getY()
        returns the current Y value of the Point

    measure()
        returns a well-formatted string of measurement information including X and Y coordinates

    print()
        prints a string of information about the Point including the Point address and X/Y coordinates
    """

    __pointSize = c.DEFAULTPOINTSIZE
    epsilon = c.EPSILON
    __poincare = False

    def __init__(self, x = 0, y=0, poincare = False):
        """
        Parameters
        ----------
        x : float
            The X value of the Point
        y : float
            The Y value of the Point
        poincare : boolean
            True if the points are in poincare mode
        """
        self.__x = x
        self.__y = y
        self.__poincare = poincare

    def setEpsilon(newEpsilon):
        """ Sets the epsilon (acceptable error) value of the Point class
        Parameters
        ----------
        newEpsilon : float
            The new epsilon (acceptable error) value of the Point class.
        """

        Point.epsilon = newEpsilon

    def setX(self, x):
        """ Sets the Point's X value to the new value

        Parameters
        ----------
        x : float
            the new x coordinate of the Point
        """
        self.__x = x

    def setY(self, y):
        """ Sets the Point's Y value to the new value

        Parameters
        ----------
        y : float
            the new y coordinate of the Point
        """
        self.__y = y

    def setPoincare(self, poincare):
        """ sets the boolean value of if the point is in poincare mode

        Parameters
        ----------
        poincare : boolean
            true if the point is in poincare mode, false otherwise
        """
        self.__poincare = poincare

    def getPoincare(self):
        """ gets the boolean value of if the point is in poincare mode
        """
        return self.__poincare
        
    def setPointSize(self,newPointSize):
        """ Sets the Point's size for it to appear as when plotted

        Parameters
        ----------
        x : float
            the new point size
        """
        self.__pointSize = newPointSize

    def getPointSize(self):
        """ provides the Point's size to appear when plotted

        Returns
        ----------
        float
            the Point's size value
        """
        return self.__pointSize
    
    def equals(self, otherPoint,epsilon = epsilon):
        """ Checks if the Point is equal to another point in X and Y value to within some epsilon value 

        Parameters
        ----------
        otherPoint : Point
            the point to compare the Point object to
        epsilon: float
            the epsilon value that is allowable, defaults to the class value of epsilon

        Returns
        ---------
        boolean
            True when the points are equal to within a certain epsilon value, False otherwise
        """
        if (otherPoint == None):
            return False
        elif (abs(self.__x - otherPoint.getX()) <= Point.epsilon and abs(self.__y - otherPoint.getY()) <= Point.epsilon):
            return True
        else:
            return False
    
    def convertToPoincare(self):
        """ Maps the Euclidean Point value to a position in the Poincare disk. Sets the X and Y values to match
        """
        if self.__poincare == False:
            newX,newY = poincareDisk.euclideanToPoincareFunc(self.getX(), self.getY())
            self.setX(newX)
            self.setY(newY)
            self.__poincare = True

    def convertToEuclidean(self):
        """ Maps the Poincare Disc Point value to a position in the Euclidean plane. Sets the X and Y values to match
        """
        if self.__poincare == True:
            newX,newY = poincareDisk.poincareToEuclideanFunc(self.getX(), self.getY())
            self.setX(newX)
            self.setY(newY)
            self.__poincare = False

    def exactEquals(self,otherPoint):
        """ Checks if the Point is exactly equal to another point in X and Y value
        Parameters
        ----------
        otherPoint : Point
            the point to compare the Point object to

        Returns
        ---------
        boolean
            True when the points are equal, False otherwise
        """
        if otherPoint == None:
            return False
        if (self.getX() == otherPoint.getX() and self.getY() == otherPoint.getY()):
            return True
        return False

    def containsPoint(self, point):
        """ Checks if the Point contains a given point (checks if they are equal)

        Parameters
        ----------
        point : Point
            the point to compare the Point object to

        Returns
        ---------
        boolean
            True when the points are equal to within a certain epsilon, False otherwise
        """
        if point.equals(self):
            return True
        return False

    def getPoint(self,point):
        """ If the Point contains another given point, provides the exact value of the Point object
        
        Parameters
        ----------
        otherPoint : Point
            the point to compare the Point object to

        Returns
        ---------
        self if the Point object contains the given point
        """
        if self.equals(point):
            return self
    
    def getEndPoint(self):
        return self
    
    def setEndPoint(self, point):
        """ Sets the Point's x and y values to match the given point

        Parameters
        ----------
        point: Point
            the point to get X and Y values from
        """
        self.setX(point.getX())
        self.setY(point.getY())

    def getDistance(self, otherPoint):
        """ Finds the EUCLIDEAN distance between the Point object and another point
        Parameters
        ----------
        otherPoint : Point
            the point to compare the Point object to

        Returns
        ---------
        float
            the calculated Euclidean distance between points
        """
        return math.sqrt(((self.getX()-otherPoint.getX()))**2+(self.getY()-otherPoint.getY())**2)

    def plotShape(self, plot, linewidth = c.THINLINE, poincare = False):
        """ Plots the point in the Euclidean Plane if poincare is False

        Parameters
        ----------
        plot : obj
            the plot to place the Point object in
        linewidth : int, optional
            the width of a plotted line: DOES NOT APPLY HERE
        poincare: boolean
            whether or not the point is in poincare mode - used to check that the point is plotted correctly

        Returns
        ---------
        obj
            An object containing the plot (stored to remove the Point from the plot)
        """
        
        pointsize = self.getPointSize()
        if linewidth == c.THICKLINE:
            self.setPointSize(c.BOLDPOINTSIZE)

        if poincare == False:
            self.__plot = plot.scatter(self.__x,self.__y, color="blue", s=self.__pointSize)
            self.setPointSize(pointsize)
            return self.__plot
        else:
            self.plotShapePoincare(plot,linewidth)

    def plotShapeScaledPlotsize(self,plot,oldPlotSize, newPlotSize):
        # calculates scalefactor
        scaleFactor = newPlotSize / oldPlotSize

        # ensures that the shape is not mutated
        figure = copy.deepcopy(self)

        figure.setPointSize(c.DEFAULTPOINTSIZE*scaleFactor)
        figure.plotShape(plot,c.THINLINE)

    def plotShapePoincare(self,plot,linewidth=c.THINLINE):
        """ Plots the point in the Poincare Disc (same procedure as plotting regularly

        Parameters
        ----------
        plot : obj
            the plot to place the Point object in
        linewidth : int, optional
            the width of a plotted line: DOES NOT APPLY HERE

        Returns
        ---------
        obj
            An object containing the plot (stored to remove the Point from the plot)
        """

        self.__plot = plot.scatter(self.__x,self.__y, color="blue", s=self.__pointSize)
        return self.__plot

    def removeShape(self):
        """ removes the plotted point from the canvas 
        """

        if (self.__plot != None):
            self.__plot.remove()
            self.__plot = None

    def movePoint(self,pointToMove, newPoint):
        """ moves the Point to a new location where the X and Y value are specified by a given point 

        Parameters
        ----------
        pointToMove : Point
            the current point that must be moved: DOES NOT APPLY HERE (used by other shape objects)
        newPoint : Point
            the point specifing the new X and Y location of the Point

        Returns
        ----------
        boolean
            True when the point can move and remain in bounds, False otherwise
        """

        # ensures the point remains in poincare boundary
        if self.__poincare == True:
            if newPoint.getX()**2 + newPoint.getY()**2 < 1 :
                self.setX(newPoint.getX())
                self.setY(newPoint.getY())
                return True
            
            return False
        else:
            self.setX(newPoint.getX())
            self.setY(newPoint.getY())
            return True



    def moveShape(self,deltaX,deltaY):
        """ moves the Point to a new location where the X and Y value are altered by given amounts

        Parameters
        ----------
        deltaX : float
            the value to be added to the Point's current X value
        deltaY : float
            the value to be added to the Point's current Y value
        """
        self.setX(self.getX() + deltaX)
        self.setY(self.getY() + deltaY)

    def moveShapePoincare(self, primaryPoint, newPrimaryPoint):
        """ moves Point to a new location. 

        Parameters
        ----------
        primaryPoint : Point
            the point to move (self)
        newPrimaryPoint: Point
            new location for point to move t0
        """
        if primaryPoint.exactEquals(self):
            self.movePoint(pointToMove=primaryPoint,newPoint=newPrimaryPoint)

    def getX(self):
        """ provides the Point's current X value

        Returns
        ----------
        float
            the Point's X value
        """
        return self.__x
    
    def getY(self):
        """ provides the Point's current Y value

        Returns
        ----------
        float
            the Point's Y value
        """
        return self.__y
    
    def measure(self):
        """ provides a well-formatted string containing information about the Point's X and Y locations

        Returns
        ----------
        string
            a string containing the Point's X and Y values
        """
        return "{0}, {1}".format(round(self.getX(),3),round(self.getY(),3))
    
    def print(self):
        """ prints a well-formatted string containing information about the Point

        Returns
        ----------
        string
            a string containing the Point's X and Y values and its object name
        """
        string = "Point: " + str(self)
        string += "\n\tX: " + str(self.getX()) + "\tY: " + str(self.getY())
        print(string)

    def hideMetrics(self):
        """ hides the metrics associated with the Point object. Note: there cannot be metrics associated with a point object
        """
        pass
