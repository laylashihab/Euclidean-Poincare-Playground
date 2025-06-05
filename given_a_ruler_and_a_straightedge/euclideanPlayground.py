from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from Point import *
from Line import *
from Circle import *
from Shape import *

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
                movePoint = currentPoint
                currentShape = shape
            elif toolMode == "Draw":
                currentPoint = shape.getEndPoint()
                currentShape = Line() if shapeType == "Line" else Circle()
                currentShape.setStartPoint(currentPoint)
                numComponents = 1 + shape.getNumComponents()
                shapes = [shape, currentShape]
                shapeList.remove(shape)
                currentShape = Shape(shapes, numComponents)
                shapeList.append(currentShape)
                return
            elif toolMode == "Delete":
                shape.removeShape(canvas)
                dataDisplay.config(text="")
                dataDisplay.update()
                return
            elif toolMode == "Select":
                currentShape = shape   

        dataDisplay.config(text=currentShape.measure())
        dataDisplay.update()
         
    if (toolMode == "Draw"):
        currentShape = Line() if shapeType == "Line" else Circle()
        currentShape.setStartPoint(currentPoint)
        shapeList.append(currentShape)

def drag_handler(event):
    if event.inaxes and mouseDown:
        global movePoint
        global currentShape
        global currentPoint
        lastPoint = currentPoint.copy()
        currentPoint = Point(event.xdata,event.ydata)
        if (movePoint != None):
            movePoint = currentPoint

        if (toolMode == "Draw" or toolMode == "Move"):
            # removes the current drawing of the line
            currentShape.removeShape(canvas)

            # moves the point to the current point
            currentShape.setEndPoint(currentPoint)
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
    global mouseDown
    mouseDown = False

# changes type of shape plot
def changeShape(newShape):
    global shapeType
    global toolMode
    shapeType = newShape
    toolMode = "Draw"

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
shapeType = "Line" #Line or Circle
toolMode = "Draw" #Draw (when creating new lines or circles) or Delete or Move
plot_size = 400
currentShape = None
currentPoint = None
movePoint = None
mouseDown = False
Point.setEpsilon(10)

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
lineButton.grid(row=rowplus(),column=0, padx=padx, pady=pady)
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
