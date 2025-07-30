import Point
import Line
from Circle import *
from Shape import *
from Achievement import *

import FrameSetUp
import constants as c 

"""
Series of functions to deal with mouseEvents

"""


# function to deal with user clicking.
def click_handler(event):
    if (not event.inaxes):
        return
    # ensures that the user isn't clicking outside the circle
    if poincareMode == True and (event.xdata**2 + event.ydata** 2 > 1):
        return

    global shapeList,currentPoint,currentShape,mouseDown,movePoint,selectedShape

    currentPoint =Point.Point(event.xdata, event.ydata)
    
    mouseDown = True

    # checks if the point where the user clicked is a point in a shape
    for shape in shapeList:
        if shape.containsPoint(currentPoint):
            match toolMode:
                case c.MOVEPOINT:
                    currentShape = shape

                    if (type(currentShape) == Shape): 
                        currentShape.hideAngles()
                    currentShape.hideMetrics()
                    
                    CANVAS.draw()

                    # sets the point to move as the exact point from the figure
                    movePoint = shape.getPoint(currentPoint)

                    return
                case c.MOVEOBJECT:
                    currentShape = shape
                    if (type(currentShape) == Shape): 
                        currentShape.hideAngles()
                    currentShape.hideMetrics()
                    CANVAS.draw()
                    return

                case c.DRAW:
                    # if drawing from a point, remove the point since the endpoint of the new shape will replace it

                    point = shape.getPoint(currentPoint)
                    new = newBasicShape(point)
                    
                    # if its a point, remove the point from the actual shape (reduces clutter)
                    if type(shape) == Point:
                        shapeList.remove(shape)
                        shape.removeShape()
                        currentShape = new
                    else:
                        shape.removeShape()
                        currentShape = newShape(shape, new)
                    
                    # hides angles and metrics
                    if (type(currentShape) == Shape): 
                        currentShape.hideAngles()
                    currentShape.hideMetrics()

                    currentShape.plotShape(PLOT, poincare=poincareMode)
                    CANVAS.draw()

                    return
                case c.DELETE:
                    shape.removeShape()
                    CANVAS.draw()
                    shapeList.remove(shape)

                    currentShape = None

                    # updates data display
                    updateDataDisplay()
                    
                    return
                
                case c.SELECT:
                    if (selectedShape != None):
                        selectedShape.removeShape()
                        selectedShape.plotShape(PLOT, poincare=poincareMode)

                    selectedShape = shape
                    
                    #plots selected shape w a thick line
                    shape.removeShape()
                    shape.plotShape(PLOT,c.THICKLINE,poincare=poincareMode)
                    CANVAS.draw()

                    FrameSetUp.saveFigure(shape)

                    return
                case c.SCALE:
                    # ensures any previously selected shape is plotted with thin lines
                    if currentShape != None:
                        currentShape.removeShape()
                        currentShape.plotShape(PLOT, poincare=poincareMode)
                        CANVAS.draw()

                        
                    currentShape = shape

                    # ensures the new selection is plotted with thick lines
                    if currentShape != None:
                        currentShape.removeShape()
                        currentShape.plotShape(PLOT,linewidth=c.THICKLINE, poincare=poincareMode)
                        CANVAS.draw()

                    return
                
    # if the user is clicking on a clear space of the CANVAS
    if (toolMode == c.DRAW):
        currentShape = newBasicShape(currentPoint)
    else:
        currentShape = None

