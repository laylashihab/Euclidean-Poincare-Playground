from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from Point import *
from Line import *
from Circle import *
from Shape import *
from Achievement import *

"""
Series of functions to deal with mouseEvents

"""
# function to deal with user clicking.
def click_handler(event):
    if (not event.inaxes):
        return
    
    global mouseDown
    global currentShape
    global movePoint
    global currentPoint
    currentPoint = Point(event.xdata, event.ydata)
    mouseDown = True

    # checks if the point where the user clicked is a point in a shape
    for shape in shapeList:
        if shape.containsPoint(currentPoint):
            if toolMode == "Move":
                # sets the point to move as the shape's point
                movePoint = currentPoint
                currentShape = shape
            elif toolMode == "Draw":
                # sets the currentPoint to the point the user is clicking on
                currentPoint = shape.getPoint(currentPoint)
                currentShape = newShape(currentPoint)
                numComponents = 1 + shape.getNumComponents()
                shapes = [shape, currentShape]
                shapeList.remove(shape)
                currentShape = Shape(shapes, numComponents)
                shapeList.append(currentShape)
                return
            elif toolMode == "Delete":
                shape.removeShape(canvas)
                shapeList.remove(shape)
                dataDisplay.config(text="")
                dataDisplay.update()
                return
            elif toolMode == "Select":
                currentShape = shape   

        dataDisplay.config(text=currentShape.measure())
        dataDisplay.update()
         
    if (toolMode == "Draw"):
        currentShape = newShape(currentPoint)

def drag_handler(event):
    if event.inaxes and mouseDown:
        global movePoint
        global currentShape
        global currentPoint
        lastPoint = currentPoint.copy()
        currentPoint = Point(event.xdata,event.ydata)

        if toolMode == "Draw":
            if (shapeType == "Point"):
                currentShape = newShape(currentPoint)
            currentShape.draw(plot1,canvas,currentPoint)

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
    if (toolMode == "Draw" or toolMode == "Move" or toolMode == "Select"):
        if (type(currentShape) != Point):
            for shape in shapeList:
                if (shape != currentShape and type(shape) != Point and shape.containsPoint(currentPoint)):
                    currentShape.setEndPoint(shape.getPoint(currentPoint))
                    shapeList.remove(shape)
                    shapes = [shape, currentShape]
                    currentShape = Shape(shapes, shape.getNumComponents() + currentShape.getNumComponents())
                    shapeList.append(currentShape)

                    #redraw figures so they connect smoothly at point
                    currentShape.removeShape(canvas)
                    currentShape.plotShape(plot1, canvas)

                    # updates data display
                    dataDisplay.config(text=currentShape.measure())
                    dataDisplay.update()

# changes type of shape plot
def changeShape(newShape):
    global shapeType
    global toolMode
    shapeType = newShape
    toolMode = "Draw"

# initializes a new shape
def newShape(currentPoint):
    if (shapeType == "Point"):
        if (createPoint.isComplete() == False):
            createPoint.showAchievement()
            pointButton.grid(row=1,column=0, padx=padx, pady=pady)

        shape =currentPoint.copy()
        shape.plotShape(plot1,canvas)
        shapeList.append(shape)
    else:
        shape = Line() if shapeType == "Line" else Circle()
        shape.setStartPoint(currentPoint)
        shape.setEndPoint(currentPoint)
        shapeList.append(shape)
    return shape
    
def changeToolMode(newTool):
    global toolMode
    toolMode = newTool

# clears the plot
def clear():
    global shapeList
    shapeList = []
    plot1.cla()
    plot1.set_xlim(0,plot_size)
    plot1.set_ylim(0,plot_size)
    plot1.set_axis_off()
    canvas.draw()


# variables
startPoint = [0,0]
shapeType = "Point" #Line or Circle or Point
toolMode = "Draw" #Draw (when creating new lines or circles) or Delete or Move
plot_size = 400
currentShape = None
currentPoint = None
movePoint = None
mouseDown = False
Point.setEpsilon(20)

# achievements
"""
All definitions come from a translation of Euclid's Elements
source:
http://aleph0.clarku.edu/~djoyce/elements/bookI/bookI.html
"""
createPoint = Achievement("Define a Point", "A point is that which has no part.")
createLine = Achievement("Define a Line", "A line is breadthless length.\nThe ends of a line are points.\nA straight line is a line which lies evenly with the points on itself.")


# store various graph objects
shapeList = [] 

# frame/window settings
padx = 10
pady = 5

# the figure that will contain the plot
fig = Figure(figsize = (5, 5), dpi = 100, constrained_layout=True)

#main window setup
root = Tk()
root.geometry("600x700")
root.title('Euclidean Playground')

# description setup
descriptLabel = Label(root, text="You have been given a straightedge and a compass")
descriptLabel.pack()

# tool setup
toolbar = Frame(root)
toolLabel = Label(toolbar, text="Toolbar")
shapeLabel = Label(toolbar, text="Shape Library")
operationLabel = Label(toolbar, text="Operations")
pointButton = Button(toolbar, command=lambda: changeShape("Point"), height = 2, width = 10, text = "Point")
lineButton = Button(toolbar, command=lambda: changeShape("Line"), height = 2, width = 10, text = "Line")
circleButton = Button(toolbar, command =lambda: changeShape("Circle"), height = 2, width = 10, text = "Circle")
clearButton = Button(toolbar,command=clear,height = 2, width = 10, text = "Clear")
moveButton = Button(toolbar,command =lambda: changeToolMode("Move"),height = 2, width = 10, text = "Move Point")
deleteButton = Button(toolbar,command =lambda: changeToolMode("Delete"),height = 2, width = 10, text = "Delete Object")
selectButton = Button(toolbar,command =lambda: changeToolMode("Select"),height = 2, width = 10, text = "Select Object")

row = 0
# increments row and returns new incremented val
def rowplus():
    global row
    row = row + 1
    return row
toolLabel.grid(row=row, column=1, padx=padx, pady=pady)
shapeLabel.grid(row=rowplus(), column=1, padx=padx, pady=pady)

row = 1
lineButton.grid(row=row,column=1, padx=padx, pady=pady)
circleButton.grid(row=row,column=2, padx=padx, pady=pady)

operationLabel.grid(row=rowplus(), column = 1, padx=padx, pady=pady)
clearButton.grid(row=rowplus(),column=0, padx=padx, pady=pady)
moveButton.grid(row=row,column=1, padx=padx, pady=pady)
deleteButton.grid(row=row,column=2, padx=padx, pady=pady)
selectButton.grid(row=row, column = 3, padx=padx, pady=pady)
toolbar.pack()


# creating the Tkinter canvas containing the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master = root)  
canvas.get_tk_widget().config(width=plot_size,height=plot_size)
canvas.draw()

# placing the canvas on the Tkinter window
canvas.get_tk_widget().pack()

# adding the subplot
plot1 = fig.add_subplot(111)
plot1.set_xlim(0,plot_size)
plot1.set_ylim(0,plot_size)
plot1.set_axis_off()

# creating the Matplotlib toolbar
tb = NavigationToolbar2Tk(canvas, root)
tb.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack()

# data display setup
dataDisplay = Label(root, text="")
dataDisplay.pack()

# bindings
canvas.mpl_connect("button_press_event", click_handler)
canvas.mpl_connect("motion_notify_event", drag_handler)
canvas.mpl_connect("button_release_event", unclick_handler)

root.mainloop()
