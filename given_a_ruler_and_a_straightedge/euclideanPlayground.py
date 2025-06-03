from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from Point import *
from Line import *
from Circle import *

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
    currentPoint = Point(event.xdata, event.ydata)
    mouseDown = True

    for shape in shapeList:
        if shape.containsPoint(currentPoint):
            movePoint = currentPoint
            currentShape = shape
            return

    currentShape = Line() if mode == "Line" else Circle()
    currentShape.setStartPoint(currentPoint)
    shapeList.append(currentShape)

def drag_handler(event):
    if event.inaxes and mouseDown:
        global movePoint
        global currentShape
        currentPoint = Point(event.xdata,event.ydata)

        if (movePoint != None):
            movePoint = currentPoint

        #removes the current drawing of the line
        currentShape.removeShape(canvas)
        currentShape.setEndPoint(currentPoint)
        currentShape.plotShape(plot1, canvas)

def unclick_handler(event):
    global mouseDown
    mouseDown = False

# changes type of shape plot
def changeMode(newMode):
    global mode
    mode = newMode

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
mode = "Line"
plot_size = 400
currentShape = None
movePoint = None
mouseDown = False
Point.setEpsilon(10)

# store various graph objects
shapeList = [] 

# the figure that will contain the plot
fig = Figure(figsize = (5, 5), dpi = 100, constrained_layout=True)

#main window setup
root = Tk()
root.geometry("500x500")
root.title('Euclidean Playground')

# description setup
descriptLabel = Label(root, text="You have been given a straightedge and a compass")
descriptLabel.pack()

# tool setup
toolLabel = Label(root, text="Tools:")
lineButton = Button(root, command=lambda: changeMode("Line"), height = 2, width = 10, text = "Line")
lineButton.pack()
circleButton = Button(root, command =lambda: changeMode("Circle"), height = 2, width = 10, text = "Circle")
circleButton.pack()
clearButton = Button(root,command=clear,height = 2, width = 10, text = "Clear")
clearButton.pack()

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
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack()

# bindings
canvas.mpl_connect("button_press_event", click_handler)
canvas.mpl_connect("motion_notify_event", drag_handler)
canvas.mpl_connect("button_release_event", unclick_handler)

root.mainloop()