def drag_handler(event):
    global shapeType,currentShape,currentPoint,shapeList,toolMode,movePoint

    if not event.inaxes or not mouseDown or currentShape == None:
        return
    
    # ensures that the user isn't clicking outside the circle
    if poincareMode == True and (event.xdata**2 + event.ydata** 2 > 1):
        return

    lastPoint = copy.deepcopy(currentPoint)
    currentPoint =Point.Point(event.xdata, event.ydata)

    match toolMode:
        case c.DRAW:
            # if the user is trying to draw a point but drags instead, creates a line
            if type(currentShape) == Point.Point:
                currentShape.removeShape()
                if currentShape in shapeList:
                    shapeList.remove(currentShape)
                FrameSetUp.changeShape(c.LINE)
                FrameSetUp.changeButtonColor(FrameSetUp.lineButton)
                currentShape = newBasicShape(startPoint=currentPoint)
            else:
                currentShape.removeShape()
                currentShape.setEndPoint(currentPoint)
                currentShape.plotShape(PLOT, poincare=poincareMode)
            CANVAS.draw()

        case c.MOVEPOINT:
            currentShape.removeShape()

            currentShape.movePoint(pointToMove=movePoint, newPoint=currentPoint)
            movePoint = currentPoint #movepoint represents the point that will be moving/moved

            currentShape.plotShape(PLOT, poincare=poincareMode)

            CANVAS.draw()

        # moves the entire shape
        case c.MOVEOBJECT:
            deltaX = currentPoint.getX() - lastPoint.getX()
            deltaY = currentPoint.getY() - lastPoint.getY()
            currentShape.moveShape(deltaX, deltaY)
            currentShape.removeShape()
            currentShape.plotShape(PLOT, poincare=poincareMode)
            CANVAS.draw()

def unclick_handler(event):
    global currentPoint,currentShape,mouseDown,toolMode,shapeType
    mouseDown = False

    if not event.inaxes or currentShape == None:
        return
    
    currentPoint =Point.Point(event.xdata, event.ydata)

    if (toolMode != c.SELECT and toolMode != c.SCALE):
        # checks if user is connecting the figure to another figure
        for shape in shapeList:
            # changes the last component of the shape to the currentPoint
            if type(currentShape) == Shape:
                currentShape.setLastComponent(currentPoint)

            if (shape != currentShape):
                # checks if two different shapes are being combined
                if shape.containsPoint(currentPoint):
                    point = shape.getPoint(currentPoint)
                    deltaX = currentShape.getEndPoint().getX()-point.getX()
                    deltaY = currentShape.getEndPoint().getY()-point.getY()
                    shape.moveShape(deltaX,deltaY)
                    currentShape = newShape(currentShape, shape)

                    # plots the "snapped" position
                    currentShape.removeShape()
                    currentShape.plotShape(PLOT, poincare=poincareMode)

                    break
            else:
                # checks if a shape is being attached to itself
                if (currentShape.containsPoint(currentPoint)):
                    currentShape.setEndPoint(currentShape.getPoint(currentPoint))
                    # plots the "snapped" position
                    currentShape.removeShape()
                    currentShape.plotShape(PLOT, poincare=poincareMode)

                    break

    # if a line was drawn with no length, replaces it with a point
    if type(currentShape) == Line and currentShape.getLength() == 0:
        point = currentShape.getEndPoint()
        shapeList.append(point)
        shapeList.remove(currentShape)
        currentShape.removeShape()
        point.plotShape(PLOT)
        FrameSetUp.changeShape(c.POINT)
        currentShape = point

    # ensures angles and metrics are shown that must be displayed
    if (type(currentShape) == Shape and FrameSetUp.showAnglesButton.cget("text") == "Hide Angles"):
        currentShape.showAngles(PLOT)
    if (currentShape != None and FrameSetUp.showMetricsButton.cget("text") == "Hide Metrics"):
        currentShape.showMetrics(PLOT)

    # updates the canvas
    CANVAS.draw()
    # updates data display
    updateDataDisplay()

    # achievements for creating a circle or line
    if (MAIN.achievementsOn and c.ACHIEVEMENTSDICT["createCircle"].isComplete() == False and type(currentShape) == Circle):
        c.ACHIEVEMENTSDICT["createCircle"].showAchievement()
    elif (MAIN.achievementsOn and c.ACHIEVEMENTSDICT["createLine"].isComplete() == False and type(currentShape) == Line):
        c.ACHIEVEMENTSDICT["createLine"].showAchievement()

    # various types of angle achievements
    if MAIN.achievementsOn and type(currentShape) == Shape:
        if (c.ACHIEVEMENTSDICT["createAcuteAngle"].isComplete() == False or c.ACHIEVEMENTSDICT["createObtuseAngle"].isComplete() == False 
            or c.ACHIEVEMENTSDICT["createRightAngle"].isComplete() == False):
            angles = currentShape.showAngles(PLOT)
            currentShape.hideAngles()
            for angle in angles:
                if c.ACHIEVEMENTSDICT["createAcuteAngle"].isComplete() == False and angle < 90:
                    c.ACHIEVEMENTSDICT["createAcuteAngle"].showAchievement()
                elif c.ACHIEVEMENTSDICT["createRightAngle"].isComplete() == False and angle == 90:
                    c.ACHIEVEMENTSDICT["createRightAngle"].showAchievement()
                elif c.ACHIEVEMENTSDICT["createObtuseAngle"].isComplete() == False and angle > 90:
                    c.ACHIEVEMENTSDICT["createObtuseAngle"].showAchievement()

