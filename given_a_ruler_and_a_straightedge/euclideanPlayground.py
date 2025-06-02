from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.patches as patches
import math        


class Point:
    __x = 0
    __y = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
    
    def equals(self, otherPoint):
        if (otherPoint == None):
            return False
        elif (abs(self.__x - otherPoint.getX()) <= epsilon and abs(self.__y - otherPoint.getY()) <= epsilon):
            return True
        else:
            return False

class Line:
    __line = None
    __startPoint = None
    __endPoint = None

    __endPointPlot = None
    __startPointPlot = None
    

    def __init__(self):
        pointList[self] = []

    def plotShape(self):
        if self.__endPoint != None:
            x_data = np.linspace(self.__startPoint.getX(), self.__endPoint.getX(), 100)
            y_data = np.linspace(self.__startPoint.getY(), self.__endPoint.getY(),100)
            line, = plot1.plot(x_data,y_data)
            self.__line = line

            #plots endpoints
            self.__startPointPlot, = plot1.plot(self.__startPoint.getX(),self.__startPoint.getY(), "o")
            self.__endPointPlot, = plot1.plot(self.__endPoint.getX(),self.__endPoint.getY(), "o")
            canvas.draw()
    
    def removeShape(self):
        if self.__endPointPlot != None:
            # removes line and endPoint
            self.__line.remove()
            self.__startPointPlot.remove()
            self.__endPointPlot.remove()
            canvas.draw()

    def setStartPoint(self, startPoint):
        self.__startPoint = startPoint
        if (len(pointList[self]) == 0):
            pointList[self].append(self.__startPoint)
        else:
            pointList[self][0] = self.__startPoint

    def setEndPoint(self, endpoint):
        self.__endPoint = endpoint
        if (len(pointList[self]) == 1):
            pointList[self].append(self.__endPoint)
        else:
            pointList[self][1] = self.__endPoint
    
    def getStartPoint(self):
        return self.__startPoint
    
    def getEndPoint(self):
        return self.__endPoint
    
    def getShape(self):
        return self.__line
    
class Circle:
    __circle = None
    __centerPoint = None
    __radius = None

    __centerPointPlot = None
    

    def __init__(self):
        pointList[self] = []

    def plotShape(self):
        if self.__centerPoint != None:
            self.__circle = patches.Circle((self.__centerPoint.getX(), self.__centerPoint.getY()), radius=self.__radius, edgecolor='blue', facecolor = 'None')

            #plots circle and radius point
            plot1.add_patch(self.__circle)
            self.__centerPointPlot, = plot1.plot(self.__centerPoint.getX(),self.__centerPoint.getY(), "o")
            canvas.draw()

    def removeShape(self):
        if self.__circle != None:
            # removes line and endPoint
            self.__circle.remove()
            self.__centerPointPlot.remove()
            canvas.draw()

    # sets the center point
    def setStartPoint(self, centerPoint):
        self.__centerPoint = centerPoint
        if (len(pointList[self]) == 0):
            pointList[self].append(self.__centerPoint)
        else:
            pointList[self][0] = self.__centerPoint

    def setEndPoint(self, endPoint):
        self.__radius = math.sqrt(((self.__centerPoint.getX()-endPoint.getX()))**2+(self.__centerPoint.getY()-endPoint.getY())**2)
    
    def getCenterPoint(self):
        return self.__centerPoint
    
    def getRadius(self):
        return self.__radius
    
    def getShape(self):
        return self.__circle


"""
Series of functions to deal with mouseEvents

"""
# function to deal with user clicking.
def click_handler(event):
    global mouseDown
    global currentShape
    global movePoint
    currentPoint = Point(event.xdata, event.ydata)
    mouseDown = True

    if (not event.inaxes):
        return

    # checks if user is clicking on an existing point
    for object, points in pointList.items():
        startPoint = points[0]
        endPoint = points[1]
        if (currentPoint.equals(startPoint)):
            # flips start and end point of the line
            if (mode == "Line"):
                object.setStartPoint(endPoint)
                object.setEndPoint(startPoint)
            
            movePoint = currentPoint
            currentShape = object
            return
        elif (currentPoint.equals(endPoint)):
            movePoint = currentPoint
            currentShape = object
            return
    currentShape = Line() if mode == "Line" else Circle()
    currentShape.setStartPoint(currentPoint)
    shapeList.append(currentShape)

def drag_handler(event):
    if (not event.inaxes):
        return
    if mouseDown:
        global movePoint
        currentPoint = Point(event.xdata,event.ydata)

        if (movePoint != None):
            movePoint = currentPoint
        #removes the current drawing of the line
        currentShape.removeShape()
        currentShape.setEndPoint(currentPoint)
        currentShape.plotShape()

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
epsilon = 5 #amount of error allowed for clicking on points
mouseDown = False

# store various graph objects
shapeList = [] 
pointList = {} #dictionary to store points based on their associated structures (lines, circles, etc)

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
