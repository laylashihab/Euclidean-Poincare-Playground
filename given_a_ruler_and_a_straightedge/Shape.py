""""
Class to define compound shapes

shape and figure are used interchangeably
"""

from Line import *
from Circle import *
import constants as c
import EventHandlers

class Shape():
    __components = []
    __arcPlotLists = [] # stores both the arc and measurement plot

    # takes in a list of shape (line, point, shape, or circle) objects and an integer number of components
    def __init__(self, components, arcPlotLists):
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
        self.__arcPlotLists = arcPlotLists

    # plots each part of the shape
    def plotShape(self,plot, linewidth = c.THINLINE,poincare=False):
        for component in self.__components:
            component.plotShape(plot,linewidth,poincare)

    # plots a scaled version of the shape
    def plotShapeScaledPlotsize(self,plot,oldPlotSize, newPlotSize):
        for component in self.__components:
            component.plotShapeScaledPlotsize(plot,oldPlotSize, newPlotSize)

    def plotShapePoincare(self, plot, linewidth = c.THINLINE):
        for component in self.__components:
            component.plotShapePoincare(plot,linewidth)

    def convertToPoincare(self):
        for component in self.__components:
            component.convertToPoincare()

    def convertToEuclidean(self):
        for component in self.__components:
            component.convertToEuclidean()

    def scale(self,scaleVal,plot,poincare=False):
        # finds the midpoint of the shape
        points = set()
        for component in self.getComponents():
            points.add(component.getStartPoint())
            points.add(component.getEndPoint())
        numPoints = len(points)
        xTotal = 0
        yTotal = 0
        for p in points:
            xTotal += p.getX()
            yTotal += p.getY()

        midpoint = Point.Point(xTotal/numPoints, yTotal/numPoints)

        for component in self.getComponents():
            if (type(component) == Line):
                if (poincare == True):
                    component.convertToEuclidean()
                # dealing with start point
                currentStart = component.getStartPoint()

                # finds the distance the startpoint must move
                curDistanceToMid = currentStart.getDistance(midpoint)
                newDistance = curDistanceToMid * scaleVal

                # finds the angle of the line connecting the midpoint to point
                dx = (currentStart.getX() - midpoint.getX())
                dy = (currentStart.getY() - midpoint.getY())
                angle = math.atan(dx/dy)   
                
                if dy*dx < 0 :
                    angle *= -1

                # finds the new point of point using the angle
                deltaX = (newDistance-curDistanceToMid) * math.sin(angle)

                if (currentStart.getX() > midpoint.getX()):
                    deltaX *= -1

                newX = currentStart.getX() - deltaX
                newY = currentStart.getY() + ((dy/dx) * (newX-currentStart.getX()))

                # sets the new startpoint
                startPoint = component.getStartPoint()
                startPoint.setX(newX)
                startPoint.setY(newY)
                
                # dealing with the endpoint 
                currentEnd = component.getEndPoint()
                curDistanceToMid = currentEnd.getDistance(midpoint)
                newDistance = curDistanceToMid * scaleVal

                # finds the angle
                dx = (currentEnd.getX() - midpoint.getX())
                dy = (currentEnd.getY() - midpoint.getY())
                angle = math.atan(dx/dy)   
                if dy*dx < 0 :
                    angle *= -1
                deltaX = (newDistance-curDistanceToMid) * math.sin(angle)
                if (currentEnd.getX() > midpoint.getX()):
                    deltaX *= -1

                newX = currentEnd.getX() - deltaX
                newY = currentEnd.getY() + ((dy/dx)) * (newX-currentEnd.getX())

                # sets the new endpoint
                endPoint = component.getEndPoint()
                endPoint.setX(newX)
                endPoint.setY(newY)

                if poincare == True:
                    component.convertToPoincare()

                # deals w plotting
                component.removeShape()
                component.plotShape(plot, c.THICKLINE,poincare=poincare)

                # resets start and endpoints
                component.setStartPoint(currentStart)
                component.setEndPoint(currentEnd)

                if poincare == True:
                    component.convertToPoincare()

            else: # dealing w circles
                component.scale(scaleVal,plot,poincare=poincare)

    def confirmScaleSize(self,scaleVal,plot,poincare = False):
        # finds the midpoint of the shape
        points = set()
        for component in self.getComponents():
            points.add(component.getStartPoint())
            points.add(component.getEndPoint())
        numPoints = len(points)
        xTotal = 0
        yTotal = 0
        for p in points:
            xTotal += p.getX()
            yTotal += p.getY()

        midpoint = Point.Point(xTotal/numPoints, yTotal/numPoints)

        for component in self.getComponents():
            if (type(component) == Line):
                if poincare == True:
                    component.convertToEuclidean()

                # dealing with start point
                currentStart = component.getStartPoint()

                # finds the distance the startpoint must move
                curDistanceToMid = currentStart.getDistance(midpoint)
                newDistance = curDistanceToMid * scaleVal

                # finds the angle of the line connecting the midpoint to point
                dx = (currentStart.getX() - midpoint.getX())
                if dx == 0:
                    break

                dy = (currentStart.getY() - midpoint.getY())
                angle = math.atan(dx/dy)   
                
                if dy*dx < 0 :
                    angle *= -1

                # finds the new point of point using the angle
                deltaX = (newDistance-curDistanceToMid) * math.sin(angle)

                if (currentStart.getX() > midpoint.getX()):
                    deltaX *= -1

                newX = currentStart.getX() - deltaX
                newY = currentStart.getY() + ((dy/dx)) * (newX-currentStart.getX())

                # sets the new startpoint
                startPoint = component.getStartPoint()
                startPoint.setX(newX)
                startPoint.setY(newY)
                
                # dealing with the endpoint 
                currentEnd = component.getEndPoint()
                curDistanceToMid = currentEnd.getDistance(midpoint)
                newDistance = curDistanceToMid * scaleVal

                # finds the angle
                dx = (currentEnd.getX() - midpoint.getX())

                if (dx == 0):
                    break

                dy = (currentEnd.getY() - midpoint.getY())
                angle = math.atan(dx/dy)   
                if dy*dx < 0 :
                    angle *= -1
                deltaX = (newDistance-curDistanceToMid) * math.sin(angle)
                if (currentEnd.getX() > midpoint.getX()):
                    deltaX *= -1

                newX = currentEnd.getX() - deltaX
                newY = currentEnd.getY() + ((dy/dx)) * (newX-currentEnd.getX())

                # sets the new endpoint
                endPoint = component.getEndPoint()
                endPoint.setX(newX)
                endPoint.setY(newY)

                if poincare == True:
                    component.convertToPoincare()

                # deals w plotting
                component.removeShape()
                component.plotShape(plot,c.THICKLINE, poincare=EventHandlers.poincareMode)

            else: # dealing w circles
                component.confirmScaleSize(scaleVal,plot)

    # removes each part of the shape
    def removeShape(self):
        for component in self.__components:
            component.removeShape()

        self.__arcPlotLists = []

    def getStartPoint(self):
        return self.__components[0].getStartPoint()

    # sets the end point of the last figure drawn
    def setEndPoint(self, endPoint):
        component = self.__components[-1]
        if type(component) != Point:
            component.setEndPoint(endPoint)

    # gets the last drawn point of the figure
    def getEndPoint(self):
        return self.__components[-1].getEndPoint()

    # moves the entire shape by some deltaX and deltaY by moving each component
    def moveShape(self, deltaX,deltaY):
        for component in self.__components:
            component.moveShape(deltaX,deltaY)

    def moveShapePoincare(self, deltaX=0,deltaY=0):
        for component in self.__components:
            component.moveShapePoincare(deltaX,deltaY)

    # moves a particular point in the shape and updates the components that use that point 
    def movePoint(self, pointToMove, newPoint):
        for component in self.__components:
            if (component.exactContainsPoint(pointToMove)):
                component.movePoint(pointToMove, newPoint)

    # checks if any component contains a given point
    def containsPoint(self,point):
        for component in self.__components:
            if (component.containsPoint(point)):
                return True
        return False
    
    # returns a boolean regarding if the figure is closed 
    # a closed figure has the same starting and ending point
    def isClosedFigure(self):
        # checks that each point from a line or circle is connected to another

        # creates a list of all points
        pointsList = []
        for component in self.__components:
            if (type(component)==Line):
                pointsList.append(component.getStartPoint())
                pointsList.append(component.getEndPoint())
            elif type(component)== Circle:
                pointsList.append(component.getCenterPoint())
                
        # initializes a list to hold any point that has two or more shapes associated with it
        nonUniquePointsList = []

        # compares each point with every other point
        for i in range(0, len(pointsList)-1):
            for j in range(i+1,len(pointsList)):
                if pointsList[i].equals(pointsList[j]):
                    nonUniquePointsList.append(pointsList[i])
                    nonUniquePointsList.append(pointsList[j])

        # if there are NO unique points, the figure is closed
        if (set(pointsList) == set(nonUniquePointsList)):
            return True
        else:
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
            if type(component!= Point):
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
            
    # shows the angles between lines on a shape
    # returns a list of angle measures 
    def showAngles(self,plot):
        pairList = self.findConnectedLines()
        angleList = []
        self.__arcPlotLists = []
        for pair in pairList:
            # shared point
            point = pair[0].getStartPoint() if pair[1].containsPoint(pair[0].getStartPoint()) else pair[0].getEndPoint()

            # find a good radius based on length of lines
            l1 = pair[0].getLength()
            l2 = pair[1].getLength()
            minLine = min(l1,l2)
            radius = min(minLine/2,EventHandlers.plotbounds / 2)

            # find start and end angles based on the lines
            angle_start = pair[0].getTerminalAngle(point) % 360
            angle_end = pair[1].getTerminalAngle(point) % 360

            # calculate ccw and cw sweep
            sweep1 = (angle_end - angle_start) % 360
            sweep2 = (angle_start - angle_end) % 360

            # select the smallest sweep
            if sweep1 < sweep2:
                start = angle_start
                sweep = sweep1
            else:
                start = angle_end
                sweep = sweep2

            # adds the sweep to the angle list
            angleList.append(sweep)

            # plot the arc
            angles_rad = np.radians(np.linspace(start,start + sweep,100))
            arc_x = point.getX() + radius* np.cos(angles_rad)
            arc_y = point.getY() + radius* np.sin(angles_rad)
            arc, = plot.plot(arc_x,arc_y, color="red")

            # plot the measurement
            midAngle = (start + start + sweep) / 2
            textDistance = radius * 1.25
            textX = point.getX() + textDistance * np.cos(np.radians(midAngle))
            textY = point.getY() + textDistance * np.sin(np.radians(midAngle))
            arcText = plot.text(textX, textY, round(sweep,3), fontsize=10, color='red', horizontalalignment= "center")

            # store the plots
            self.__arcPlotLists.append(arc)
            self.__arcPlotLists.append(arcText)
        return angleList

    def hideAngles(self):
        for arc in self.__arcPlotLists:
            arc.remove()
        self.__arcPlotLists = []

        if len(self.__arcPlotLists) != 0:
            raise("Failed to remove all angle plots")

    def showMetrics(self,plot):
        for component in self.__components:
            component.showMetrics(plot)

    def hideMetrics(self):
        for component in self.__components:
            if type(component) != Point:
                component.hideMetrics()
            
    # provides data about the shape
    def measure(self):
        returnString = "Num Components: {0}\n Total Length: {1}".format(self.getNumComponents(), round(self.getLength(),3))
        return returnString
    
    # getters and setters for the number of components in the shape
    def getNumComponents(self):
        return len(self.__components)
    
    def getComponents(self):
        return self.__components
    
    def setArcPlotLists(self, arcPlotLists):
        self.__arcPlotLists = arcPlotLists

    def getArcPlotLists(self):
        return self.__arcPlotLists
    
    def print(self):
        print("Components: " + str(self.getNumComponents()) + "\tNum Arc Plots: " + str(len(self.__arcPlotLists)))
        for component in self.__components:
            print("\t",end="")
            component.print()
    
