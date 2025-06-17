from Point import *
from Line import *
from Circle import *
from Shape import *
from Achievement import *

import FrameSetUp

"""
Series of functions to deal with mouseEvents

"""

THINLINE = 1
THICKLINE = 3

# function to deal with user clicking.
def click_handler(event):
    if (not event.inaxes):
        return
    
    global shapeList,foundPoint,currentPoint,currentShape,mouseDown,movePoint

    currentPoint = Point(event.xdata, event.ydata)
    foundPoint = False

    mouseDown = True

    # checks if the point where the user clicked is a point in a shape
    for shape in shapeList:
        if shape.containsPoint(currentPoint):
            foundPoint = True
            if toolMode == "Move":
                # sets the point to move as the point the user is clikcing on
                movePoint = currentPoint
                currentShape = shape
            elif toolMode == "Draw":
                currentPoint = shape.getPoint(currentPoint)
                currentShape = newBasicShape(currentPoint)

                newShape(shape)
                return
            elif toolMode == "Delete":
                shape.removeShape(CANVAS)
                shapeList.remove(shape)
            elif toolMode == "Select":
                currentShape = shape   
         
    # if the user is clicking on a clear space of the CANVAS
    if (foundPoint == False):
        if (toolMode == "Draw"):
            currentShape = newBasicShape(currentPoint)

            # updates data display
            FrameSetUp.dataDisplay.config(text=currentShape.measure())
            FrameSetUp.dataDisplay.update()
        else:
            currentShape = None    

def drag_handler(event):
    if not event.inaxes or not mouseDown:
        return
    
    global shapeType,movePoint,currentShape,currentPoint,shapeList,toolMode

    lastPoint = currentPoint.copy()
    currentPoint = Point(event.xdata,event.ydata)

    if currentShape == None:
        return

    if toolMode == "Draw":
        # if the user is trying to draw a point but drags instead, creates a line
        if shapeType == "Point":
            currentShape.removeShape(CANVAS)
            if (currentShape in shapeList):
                shapeList.remove(currentShape)
            FrameSetUp.changeShape("Line")
            FrameSetUp.changeButtonColor(FrameSetUp.lineButton)
            currentShape = newBasicShape(startPoint=currentPoint)

        currentShape.draw(PLOT,CANVAS,endPoint=currentPoint, linewidth=THINLINE)

        # updates data display
        FrameSetUp.dataDisplay.config(text=currentShape.measure())
        FrameSetUp.dataDisplay.update()

    elif toolMode == "Move":
        # removes the current drawing of the line
        currentShape.removeShape(CANVAS)

        # moves the point to the current point
        currentShape.movePoint(movePoint, currentPoint)
        movePoint = currentPoint
        currentShape.plotShape(PLOT, CANVAS, THINLINE)

        # ensures angles and metrics are shown that must be displayed
        if (type(currentShape) == Shape and FrameSetUp.showAnglesButton.cget("text") == "Hide Angles"):
            currentShape.showAngles(PLOT,CANVAS)
        elif (FrameSetUp.showMetricsButton.cget("text") == "Hide Metrics"):
            currentShape.showMetrics(PLOT,CANVAS)

        # updates data display
        FrameSetUp.dataDisplay.config(text=currentShape.measure())
        FrameSetUp.dataDisplay.update()

    # moves the entire shape
    elif (toolMode == "Select"):
        if (type(currentShape) == Shape):
            currentShape.hideAngles(CANVAS)
        currentShape.removeShape(CANVAS)
        deltaX = currentPoint.getX() - lastPoint.getX()
        deltaY = currentPoint.getY() - lastPoint.getY()
        currentShape.moveShape(deltaX, deltaY)
        currentShape.plotShape(PLOT, CANVAS, THICKLINE)

        # updates data display
        FrameSetUp.dataDisplay.config(text=currentShape.measure())
        FrameSetUp.dataDisplay.update()

