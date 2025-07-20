import math
import constants as c
import poincareDisk
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

    def __init__(self, x = 0, y=0):
        """
        Parameters
        ----------
        x : float
            The X value of the Point
        y : float
            The Y value of the Point
        """
        self.__x = x
        self.__y = y

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
        
    def setPointSize(self,newPointSize):
        """ Sets the Point's size for it to appear as when plotted

        Parameters
        ----------
        x : float
            the new point size
        """
        self.__pointSize = newPointSize
    
    def equals(self, otherPoint):
        """ Checks if the Point is equal to another point in X and Y value to within some epsilon value 

        Parameters
        ----------
        otherPoint : Point
            the point to compare the Point object to

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
        newX,newY = poincareDisk.euclideanToPoincareFunc(self.getX(), self.getY())
        self.setX(newX)
        self.setY(newY)

    def convertToEuclidean(self):
        newX,newY = poincareDisk.poincareToEuclideanFunc(self.getX(), self.getY())
        self.setX(newX)
        self.setY(newY)

    # given the two endpoints and radius of the disc, returns the radius and center points of the Euclidean circle connecting them
    def findConnectingCircle(self, otherPoint, radius):
        x0 = self.getX()
        y0 = self.getY()
        x1 = otherPoint.getX()
        y1 = otherPoint.getY()
        numX = y0 * (x1**2 + y1**2 + radius**2)-y1 * (x0**2 + y0**2 + radius**2)
        numY = x1 * (x0**2 + y0**2 + radius**2)-x0 * (x1**2 + y1**2 + radius**2)
        denom = 2 * ( (x1 * y0) - (x0 * y1))
        centerX = numX/denom
        centerY = numY/denom
        r = math.sqrt(centerX**2 + centerY ** 2 - radius**2)
        return r,centerX,centerY

    # checks if the x and y values of a point match
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
        if self.equals(point):
            return True
        return False

    def getPoint(self,point):
        if self.containsPoint(point):
            return self
    
    def setEndPoint(self, point):
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
        """ Plots the point 

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
        """
        self.setX(newPoint.getX())
        self.setY(newPoint.getY())

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
