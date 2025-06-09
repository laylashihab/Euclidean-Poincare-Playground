""""
Class to define compound shapes

shape and figure are used interchangeably
"""

from Line import *
import matplotlib.patches as patches

class Shape():
    __components = []
    __numComponents = 0
    __arcPlotLists = []

    # takes in a list of shape (line, point, shape, or circle) objects and an integer number of components
    def __init__(self, components, numComponents):
        # breaks apart Shape components into their constituent parts and ensures order is preserved
        for component in components:
            if type(component) == Shape:
                index = components.index(component)
                components.remove(component)
                toAdd = component.getComponents()
                for component in toAdd:
                    components.insert(index, component)
                    index +=1
        self.__components = components
        self.__numComponents = numComponents

    # plots each part of the shape
    def plotShape(self,plot,canvas):
        for component in self.__components:
            component.plotShape(plot,canvas)

        self.showAngles(plot,canvas)

    
    # removes each part of the shape
    def removeShape(self,canvas):
        for component in self.__components:
            component.removeShape(canvas)
        
        for arc in self.__arcPlotLists:
            arc.remove()
        self.__arcPlotLists = []

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
    
    # returns a list of pairs of connected lines stored as tuples
    def findConnectedLines(self):
        # puts all the lines in a list
        lineList = []
        for component in self.__components:
            if type(component) == Line:
                lineList.append(component)

        # goes through each line and finds any connected lines
        pairList = []
        for i in range(0,len(lineList)-1):
            curLine = lineList[i]
            for j in range(i+1, len(lineList)):
                if lineList[j].containsPoint(curLine.getStartPoint()) or lineList[j].containsPoint(curLine.getEndPoint()):
                    pairList.append((curLine,lineList[j]))
        
        uniquePairList = []
        for s in pairList:
            if s not in uniquePairList:
                uniquePairList.append(s)
        return uniquePairList
    
    # returns a dictionary of lines and their associated angles
    def getAngles(self):
        lineAngleDict = {}
        # puts all the lines in a list
        for component in self.__components:
            if type(component) == Line:
                lineAngleDict[component] = component.getAngle(Line())
        
        return lineAngleDict
    
    # shows the angles between lines on a shape
    def showAngles(self,plot,canvas):
        lineAngleDict = self.getAngles()
        pairList = self.findConnectedLines()
        for pair in pairList:
            point = pair[0].getStartPoint() if pair[1].containsPoint(pair[0].getStartPoint()) else pair[0].getEndPoint()
            np.set_printoptions(legacy='1.25')
            pointCoord = [point.getX(), point.getY()]
            theta1 = lineAngleDict[pair[0]]
            theta2 = lineAngleDict[pair[1]]
            arc = (patches.Arc(xy=pointCoord, width=250, height=250, theta1=theta1, theta2=theta2, angle= theta2-theta1, color="red", label = str(abs(theta2-theta1))+u"\u00b0"))
            plot.add_patch(arc)
            self.__arcPlotLists.append(arc)
            canvas.draw()


    # provides data about the shape
    def measure(self):
        returnString = "Num Components: {0}\n Total Length: {1}".format(self.__numComponents, round(self.getLength(),3))
        return returnString
    
    # getters and setters for the number of components in the shape
    def getNumComponents(self):
        return self.__numComponents
    
    def setNumComponents(self, numComponents):
        self.__numComponents = numComponents

    def getComponents(self):
        return self.__components