def unclick_handler(event):
    global currentPoint,currentShape,mouseDown
    mouseDown = False

    currentPoint = Point(event.xdata,event.ydata)

    if (toolMode == "Draw" or toolMode == "Move" or toolMode == "Select"):
        for shape in shapeList:
            # changes lines to thin 
            currentShape.removeShape(CANVAS)
            currentShape.plotShape(PLOT, CANVAS,THINLINE)

            if (shape != currentShape and type(shape) != Point and shape.containsPoint(currentPoint)):
                currentShape.setEndPoint(shape.getPoint(currentPoint))

                newShape(shape)

                # updates data display
                FrameSetUp.dataDisplay.config(text=currentShape.measure())
                FrameSetUp.dataDisplay.update()
    
    # ensures selected shapes are still selected and thick
    if (toolMode == "Select"):
        currentShape.removeShape(CANVAS)
        currentShape.plotShape(PLOT, CANVAS,THICKLINE)

        if (type(currentShape) == Shape and currentShape.isClosedFigure()):
            FrameSetUp.saveFigureButton.grid(row=6, column=3,padx=FrameSetUp.PADX,pady=FrameSetUp.PADY)
        else:
            FrameSetUp.saveFigureButton.grid_forget()

    else:
        currentShape = None


    # ensures angles and metrics are shown that must be displayed
    if (type(currentShape) == Shape and FrameSetUp.showAnglesButton.cget("text") == "Hide Angles"):
        currentShape.showAngles(PLOT,CANVAS)
    if (FrameSetUp.showMetricsButton.cget("text") == "Hide Metrics"):
        currentShape.showMetrics(PLOT, CANVAS)

    # achievements for creating a circle or line
    if (MAIN.achievementsOn and ACHIEVEMENTSDICT["createCircle"].isComplete() == False and type(currentShape) == Circle):
        ACHIEVEMENTSDICT["createCircle"].showAchievement()
    elif (MAIN.achievementsOn and ACHIEVEMENTSDICT["createLine"].isComplete() == False and type(currentShape) == Line):
        ACHIEVEMENTSDICT["createLine"].showAchievement()


    # various types of angle achievements
    if MAIN.achievementsOn and type(currentShape) == Shape:
        if (ACHIEVEMENTSDICT["createAcuteAngle"].isComplete() == False or ACHIEVEMENTSDICT["createObtuseAngle"].isComplete() == False or ACHIEVEMENTSDICT["createRightAngle"].isComplete() == False):
            angles = currentShape.showAngles(PLOT, CANVAS)
            currentShape.hideAngles(CANVAS)
            for angle in angles:
                if ACHIEVEMENTSDICT["createAcuteAngle"].isComplete() == False and angle < 90:
                    ACHIEVEMENTSDICT["createAcuteAngle"].showAchievement()
                elif ACHIEVEMENTSDICT["createRightAngle"].isComplete() == False and angle == 90:
                    ACHIEVEMENTSDICT["createRightAngle"].showAchievement()
                elif ACHIEVEMENTSDICT["createObtuseAngle"].isComplete() == False and angle > 90:
                    ACHIEVEMENTSDICT["createObtuseAngle"].showAchievement()

# initializes a new Basic shape (Point, Line, Circle)
# for points, creates a new point object
# for lines and circles, sets the endpoint and startpoint to the given start point 
def newBasicShape(startPoint):
    global CANVAS,PLOT

    # creates a new point
    if (shapeType == "Point"):

        # achievement for creating a point
        if (ACHIEVEMENTSDICT["createPoint"].isComplete() == False and MAIN.achievementsOn):
            ACHIEVEMENTSDICT["createPoint"].showAchievement()

        shape =startPoint.copy()
        shape.plotShape(PLOT,CANVAS,THICKLINE)
        shapeList.append(shape)
    else:
        # creates lines and circles
        shape = Line() if shapeType == "Line" else Circle()
        shape.setStartPoint(startPoint)
        shape.setEndPoint(startPoint)
        shapeList.append(shape)

    return shape

# creates a new Shape type shape
def newShape(newShape):
    global currentShape

    # create Angle achievement
    if (ACHIEVEMENTSDICT["createAngle"].isComplete() == False and type(newShape) == Line and type(currentShape) == Line and MAIN.achievementsOn):
        ACHIEVEMENTSDICT["createAngle"].showAchievement()

    numComponents = 1 + newShape.getNumComponents()
    shapes = [newShape, currentShape]

    if (newShape in shapeList):
        shapeList.remove(newShape)
    if (currentShape in shapeList):
        shapeList.remove(currentShape)

    # gathers all arcplots
    arcPlots = []
    if (type(newShape) == Shape):
        arcPlots.extend(newShape.getArcPlotLists())
    if (type(currentShape) == Shape):
        arcPlots.extend(currentShape.getArcPlotLists())
    currentShape = Shape(shapes, numComponents, arcPlots)
    shapeList.append(currentShape)

# class variables
currentShape = None
currentPoint = None
movePoint = None
mouseDown = False
shapeType = "Point"
shapeList = [] 
toolMode = "Draw"

# constant variables to set from Main
CANVAS = None
PLOT = None
ACHIEVEMENTSDICT = None
MAIN = None

# sets up bindings with CANVAS
def bindEvents(Main):
    global CANVAS, PLOT, ACHIEVEMENTSDICT
    global MAIN
    
    CANVAS = FrameSetUp.CANVAS
    PLOT = FrameSetUp.PLOT
    ACHIEVEMENTSDICT = Main.ACHIEVEMENTSDICT

    MAIN = Main

    CANVAS.mpl_connect("button_press_event", click_handler)
    CANVAS.mpl_connect("motion_notify_event", drag_handler)
    CANVAS.mpl_connect("button_release_event", unclick_handler)