def clearCurrentShape():
    global currentShape
    currentShape = None

def slider_click(event):
    if currentShape == None:
        return 
    
    # makes the current shape bold
    currentShape.removeShape()
    currentShape.plotShape(PLOT,linewidth=c.THICKLINE,poincare=poincareMode)
    CANVAS.draw()

    # turns off metrics and angles
    currentShape.hideMetrics()
    if type(currentShape) == Shape:
        currentShape.hideAngles()

def slider_drag(event):
    if currentShape == None:
        return 

    if (type(currentShape) != Point):
        value = FrameSetUp.scaleSlider.get()
        value = float(value) / 100
        currentShape.scale(value, PLOT, poincare=poincareMode)
        CANVAS.draw()

def slider_unclick(event):

    if currentShape == None:
        # ensures the scale slider is hidden
        FrameSetUp.scaleSlider.set(100)

        return 
    
    scaleVal = float(FrameSetUp.scaleSlider.get()) / 100
    currentShape.confirmScaleSize(scaleVal,PLOT, poincare=poincareMode)
    
    CANVAS.draw()

    # ensures the scale slider is hidden
    FrameSetUp.scaleSlider.set(100)

    # ensures angles and metrics are shown that must be displayed
    if (type(currentShape) == Shape and FrameSetUp.showAnglesButton.cget("text") == "Hide Angles"):
        currentShape.showAngles(PLOT)
    if (currentShape != None and FrameSetUp.showMetricsButton.cget("text") == "Hide Metrics"):
        currentShape.showMetrics(PLOT)

    # updates the canvas
    CANVAS.draw()

def updateDataDisplay():
    if (poincareMode == True):
        return
    if currentShape == None:
        FrameSetUp.dataDisplay.config(text="")
        FrameSetUp.dataDisplay.update()
    else:
        FrameSetUp.dataDisplay.config(text=currentShape.measure())
        FrameSetUp.dataDisplay.update()



# initializes a new Basic shape (Point, Line, Circle)
# for points, creates a new point object
# for lines and circles, sets the endpoint and startpoint to the given start point 
def newBasicShape(startPoint):
    global shapeType,shapeList

    # creates a new point
    if (shapeType == c.POINT):

        # achievement for creating a point
        if (c.ACHIEVEMENTSDICT["createPoint"].isComplete() == False and MAIN.achievementsOn):
            c.ACHIEVEMENTSDICT["createPoint"].showAchievement()

        shape = copy.deepcopy(startPoint)
        shape.plotShape(PLOT, poincare=poincareMode)
        shapeList.append(shape)
    else:
        # creates lines and circles
        shape = Line(poincareMode) if shapeType == c.LINE else Circle(poincareMode)
        shape.setStartPoint(startPoint)
        shape.setEndPoint(startPoint)
        shapeList.append(shape)

    return shape

# creates a new Shape type shape with two Shape objects
def newShape(oldShape, newShape):
    global shapeList
    # create Angle achievement
    if (c.ACHIEVEMENTSDICT["createAngle"].isComplete() == False and type(newShape) == Line and type(oldShape) == Line and MAIN.achievementsOn):
        c.ACHIEVEMENTSDICT["createAngle"].showAchievement()

    # checks if a shape is a point
    if type(oldShape) == Point.Point:
        shapeList.remove(oldShape)
        oldShape.removeShape()
        return newShape
    elif type(newShape) == Point.Point:
        shapeList.remove(newShape)
        newShape.removeShape()
        return oldShape
    
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
    newlyCreatedShape = Shape(oldShape,newShape, arcPlots)
    shapeList.append(newlyCreatedShape)
    return newlyCreatedShape

