from Point import *
from Line import *
from Circle import *
from Shape import *
from Achievement import *

import FrameSetUp
import constants as c 

"""
Series of functions to deal with mouseEvents

"""

THINLINE = 1
THICKLINE = 3

# function to deal with user clicking.
def click_handler(event):
    if (not event.inaxes):
        return
    
    global shapeList,currentPoint,currentShape,mouseDown,movePoint,selectedShape

    currentPoint = Point(event.xdata, event.ydata)

    mouseDown = True

    # removes option to save shape
    if (toolMode != c.SELECT):
        FrameSetUp.saveFigureButton.grid_forget()


    # checks if the point where the user clicked is a point in a shape
    for shape in shapeList:
        if shape.containsPoint(currentPoint):
            match toolMode:
                case c.MOVEPOINT:
                    currentShape = shape

                    if (type(currentShape) == Shape): 
                        currentShape.hideAngles(CANVAS)
                    currentShape.hideMetrics(CANVAS)

                    # sets the point to move as the exact point from the figure
                    movePoint = shape.getPoint(currentPoint)

                    return
                case c.MOVEOBJECT:
                    currentShape = shape
                    if (type(currentShape) == Shape): 
                        currentShape.hideAngles(CANVAS)
                    currentShape.hideMetrics(CANVAS)
                    return

                case c.DRAW:
                    point = shape.getPoint(currentPoint)
                    new = newBasicShape(point)

                    currentShape = newShape(shape, new)
                    
                    if (type(currentShape) == Shape): 
                        currentShape.hideAngles(CANVAS)
                    currentShape.hideMetrics(CANVAS)

                    return
                case c.DELETE:

                    shape.removeShape(CANVAS)
                    shapeList.remove(shape)

                    currentShape = None

                    # updates data display
                    FrameSetUp.dataDisplay.config(text="")
                    FrameSetUp.dataDisplay.update()

                    return
                
                case c.SELECT:
                    if (selectedShape != None):
                        selectedShape.removeShape(CANVAS)
                        selectedShape.plotShape(PLOT, CANVAS, THINLINE)

                    selectedShape = shape
                    #plots selected shape w a thick line
                    shape.removeShape(CANVAS)
                    shape.plotShape(PLOT, CANVAS,THICKLINE)

                    FrameSetUp.saveFigureButton.grid(row=6, column=3,padx=FrameSetUp.PADX,pady=FrameSetUp.PADY)

                    # updates data display
                    FrameSetUp.dataDisplay.config(text=shape.measure())
                    FrameSetUp.dataDisplay.update()

                    return

    # if the user is clicking on a clear space of the CANVAS
    if (toolMode == c.DRAW):
        currentShape = newBasicShape(currentPoint)

        # updates data display
        FrameSetUp.dataDisplay.config(text=currentShape.measure())
        FrameSetUp.dataDisplay.update()
    else:
        currentShape = None    

def drag_handler(event):
    global shapeType,currentShape,currentPoint,shapeList,toolMode,movePoint

    if not event.inaxes or not mouseDown or currentShape == None:
        return
    
    lastPoint = currentPoint.copy()
    currentPoint = Point(event.xdata,event.ydata)

    match toolMode:
        case c.DRAW:
            # if the user is trying to draw a point but drags instead, creates a line
            if shapeType == c.POINT:
                currentShape.removeShape(CANVAS)
                if (currentShape in shapeList):
                    shapeList.remove(currentShape)
                FrameSetUp.changeShape(c.LINE)
                FrameSetUp.changeButtonColor(FrameSetUp.lineButton)
                currentShape = newBasicShape(startPoint=currentPoint)
            else:
                currentShape.removeShape(CANVAS)
                currentShape.setEndPoint(currentPoint)
                currentShape.plotShape(PLOT,CANVAS,THINLINE)

        case c.MOVEPOINT:
            currentShape.removeShape(CANVAS)

            currentShape.movePoint(movePoint, currentPoint)
            movePoint = currentPoint #cmovepoint represents the point that will be moving/moved

            currentShape.plotShape(PLOT, CANVAS, THINLINE)

        # moves the entire shape
        case c.MOVEOBJECT:
            currentShape.removeShape(CANVAS)
            deltaX = currentPoint.getX() - lastPoint.getX()
            deltaY = currentPoint.getY() - lastPoint.getY()
            currentShape.moveShape(deltaX, deltaY)
            currentShape.plotShape(PLOT, CANVAS, THINLINE)

