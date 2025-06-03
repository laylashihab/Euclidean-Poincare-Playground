import math
import matplotlib.patches as patches

""""
class to create Euclidean Circle objects

Cirles are defined by a center point and radius
"""

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
            self.__circle = patches.Circle((self.__centerPoint.getX(), self.__centerPoint.getY()), radius=self.__radius, edgecolor='blue', facecolor = 'None')

            #plots circle and radius point
            plot.add_patch(self.__circle)
            self.__centerPointPlot, = plot.plot(self.__centerPoint.getX(),self.__centerPoint.getY(), "o")
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

    # updates the part of the circle that moves (either radius or center point)
    def setEndPoint(self, endPoint):
        # if setting radius for first time, set radius. Else move the center point
        if (self.__moveCenter):
            self.__centerPoint = endPoint
            self.__circle = None
        else:
            self.__radius = math.sqrt(((self.__centerPoint.getX()-endPoint.getX()))**2+(self.__centerPoint.getY()-endPoint.getY())**2)

    def getCenterPoint(self):
        return self.__centerPoint
    
    def getRadius(self):
        return self.__radius
    
    def getShape(self):
        return self.__circle
    
    # checks if a given point is the center point
    # if so, marks that the center will be move (radius will not be adjusted)
    def containsPoint(self, point):
        if point.equals(self.__centerPoint):
            self.__moveCenter = True
            return True
        else: 
            return False
        
    # returns the euclidean distance around the circle
    def getCircumference(self):
        return math.pi * 2 * self.__radius
    
    # returns the euclidean area of the circle
    def getArea(self):
        return math.pi * (self.__radius ** 2)
    