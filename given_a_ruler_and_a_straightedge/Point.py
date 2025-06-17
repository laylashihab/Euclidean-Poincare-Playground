""""
Class to define a point in a graph
Points are defined by an x and y value
"""

class Point:
    __x = 0
    __y = 0
    __plot = None
    epsilon = 0

    def __init__(self, x = 0, y=0):
        self.__x = x
        self.__y = y

    # getters and setters
    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
    
    def getNumComponents(self):
        return 1
    
    def getLength(self):
        return 0
    
    def setEpsilon(newEpsilon):
        Point.epsilon = newEpsilon

    
    # checks if the point is equal to a given point to within some epsilon value
    def equals(self, otherPoint):
        if (otherPoint == None):
            return False
        elif (abs(self.__x - otherPoint.getX()) <= Point.epsilon and abs(self.__y - otherPoint.getY()) <= Point.epsilon):
            return True
        else:
            return False
        
    # checks if the Point shape contains a given point (essentially checks if they are close to equivalent)
    def containsPoint(self, point):
        return self.equals(point)
    
    # gets the exact point associated with a point 'equal' to this point
    # essentially removes the epsilon for smoother joining for shapes
    def getPoint(self, point):
        if (self.equals(point)):
            return self
        
    # plots the point
    def plotShape(self, plot, canvas, linewidth):
        self.__plot, = plot.plot(self.__x,self.__y, "o", color="blue", lw = linewidth)
        canvas.draw()
        return self.__plot

    # updates value for point and plots
    def draw(self,plot,canvas,endPoint,linewidth):
        self.removeShape(canvas)
        self.movePoint(self,endPoint)
        self.plotShape(plot,canvas,linewidth)

    # removes the plotted point from the canvas
    def removeShape(self,canvas):
        if (self.__plot != None):
            self.__plot.remove()
            self.__plot = None

            canvas.draw()

    # moves the point to a new location
    def movePoint(self,point, newPoint):
        self.setX(newPoint.getX())
        self.setY(newPoint.getY())

    # moves the point by a certain amount 
    def moveShape(self,deltaX,deltaY):
        self.setX(self.getX() + deltaX)
        self.setY(self.getY() + deltaY)
        
    # creates a copy of the point with a NEW memory address (not the same Point but has same values)
    def copy(self):
        return Point(self.getX(), self.getY())
    
    # provides measurements for the point
    def measure(self):
        return "{0}, {1}".format(round(self.getX(),3),round(self.getY(),3))