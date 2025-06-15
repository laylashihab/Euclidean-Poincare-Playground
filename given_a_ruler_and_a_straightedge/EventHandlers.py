from Point import *
from Line import *
from Circle import *
from Shape import *
from Achievement import *

import FrameSetUp

"""
Series of functions to deal with mouseEvents

"""
# function to deal with user clicking.
def click_handler(event):
    if (not event.inaxes):
        return
    
    global shapeList
    global foundPoint
    global currentPoint
    global currentShape
    global mouseDown
    global movePoint
    currentPoint = Point(event.xdata, event.ydata)
    foundPoint = False

    mouseDown = True

    print(shapeList)

    # checks if the point where the user clicked is a point in a shape
    for shape in shapeList:
        if shape.containsPoint(currentPoint):
            foundPoint = True
            if toolMode == "Move":
                # sets the point to move as the point the user is clikcing on
                movePoint = currentPoint
                currentShape = shape
            elif toolMode == "Draw":
                # creates a compound shape in the Shape class with the shape the user clicked on and their new drawing
                currentPoint = shape.getPoint(currentPoint)
                currentShape = newShape(currentPoint)
                numComponents = 1 + shape.getNumComponents()
                shapes = [shape, currentShape]
                shapeList.remove(shape)
                shapeList.remove(currentShape)
                # gathers all arcplots
                arcPlots = []
                if (type(shape) == Shape):
                    arcPlots.extend(shape.getArcPlotLists())
                if (type(currentShape) == Shape):
                    arcPlots.extend(currentShape.getArcPlotLists())
                currentShape = Shape(shapes, numComponents, arcPlots)
                shapeList.append(currentShape)
                return
            elif toolMode == "Delete":
                shape.removeShape(canvas)
                shapeList.remove(shape)
            elif toolMode == "Select":
                currentShape = shape   
         
    # if the user is clicking on a clear space of the canvas
    if (foundPoint == False):
        if (toolMode == "Draw"):
            currentShape = newShape(currentPoint)
            dataDisplay.config(text=currentShape.measure())
            dataDisplay.update()
        else:
            currentShape = None    

def drag_handler(event):
    if event.inaxes and mouseDown:
        global shapeType
        global movePoint
        global currentShape
        global currentPoint
        global shapeList
        global toolMode
        lastPoint = currentPoint.copy()
        currentPoint = Point(event.xdata,event.ydata)

        if currentShape == None:
            return

        # Create Line achievement
        if (createLine.isComplete() == False and achievementsOn):
            createLine.showAchievement()
            FrameSetUp.lineButton.grid(row=2,column=1, padx=padx, pady=pady)

        if toolMode == "Draw":
            # if the user is trying to draw a point but drags instead, creates a line
            if shapeType == "Point":
                currentShape.removeShape(canvas)
                if (currentShape in shapeList):
                    shapeList.remove(currentShape)
                FrameSetUp.changeShape("Line")
                FrameSetUp.changeButtonColor(FrameSetUp.lineButton)
                currentShape = newShape(startPoint=currentPoint)

            currentShape.draw(plot1,canvas,endPoint=currentPoint)

            # updates data display
            dataDisplay.config(text=currentShape.measure())
            dataDisplay.update()

        elif toolMode == "Move":
            # removes the current drawing of the line
            currentShape.removeShape(canvas)

            # moves the point to the current point
            currentShape.movePoint(movePoint, currentPoint)
            movePoint = currentPoint
            currentShape.plotShape(plot1, canvas)

            # updates data display
            dataDisplay.config(text=currentShape.measure())
            dataDisplay.update()
        # moves the entire shape
        elif (toolMode == "Select"):
            currentShape.removeShape(canvas)
            deltaX = currentPoint.getX() - lastPoint.getX()
            deltaY = currentPoint.getY() - lastPoint.getY()
            currentShape.moveShape(deltaX, deltaY)
            currentShape.plotShape(plot1, canvas)

            # updates data display
            dataDisplay.config(text=currentShape.measure())
            dataDisplay.update()

def unclick_handler(event):
    # checks if the user is connecting two shapes
    global currentPoint
    global currentShape
    global mouseDown
    mouseDown = False

    currentPoint = Point(event.xdata,event.ydata)
    # checks if the user is connecting up a figure
    if (toolMode == "Draw" or toolMode == "Move" or toolMode == "Select"):
        if (type(currentShape) != Point):
            for shape in shapeList:
                if (shape != currentShape and type(shape) != Point and shape.containsPoint(currentPoint)):
                    currentShape.setEndPoint(shape.getPoint(currentPoint))
                    shapeList.remove(shape)
                    shapeList.remove(currentShape)
                    shapes = [shape, currentShape]
                    arcPlots = []
                    if (type(shape) == Shape):
                        arcPlots.extend(shape.getArcPlotLists())
                    if (type(currentShape) == Shape):
                        arcPlots.extend(currentShape.getArcPlotLists())
                    currentShape = Shape(shapes, shape.getNumComponents() + currentShape.getNumComponents(), arcPlots)
                    shapeList.append(currentShape)

                    #redraw figures so they connect smoothly at point
                    currentShape.removeShape(canvas)
                    currentShape.plotShape(plot1, canvas)

                    # updates data display
                    dataDisplay.config(text=currentShape.measure())
                    dataDisplay.update()


# initializes a new shape
def newShape(startPoint):
    global canvas
    global plot1
    global padx
    global pady
    global achievementsOn
    global createPoint

    # creates a new point
    if (shapeType == "Point"):

        # achievement for creating a line
        if (createPoint.isComplete() == False and achievementsOn):
            createPoint.showAchievement()
            FrameSetUp.pointButton.grid(row=2,column=0, padx=padx, pady=pady)

        shape =startPoint.copy()
        shape.plotShape(plot1,canvas)
        shapeList.append(shape)
    else:
        # creates lines and circles
        shape = Line() if shapeType == "Line" else Circle()
        shape.setStartPoint(startPoint)
        shape.setEndPoint(startPoint)
        shapeList.append(shape)
    return shape

currentShape = None
currentPoint = None
movePoint = None
mouseDown = False
shapeType = "Point"
shapeList = [] 
toolMode = "Draw"
canvas = None
dataDisplay = None
plot1 = None
padx = None
pady = None
achievementsOn = None
createLine = None
createPoint = None



# bindings
def bindEvents(Main):
    global canvas
    global dataDisplay
    global plot1
    global createLine
    global createPoint
    global padx
    global pady
    global achievementsOn
    
    canvas = Main.canvas
    dataDisplay = Main.dataDisplay
    plot1 = Main.plot1
    createLine = Main.createLine
    createPoint = Main.createPoint
    padx = Main.padx
    pady = Main.pady
    achievementsOn = Main.achievementsOn


    Main.canvas.mpl_connect("button_press_event", click_handler)
    Main.canvas.mpl_connect("motion_notify_event", drag_handler)
    Main.canvas.mpl_connect("button_release_event", unclick_handler)