def unclick_handler(event):
    global currentPoint,currentShape,mouseDown,toolMode
    mouseDown = False

    currentPoint = Point(event.xdata,event.ydata)

    if currentShape == None:
        return
    
    # updates data display
    FrameSetUp.dataDisplay.config(text=currentShape.measure())
    FrameSetUp.dataDisplay.update()
            
    if (toolMode == c.DRAW or toolMode == c.MOVEPOINT or toolMode == c.MOVEOBJECT):
        if (toolMode == c.DRAW):
            # checks if the user is connecting a figure back to itself and cleans up point location
            if currentShape.containsPoint(currentPoint):
                currentShape.setEndPoint(currentShape.getPoint(currentPoint))

                # plots the "snapped" position
                currentShape.removeShape(CANVAS)
                currentShape.plotShape(PLOT, CANVAS,THINLINE)

        # checks if user is connecting the figure to another figure
        for shape in shapeList:
            if (shape != currentShape):
                # checks if two shapes are being combined
                if shape.containsPoint(currentPoint):
                    currentShape.setEndPoint(shape.getPoint(currentPoint))

                    currentShape = newShape(currentShape, shape)

                    # updates data display
                    FrameSetUp.dataDisplay.config(text=currentShape.measure())
                    FrameSetUp.dataDisplay.update()
                
                # changes lines to thin for all other shapes
                currentShape.removeShape(CANVAS)
                currentShape.plotShape(PLOT, CANVAS,THINLINE)

    # ensures angles and metrics are shown that must be displayed
    if (type(currentShape) == Shape and FrameSetUp.showAnglesButton.cget("text") == "Hide Angles"):
        currentShape.showAngles(PLOT,CANVAS)
    if (currentShape != None and FrameSetUp.showMetricsButton.cget("text") == "Hide Metrics"):
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
    global shapeType,shapeList

    # creates a new point
    if (shapeType == c.POINT):

        # achievement for creating a point
        if (ACHIEVEMENTSDICT["createPoint"].isComplete() == False and MAIN.achievementsOn):
            ACHIEVEMENTSDICT["createPoint"].showAchievement()

        shape =startPoint.copy()
        shape.plotShape(PLOT,CANVAS,THINLINE)
        shapeList.append(shape)
    else:
        # creates lines and circles
        shape = Line() if shapeType == c.LINE else Circle()
        shape.setStartPoint(startPoint)
        shape.setEndPoint(startPoint)
        shapeList.append(shape)

    return shape

# creates a new Shape type shape with two Shape objects
def newShape(oldShape, newShape):
    global shapeList
    # create Angle achievement
    if (ACHIEVEMENTSDICT["createAngle"].isComplete() == False and type(newShape) == Line and type(oldShape) == Line and MAIN.achievementsOn):
        ACHIEVEMENTSDICT["createAngle"].showAchievement()

    numComponents = oldShape.getNumComponents() + newShape.getNumComponents()
    shapes = [oldShape,newShape]

    #removes old shapes from shape list
    if (newShape in shapeList):
        shapeList.remove(newShape)
    if (oldShape in shapeList):
        shapeList.remove(oldShape)

    # gathers all arcplots
    arcPlots = []
    if (type(newShape) == Shape):
        arcPlots.extend(newShape.getArcPlotLists())
    if (type(oldShape) == Shape):
        arcPlots.extend(oldShape.getArcPlotLists())

    # creates new shape object
    newlyCreatedShape = Shape(shapes, numComponents, arcPlots)
    shapeList.append(newlyCreatedShape)
    return newlyCreatedShape

# class variables
currentShape = None
currentPoint = None
mouseDown = False
shapeType = c.POINT
shapeList = [] 
toolMode = c.DRAW
movePoint = None
selectedShape = None

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
    ACHIEVEMENTSDICT = c.ACHIEVEMENTSDICT

    MAIN = Main

    CANVAS.mpl_connect("button_press_event", click_handler)
    CANVAS.mpl_connect("motion_notify_event", drag_handler)
    CANVAS.mpl_connect("button_release_event", unclick_handler)


