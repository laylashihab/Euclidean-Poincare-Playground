""""
Class to define compound shapes

shape and figure are used interchangeably
"""
class Shape():
    __components = []
    __numComponents = 0

    def __init__(self, components, numComponents):
        self.__components = components
        self.__numComponents = numComponents

    # plots each part of the shape
    def plotShape(self,plot,canvas):
        for component in self.__components:
            component.plotShape(plot,canvas)
    
    # removes each part of the shape
    def removeShape(self,canvas):
        for component in self.__components:
            component.removeShape(canvas)

    # updates the plot of the last component to be added
    def draw(self,plot,canvas,endPoint):
        self.__components[-1].draw(plot,canvas,endPoint)

    # sets the end point of the last figure drawn
    def setEndPoint(self, endPoint):
        self.__components[-1].setEndPoint(endPoint)

    # gets the last drawn point of the figure
    def getEndPoint(self):
        return self.__components[-1].getEndPoint()

    # moves the entire shape by some deltaX and deltaY by moving each component
    def moveShape(self, deltaX,deltaY):
        for component in self.__components:
            component.moveShape(deltaX,deltaY)

    # moves a particular point in the shape and updates the components that use that point 
    def movePoint(self, point, newPoint):
        for component in self.__components:
            if (component.containsPoint(point)):
                component.movePoint(point, newPoint)

    # checks if any component contains a given point
    def containsPoint(self,point):
        for component in self.__components:
            if (component.containsPoint(point)):
                return True
        return False
    
    # gets the exact point of a point in the shape if the point is contained with the shape (removes the epsilon value)
    # used for smoother combining of shapes
    def getPoint(self,point):
        for component in self.__components:
            p =component.getPoint(point)
            if (p != None):
                return p
    
    # returns the total summed length of each component in the shape
    def getLength(self):
        totalLength = 0
        for component in self.__components:
            totalLength += component.getLength()

        return totalLength
    
    # provides data about the shape
    def measure(self):
        returnString = "Num Components: {0}\n Total Length: {1}".format(self.__numComponents, round(self.getLength(),3))
        return returnString
    
    # getters and setters for the number of components in the shape
    def getNumComponents(self):
        return self.__numComponents
    
    def setNumComponents(self, numComponents):
        self.__numComponents = numComponents