import math
import matplotlib.patches as patches
import copy
import constants as c
import numpy as np
import Point

""""
class to create Euclidean Circle objects

Cirles are defined by a center point and radius
"""

class Circle:

    """A class used to represent a Line object defined a start Point and end Point

    Attributes
    ----------
    __circle = None
    __centerPoint = None
    __radius = None

    __centerPointPlot = None
    __radiusSet = False
    
    __poincare = False # boolean flag for if points are poincare versions

    __centerPoint : Point
        the center point of the circle
    __radius : float
        the radius of the circle 
    __centerPointPlot : obj
        the plotted center point object in the graph
    __circle: obj
        the plotted circle object in the graph
    __radiusSet: boolean 
        boolean determing whether the circle's radius has been permanently set
    __poincare: boolean
        boolean determining whether the line is in poincare mode or not

    Methods
    -------
    plotShape(plot, linewidth = c.THINLINE, poincare = False)
        Plots the center point and circle in the given plot

    plotShapePoincare(plot,linewidth=c.THINLINE)
        Plots the center point and Hyperbolic circle in the given plot

    convertToPoincare()
        Converts the center point of the circle to its poincare mapping, sets poincare boolean to True

    convertToEuclidean()
        Converts the center point of the circle to its Euclidean mapping, sets poincare boolean to False

    plotShapeScaledPlotsize(plot,oldPlotSize, newPlotSize)
        Plots the center point and Euclidean circle in the given plot, adjusting the pointsize based on the old/new plot sizes

    scale(scaleVal,plot,poincare = False)
        Scales the entire shape by the scaleVal AND plots the new scaled shape AND sets radius back to its original radius after plotting

    confirmScaleSize(scaleVal,plot, poincare = False)
        Scales the entire shape by the scaleVal AND plots the new scaled shape

    removeShape()
        removes the centerpoint and circle plots from the canvas

    moveShape(deltaX, deltaY)
        moves centerpoint by the given delta amounts

    moveShapePoincare(primaryPoint,newPrimaryPoint)
        moves center point to a new location

    movePoint(pointToMove, newPoint)
        Sets a given point within the shape to a new point

    setStartPoint(centerPoint)
        Sets the 'start point' / center point of the line to a new point

    setCenterPoint(centerPoint)
        Sets the center point of the line to a new point

    setEndPoint(endPoint)
        If the radius is already set, sets the center point as the new point

    setRadius(radius)
        Sets the radius of the circle

    getCenterPoint()
        Returns the Circle's center point

    getStartPoint()
        Returns the Circle's 'start'/center point

    getEndPoint()
        Returns the Circle's 'end'/center point

    getRadius()
        Returns the Circle's radius value

    getShape()
        Returns the circle plot of the object

    getPoincare()
        Returns the Circle's poincare value

    containsPoint(point)
        Determines if the circle contains the given point (the given point can be off by an epsilon value associated with the Point class)

    exactContainsPoint(point)
        Determines if the circle contains the given EXACT point (no epsilon allowance)

    getPoint(point)
        Finds the exact Point that is found with self.containsPoint(point)

    getLength()
        Finds the Euclidean distance around the circle (circumference)

    getCircumference()
        Finds the Euclidean distance around the circle

    getArea()
        Finds the Euclidean area of the circle 

    measure()
        Returns a string of details about the circle including its radius, circumference, and area

    print()
        Prints information about the line including the line's memory address in addition to details about the start and end point
    """

    __centerPoint = None
    __radius = None

    # plot objects for the center point and circle 
    __circle = None
    __centerPointPlot = None

    __radiusSet = False # boolean flag for if the circle radius has been set permanently
    __poincare = False # boolean flag for if points are poincare versions

    def __init__(self, poincare = False):
        """
        Parameters
        ----------
        poincare : boolean
            True if the object is in poincare mode
        """

        self.__poincare = poincare

    def plotShape(self, plot, linewidth = c.THINLINE, poincare = False):
        """ Plots the center point and circle in the given plot
        When poincare is false, draws a euclidean circle around the center point

        Parameters
        ----------
        plot : obj
            the plot to draw the shape in 
        linewidth: int, optional
            width of the line creating the circle
        poincare: boolean, optional
            whether or not the Circle is in poincare mode - used to ensure correct type of plotting 
        """
        if poincare == True:
            self.plotShapePoincare(plot, linewidth=linewidth)
            return            
        if self.__centerPoint != None:
            self.__circle = patches.Circle((self.__centerPoint.getX(), self.__centerPoint.getY()), radius=self.__radius, edgecolor='black', facecolor = 'None', linewidth= linewidth)

            #plots circle and radius point
            plot.add_patch(self.__circle)
            self.__centerPointPlot = self.__centerPoint.plotShape(plot,linewidth)

    def plotShapePoincare(self,plot,linewidth=c.THINLINE):
        """ Plots the center point and Hyperbolic circle in the given plot

        Parameters
        ----------
        plot : obj
            the plot to draw the shape in 
        linewidth: int, optional
            width of the line creating the circle
        """
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

            self.__circle = plot.contour(X,Y,Z,[0], colors="black", linewidths = linewidth)
            self.__centerPointPlot = self.__centerPoint.plotShape(plot)

    def convertToPoincare(self):
        """ Converts the center point of the circle to its poincare mapping, sets poincare boolean to True
        """
        if self.__poincare == False:
            self.getCenterPoint().convertToPoincare()
            self.__poincare = True

    def convertToEuclidean(self):
        """ Converts the center point of the circle to its Euclidean mapping, sets poincare boolean to False
        """
        if self.__poincare == True:
            self.getCenterPoint().convertToEuclidean()
            self.__poincare = False

    def plotShapeScaledPlotsize(self,plot,oldPlotSize, newPlotSize):
        """ Plots the center point and Euclidean circle in the given plot, adjusting the pointsize based on the old/new plot sizes 

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

        figure.getCenterPoint().setPointSize(c.DEFAULTPOINTSIZE*scaleFactor)
        figure.plotShape(plot,c.THINLINE)

    def scale(self,scaleVal,plot,poincare = False):
        """ Scales the entire shape by the scaleVal AND plots the new scaled shape AND sets radius back to its original radius after plotting.
        The scaled change is NOT permanent (original radius is restored). This is done to ensure that when dragging the slider, the shape is being 
        scaled based on its original raidus, not the already scaled radius. 

        Parameters
        ----------
        scaleVal : float
            The value by which to scale the radius of the shape
        plot: obj
            the plot for the shape to appear in
        poincare: boolean, optional
            whether or not the object is in poincare mode
        """

        self.removeShape()
        oldRadius = self.getRadius()
        newRadius = scaleVal * oldRadius
        self.setRadius(newRadius)
        self.plotShape(plot,c.THICKLINE, poincare=poincare)
        self.setRadius(oldRadius)

    def confirmScaleSize(self,scaleVal,plot, poincare = False):
        """ Scales the entire shape by the scaleVal AND plots the new scaled shape
        The scaled change IS permanent  

        Parameters
        ----------
        scaleVal : float
            The value by which to scale the radius of the shape
        plot: obj
            the plot for the shape to appear in
        poincare: boolean, optional
            whether or not the object is in poincare mode
        """

        self.removeShape()
        oldRadius = self.getRadius()
        newRadius = scaleVal * oldRadius
        self.setRadius(newRadius)
        self.plotShape(plot,c.THICKLINE, poincare=poincare)

    def removeShape(self):
        """ removes the centerpoint and circle plots from the canvas.
        """

        if self.__circle != None:
            # removes line and endPoint
            self.__circle.remove()
            self.__circle = None
            self.__centerPointPlot.remove()

    def moveShape(self, deltaX, deltaY):
        """ moves centerpoint by the given delta amounts. 

        Parameters
        ----------
        deltaX : float
            the Euclidean horizontal distance for the shape to move
        deltaY: float
            the Euclidean vertical distance for the shape to move
        """
        if self.__poincare == False:
            self.__centerPoint =Point.Point(self.getCenterPoint().getX()+deltaX, self.getCenterPoint().getY() + deltaY)
    
    def moveShapePoincare(self, primaryPoint, newPrimaryPoint):
        """ moves center point to a new location. 

        Parameters
        ----------
        primaryPoint : Point
            the point to move (should be center point)
        newPrimaryPoint: Point
            new location for center point to move
        """
        if primaryPoint.exactEquals(self.getCenterPoint()):
            self.getCenterPoint().movePoint(pointToMove=primaryPoint,newPoint=newPrimaryPoint)

    def movePoint(self, pointToMove, newPoint):
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
            True when the center point can be moved and stays within the boundaries, False otherwise
        """
        
        if self.__centerPoint.exactEquals(pointToMove):
            bool = self.getCenterPoint().movePoint(pointToMove,newPoint)
            return bool
        else:
            return False

    def setStartPoint(self, centerPoint):
        """ Sets the 'start point' / center point of the line to a new point.

        Parameters
        ----------
        centerPoint : Point
            the new center point
        """
        self.setCenterPoint(centerPoint)

    def setCenterPoint(self, centerPoint):
        """ Sets the center point of the line to a new point

        Parameters
        ----------
        centerPoint : Point
            the new center point
        """

        self.__centerPoint = centerPoint
        if self.__poincare:
            centerPoint.setPoincare(True)
    
    def setEndPoint(self, endPoint):
        """ If the radius is already set, sets the center point as the new point. 
        Otherwise, sets the radius as the Euclidean distance from the center to the new point

        Note: this is done to simplify the EventHandlers class in terms of drawing and updating circles

        Parameters
        ----------
        endPoint : Point
            the new end point
        """

        # if setting radius for first time, set radius. Else move the center point
        if (self.__radiusSet):
            self.setCenterPoint(endPoint)
        else:
            if self.__poincare == True:
                # allows the radius to closer match the cursor
                self.__centerPoint.convertToEuclidean()
                endPoint.convertToEuclidean()
                self.__radius = math.sqrt(((self.__centerPoint.getX()-endPoint.getX()))**2+(self.__centerPoint.getY()-endPoint.getY())**2)
                self.__centerPoint.convertToPoincare()
            else:
                self.__radius = math.sqrt(((self.__centerPoint.getX()-endPoint.getX()))**2+(self.__centerPoint.getY()-endPoint.getY())**2)

    def setRadius(self,radius):
        """ Sets the radius of the circle

        Parameters
        ----------
        radius : float
            the new radius
        """
        self.__radius = radius

    def getRadiusSet(self):
        return self.__radiusSet
    
    def getCenterPoint(self):
        """ Returns the Circle's center point
        
        Returns
        ----------
        Point
            the center point of the line
        """
        return self.__centerPoint
    
    def getStartPoint(self):
        """ Returns the Circle's 'start'/center point
        
        Returns
        ----------
        Point
            the center point of the line
        """

        return self.__centerPoint
    
    def getEndPoint(self):
        """ Returns the Circle's 'end'/center point
        
        Returns
        ----------
        Point
            the center point of the line
        """
        return self.__centerPoint

    def getRadius(self):
        """ Returns the Circle's radius value
        
        Returns
        ----------
        float
            the radius value
        """
        return self.__radius
    
    def getShape(self):
        """ Returns the circle plot of the object

        Returns
        ----------
        obj
            the circle plot 
        """
        return self.__circle
                
    def getPoincare(self):
        """ Returns the Circle's poincare value

        Returns
        ----------
        boolean
            whether or not the circle is in poincare mode 
        """
        return self.__poincare
    
    def containsPoint(self, point):
        """ Determines if the circle contains the given point (the given point can be off by an epsilon value associated with the Point class)
        If the circle DOES contain the point, marks the radius set boolean to true

        Parameters 
        ----------
        point : Point
            the point to check if the Line contains

        Returns
        ----------
        boolean
            whether or not the given point is found within the line
        """

        if point.equals(self.__centerPoint):
            self.__radiusSet = True #implies that circle is fully drawn and can only be moved now (radius will not change)
            return True
        else: 
            return False
        
    def exactContainsPoint(self,point):
        """ Determines if the circle contains the given EXACT point (no epsilon allowance)

        Parameters 
        ----------
        point : Point
            the point to check if the circle contains

        Returns
        ----------
        boolean
            whether or not the given point is found within the circle
        """

        if (self.getCenterPoint().getX() == point.getX() or self.getCenterPoint().getY() == point.getY()):
            return True
        else:
            return False

    def getPoint(self,point):
        """ Finds the exact Point that is found with self.containsPoint(point)

        essentially removes the epsilon value associated with a contained point for smoother joining of shapes

        Parameters 
        ----------
        point : Point
            the point used to find the exact Circle point

        Returns
        ----------
        Point
            the point contained in the Circle that is within an epsilon value of the given point
        """
        if (self.containsPoint(point)):
            return self.getEndPoint()

        if (self.containsPoint(point)):
            return self.getEndPoint()

    def getLength(self):
        """ Finds the Euclidean distance around the circle (circumference)

        Returns
        ----------
        float
            the circumference of the circle
        """
        return self.getCircumference()
        
    def getCircumference(self):
        """ Finds the Euclidean distance around the circle (circumference)

        Returns
        ----------
        float
            the circumference of the circle
        """
        return math.pi * 2 * self.__radius
    
    def getArea(self):
        """ Finds the Euclidean area of the circle 

        Returns
        ----------
        float
            the area of the circle
        """

        return math.pi * (self.__radius ** 2)
    
    def measure(self):
        """ Returns a string of details about the circle including its radius, circumference, and area

        Returns
        ----------
        String
            a string containing details about the circle
        """

        label = "Radius: {0}\nCircumference: {1}\nArea: {2}".format(round(self.getRadius(), 3), round(self.getCircumference(),3),round(self.getArea(),3))
        return label

    def print(self):
        """ Prints information about the line including the line's memory address in addition to details about the start and end point 
        """
        string = "Circle: " + str(self)
        string += "\n\tCenterPoint: " + str(self.getCenterPoint()) 
        print(string)
