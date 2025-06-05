""""
Class to define compound shapes

"""
class Shape():
    __components = []
    __numComponents = 0

    def __init__(self, components, numComponents):
        self.__components = components
        self.__numComponents = numComponents

    def plotShape(self,plot,canvas):
        for component in self.__components:
            component.plotShape(plot,canvas)
    
    def removeShape(self,canvas):
        for component in self.__components:
            component.removeShape(canvas)

    def moveShape(self, deltaX,deltaY):
        for component in self.__components:
            component.moveShape(deltaX,deltaY)

    def movePoint(self, point, newPoint):
        for component in self.__components:
            if (component.containsPoint(point)):
                component.movePoint(newPoint)

    def containsPoint(self,point):
        for component in self.__components:
            if (component.containsPoint(point)):
                return True
        
        return False
    
    def getPoint(self,point):
        for component in self.__components:
            p =component.getPoint(point)
            if (p != None):
                return p
    
    def getLength(self):
        totalLength = 0
        for component in self.__components:
            totalLength += component.getLength()

        return totalLength
    
    def measure(self):
        returnString = "Num Components: {0}\n Total Length: {1}".format(self.__numComponents, round(self.getLength(),3))
        return returnString
    
    def setEndPoint(self, endPoint):
        self.__components[-1].setEndPoint(endPoint)

    def getEndPoint(self):
        return self.__components[-1].getEndPoint()
    
    def getNumComponents(self):
        return self.__numComponents
    
    def setNumComponents(self, numComponents):
        self.__numComponents = numComponents