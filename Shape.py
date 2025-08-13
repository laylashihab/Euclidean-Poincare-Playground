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
    __poincare = False # boolean determining if the shape is in poincare mode or not

    # takes in a list of shape (line, point, shape, or circle) objects and an integer number of components
    def __init__(self, shape1, shape2, arcPlotLists):
        finalComponents = []
        if type(shape1) == Shape:
            finalComponents.extend(shape1.getComponents())
        else:
            finalComponents.append(shape1)
        if type(shape2) == Shape:
            finalComponents.extend(shape2.getComponents())
        else:
            finalComponents.append(shape2)
        self.__components = finalComponents
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

        self.__poincare == True

    def convertToEuclidean(self):
        for component in self.__components:
            component.convertToEuclidean()

        self.__poincare == False

    def scaleFunc(self,point,midpoint,scaleVal):
            # finds the distance the startpoint must move
            curDistanceToMid = point.getDistance(midpoint)
            newDistance = curDistanceToMid * scaleVal

            # finds the angle of the line connecting the midpoint to point
            dx = (point.getX() - midpoint.getX())
            if dx == 0:
                return point

            dy = (point.getY() - midpoint.getY())
            angle = math.atan(dx/dy)   
            
            if dy*dx < 0 :
                angle *= -1

            # finds the new point of point using the angle
            deltaX = (newDistance-curDistanceToMid) * math.sin(angle)

            if (point.getX() > midpoint.getX()):
                deltaX *= -1

            newX = point.getX() - deltaX
            newY = point.getY() + ((dy/dx)) * (newX-point.getX())

            # sets the new startpoint
            newPoint = Point.Point(newX,newY)

            return newPoint

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
            if poincare == True:
                component.convertToEuclidean()

            if type(component) == Line:
                # dealing with start point
                currentStart = component.getStartPoint()

                newStart = self.scaleFunc(currentStart,midpoint,scaleVal)
                if newStart.equals(midpoint,epsilon=c.EPSILON):
                    pass
                else:
                    component.setStartPoint(newStart)
                
                # dealing with the endpoint 
                currentEnd = component.getEndPoint()
                newEnd = self.scaleFunc(currentEnd,midpoint,scaleVal)
                if newEnd.equals(midpoint,epsilon=c.EPSILON):
                    pass
                else:
                    component.setEndPoint(newEnd)
            elif type(component) == Circle:
                currentCenter = component.getCenterPoint()

                newCenter = self.scaleFunc(currentCenter,midpoint,scaleVal)
                if newCenter.equals(midpoint,epsilon=c.EPSILON):
                    pass
                else:
                    component.setCenterPoint(newCenter)

                currentRadius = component.getRadius()
                newRadius = currentRadius * scaleVal
                component.setRadius(newRadius)

            if poincare == True:
                component.convertToPoincare()

            # deals w plotting
            component.removeShape()
            component.plotShape(plot, linewidth= c.THICKLINE,poincare=poincare)

            # resets points
            if type(component) == Line:
                component.setStartPoint(currentStart)
                component.setEndPoint(currentEnd)
            else:
                component.setCenterPoint(currentCenter)
                component.setRadius(currentRadius)

            if poincare == True:
                component.convertToPoincare()

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
            if poincare == True:
                component.convertToEuclidean()

            if type(component) == Line:
                # dealing with start point
                currentStart = component.getStartPoint()

                newStart = self.scaleFunc(currentStart,midpoint,scaleVal)
                if newStart.equals(midpoint,epsilon=c.EPSILON):
                    pass
                else:
                    component.setStartPoint(newStart)
                
                # dealing with the endpoint 
                currentEnd = component.getEndPoint()
                newEnd = self.scaleFunc(currentEnd,midpoint,scaleVal)
                if newEnd.equals(midpoint,epsilon=c.EPSILON):
                    pass
                else:
                    component.setEndPoint(newEnd)
            elif type(component) == Circle:
                currentCenter = component.getCenterPoint()

                newCenter = self.scaleFunc(currentCenter,midpoint,scaleVal)
                if newCenter.equals(midpoint,epsilon=c.EPSILON):
                    pass
                else:
                    component.setCenterPoint(newCenter)

                currentRadius = component.getRadius()
                newRadius = currentRadius * scaleVal
                component.setRadius(newRadius)
                component.setRadius(newRadius)

            if poincare == True:
                component.convertToPoincare()

            # deals w plotting
            component.removeShape()
            component.plotShape(plot, linewidth= c.THICKLINE,poincare=poincare)

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
        component.setEndPoint(endPoint)
        if self.__poincare == True:
            endPoint.setPoincare(True)

    # sets the final component in components list as the component containing the given point
    def setLastComponent(self,point):
        for component in self.__components:
            if component.containsPoint(point):
                newComponentsList = self.__components[:]
                newComponentsList.remove(component)
                newComponentsList.append(component)
                self.__components = newComponentsList
                return
    
    # gets the last drawn point of the figure
    def getEndPoint(self):
        return self.__components[-1].getEndPoint()
    
    def getPoincare(self):
        return self.__components[-1].getPoincare()

    # moves the entire shape by some deltaX and deltaY by moving each component
    def moveShape(self, deltaX,deltaY):
        pointList = self.getAllPoints()
        
        for point in pointList:
            point.moveShape(deltaX,deltaY)

    # moves the shape a distance specified by two points from the Poincare model
    # performs all calculations and transformations in euclidean mode, then converts to poincare mode.
    def moveShapePoincare(self, primaryPoint, newPrimaryPoint):
        # finds the distance to move each point
        primaryPoint.convertToEuclidean()
        newPrimaryPoint.convertToEuclidean()
        deltaX = newPrimaryPoint.getX() - primaryPoint.getX()
        deltaY = newPrimaryPoint.getY() - primaryPoint.getY()
        primaryPoint.convertToPoincare()
        newPrimaryPoint.convertToPoincare()

        # compiles a list of unique points in the shape (avoids transforming the same shape twice)
        pointList = self.getAllPoints()

        for point in pointList:
            point.convertToEuclidean()
            point.moveShape(deltaX,deltaY)
            point.convertToPoincare()
        
    # gets a list of all unique points in the shape
    def getAllPoints(self):
        pointList = set()
        for component in self.__components:
            if type(component) == Line:
                pointList.add(component.getStartPoint())
                pointList.add(component.getEndPoint())
            else:
                pointList.add(component.getCenterPoint())

        return pointList

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
        # checks through components in reverse order
        for i in range(len(self.__components) - 1, -1, -1):
            component = self.__components[i]
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
            radius = min(minLine/2,EventHandlers.plotBounds / 2)

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
            if type(component) == Line:
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
    
    def hasAngle(self):
        numLines = 0
        for component in self.__components:
            if type(component) == Line:
                numLines += 1
            if numLines >= 2:
                return True
        return False
    
    def print(self):
        print("Components: " + str(self.getNumComponents()) + "\tNum Arc Plots: " + str(len(self.__arcPlotLists)))
        for component in self.__components:
            print("\t",end="")
            component.print()
    