def zoom_drag(event):
    global xBoundDelta, yBoundDelta,plotBounds
    scaleVal = 100 / FrameSetUp.zoomSlider.get() 
    if poincareMode == False:
        plotBounds = c.PLOTBOUNDS * scaleVal
        PLOT.set_xlim(- plotBounds + xBoundDelta,plotBounds + xBoundDelta)
        PLOT.set_ylim(- plotBounds + yBoundDelta,plotBounds + yBoundDelta)
    else:
        PLOT.set_xlim(- scaleVal,scaleVal)
        PLOT.set_ylim(- scaleVal,scaleVal)
    CANVAS.draw()

def move_left(event):
    global xBoundDelta
    scaleVal = 100 / FrameSetUp.zoomSlider.get() 
    scaleVal *= c.EUCLIDEANSCALER

    if poincareMode == False:
        xBoundDelta -= scaleVal
        PLOT.set_xlim(- plotBounds + xBoundDelta,plotBounds + xBoundDelta)
    else:
        for shape in shapeList:
            shape.removeShape()
            shape.moveShapePoincare(deltaX=c.POINCAREDELTA)
            shape.plotShapePoincare(PLOT)
    CANVAS.draw()

def move_right(event):
    global xBoundDelta
    scaleVal = 100 / FrameSetUp.zoomSlider.get() 
    scaleVal *= c.EUCLIDEANSCALER

    if poincareMode == False:
        xBoundDelta += scaleVal
        PLOT.set_xlim(- plotBounds + xBoundDelta,plotBounds + xBoundDelta)
    else:
        for shape in shapeList:
            shape.removeShape()
            shape.moveShapePoincare(deltaX=-c.POINCAREDELTA)
            shape.plotShapePoincare(PLOT)

    CANVAS.draw()

def move_up(event):
    global yBoundDelta
    scaleVal = 100 / FrameSetUp.zoomSlider.get() 
    scaleVal *= c.EUCLIDEANSCALER

    if poincareMode == False:
        yBoundDelta += scaleVal
        PLOT.set_ylim(- plotBounds + yBoundDelta,plotBounds + yBoundDelta)
    else:
        for shape in shapeList:
            shape.removeShape()
            shape.moveShapePoincare(deltaY=-c.POINCAREDELTA)
            shape.plotShapePoincare(PLOT)

    CANVAS.draw()

def move_down(event):
    global yBoundDelta
    scaleVal = 100 / FrameSetUp.zoomSlider.get() 
    scaleVal *= c.EUCLIDEANSCALER

    if poincareMode == False:
        yBoundDelta -= scaleVal
        PLOT.set_ylim(- plotBounds + yBoundDelta,plotBounds + yBoundDelta)
    else:
        for shape in shapeList:
            shape.removeShape()
            shape.moveShapePoincare(deltaY=c.POINCAREDELTA)
            shape.plotShapePoincare(PLOT)

    CANVAS.draw()

# class variables
currentShape = None
currentPoint = None
mouseDown = False
shapeType = c.POINT
shapeList = [] 
toolMode = c.DRAW
movePoint = None
selectedShape = None
poincareMode = False
plotBounds = c.PLOTBOUNDS
xBoundDelta = 0
yBoundDelta = 0

# constant variables to set from Main
CANVAS = None
PLOT = None
MAIN = None

# sets up bindings with CANVAS
def bindEvents(Main):
    global CANVAS, PLOT, MAIN
    
    CANVAS = FrameSetUp.CANVAS
    PLOT = FrameSetUp.PLOT
    MAIN = Main

    CANVAS.mpl_connect("button_press_event", click_handler)
    CANVAS.mpl_connect("motion_notify_event", drag_handler)
    CANVAS.mpl_connect("button_release_event", unclick_handler)

    # binds scale slider to event functions
    FrameSetUp.scaleSlider.bind("<Button-1>", slider_click)
    FrameSetUp.scaleSlider.bind("<B1-Motion>", slider_drag)
    FrameSetUp.scaleSlider.bind("<ButtonRelease-1>", slider_unclick)

    # binds zoom slider to event functions
    FrameSetUp.zoomSlider.bind("<B1-Motion>", zoom_drag)

    # arrow keys
    FrameSetUp.ROOT.bind("<Left>", move_left)
    FrameSetUp.ROOT.bind("<Right>", move_right)
    FrameSetUp.ROOT.bind("<Up>", move_up)
    FrameSetUp.ROOT.bind("<Down>", move_down)



