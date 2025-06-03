""""
Class to define compound shapes

"""

class Shape:
    __components = []

    def __init__(self, components):
        self.__components = components

    def plotShape(self,plot,canvas):
        for component in self.__components:
            component.plotShape(plot,canvas)
    
    def removeShape(self,canvas):
        for component in self.__components:
            component.removeShape(canvas)

    def containsPoint(self,point):
        for component in self.__components:
            if (component.containsPoint(point)):
                return True
        
        return False
    
    def getLength(self):
        totalLength = 0
        for component in self.__components:
            totalLength += component.getLength()

        return totalLength
    
    def measure(self):
        returnString = "Num Components: {0}\n Total Length: {1}".format(len(self.__components), self.getLength())
        return returnString