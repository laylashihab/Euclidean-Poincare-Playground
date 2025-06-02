from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

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

    def plotLine(self):
        if self.__endPoint != None:
            x_data = np.linspace(self.__startPoint.getX(), self.__endPoint.getX(), 100)
            y_data = np.linspace(self.__startPoint.getY(), self.__endPoint.getY(),100)
            line, = plot1.plot(x_data,y_data)
            self.__line = line

            #plots endpoints
            self.__startPointPlot, = plot1.plot(self.__startPoint.getX(),self.__startPoint.getY(), "o")
            self.__endPointPlot, = plot1.plot(self.__endPoint.getX(),self.__endPoint.getY(), "o")
            canvas.draw()
    
    def removeLine(self):
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
    
    def getLine(self):
        return self.__line

"""
Series of functions to deal with mouseEvents

"""
# function to deal with user clicking.
def click_handler(event):
    global movePoint
    currentPoint = Point(event.x,plot_size- event.y)

    # checks if user is clicking on an existing point
    for object, points in pointList.items():
        startPoint = points[0]
        endPoint = points[1]
        if (currentPoint.equals(startPoint)):
            object.setStartPoint(endPoint)
            object.setEndPoint(startPoint)
            
            movePoint = currentPoint
            return
        elif (currentPoint.equals(endPoint)):
            movePoint = currentPoint
            return

    global currentLine
    currentLine = Line()
    currentLine.setStartPoint(currentPoint)
    lineList.append(currentLine)

def drag_handler(event):
    global movePoint
    currentPoint = Point(event.x,plot_size- event.y)

    if (movePoint != None):
        movePoint = currentPoint
    #removes the current drawing of the line
    currentLine.removeLine()
    currentLine.setEndPoint(currentPoint)
    currentLine.plotLine()

def unclick_handler(event):
    pass

# changes type of shape plot
def changeMode(newMode):
    mode = newMode

# clears the plot
def clear():
    global lineList
    lineList = []
    plot1.cla()
    plot1.set_xlim(0,plot_size)
    plot1.set_ylim(0,plot_size)
    plot1.set_axis_off()
    canvas.draw()

# variables
startPoint = [0,0]
mode = "Line"
plot_size = 400
currentLine = None
movePoint = None
epsilon = 5 #amount of error allowed for clicking on points

# store various graph objects
lineList = [] 
pointList = {} #dictionary to store points based on their associated structures (lines, circles, etc)

# the figure that will contain the plot
fig = Figure(figsize = (5, 5), dpi = 100)

#main window setup
root = Tk()
root.geometry("500x500")
root.title('Euclidean Playground')

# description setup
descriptLabel = Label(root, text="You have been given a straightedge and a compass")
descriptLabel.pack()

# tool setup
toolLabel = Label(root, text="Tools:")
lineButton = Button(root, command = changeMode("Line"), height = 2, width = 10, text = "Line")
lineButton.pack()
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
root.bind("<Button>", click_handler)
root.bind("<B1-Motion>", drag_handler)
root.bind("<ButtonRelease>", unclick_handler)

root.mainloop()
