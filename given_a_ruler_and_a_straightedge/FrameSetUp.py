from Shape import *
from Line import *
from Achievement import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import Button,Label,Frame, Tk

import EventHandlers

""""
Class dealing with frame details
Includes setting up the frame and adjusting the frame as users interact with it (such as changing buttons)
"""

# updates button colors
def changeButtonColor(button):
    clickedButtonCol = "light grey"
    unclickedButtonCol = "white smoke"
    button.config(bg=clickedButtonCol)

    # changes other buttons to other color
    if (button in shapeButtonList):
        for b in shapeButtonList:
            if (b != button):
                b.config(bg=unclickedButtonCol)

    if (button in operationButtonList):
        for b in operationButtonList:
            if (b != button):
                b.config(bg=unclickedButtonCol)


# changes the button color for the selected shape
def changeShape(newShape):
    EventHandlers.shapeType = newShape
    match newShape:
        case "Line":
            changeButtonColor(lineButton)
        case "Point":
            changeButtonColor(pointButton)
        case "Circle":
            changeButtonColor(circleButton)

# changes the button color for the selected tool
def changeToolMode(newTool):
    EventHandlers.toolMode = newTool
    match newTool:
        case "Draw":
            changeButtonColor(drawButton)
        case "Move":
            changeButtonColor(moveButton)
        case "Delete":
            changeButtonColor(deleteButton)
        case "Select":
            changeButtonColor(selectButton)

def achievementsOnOff(Main):
    Main.achievementsOn = not Main.achievementsOn
    if (Main.achievementsOn == True):
        achievementsOnButton.config(text="Turn Achievements Off")
    else:
        achievementsOnButton.config(text="Turn Achievements On")


# clears the plot
def clear():
    changeToolMode("Draw")
    changeButtonColor(drawButton)
    changeShape("Point")
    changeButtonColor(pointButton)

    EventHandlers.shapeList = []
    PLOT.cla()
    PLOT.set_xlim(0,PLOTSIZE)
    PLOT.set_ylim(0,PLOTSIZE)
    PLOT.set_axis_off()
    CANVAS.draw()

def showAngles():
    if showAnglesButton.cget("text") == "Show Angles":
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.showAngles(PLOT,CANVAS)
        showAnglesButton.config(text= "Hide Angles")

    else:
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.hideAngles(CANVAS)
        showAnglesButton.config(text= "Show Angles")

def showMetrics():
    if (showMetricsButton.cget("text") == "Show Metrics"):
        for shape in EventHandlers.shapeList:
            shape.showMetrics(PLOT, CANVAS)
        showMetricsButton.config(text = "Hide Metrics")
    else:
        for shape in EventHandlers.shapeList:
            shape.hideMetrics(CANVAS)

        showMetricsButton.config(text = "Show Metrics")

# constants to define from Main
ROOT = None
PLOT = None
CANVAS = None
PADX = None
PADY = None
PLOTSIZE = None

# Frame Set Up global variables
dataDisplay = None
toolLabel,shapeLabel,operationLabel = None, None, None
pointButton,lineButton,circleButton= None, None, None
moveButton,deleteButton,selectButton,drawButton = None,None,None,None
clearButton,showAnglesButton, showMetricsButton= None, None, None
achievementsOnButton = None
shapeButtonList,operationButtonList = None, None


def setUp(Main):
    # constants
    global ROOT, PLOT, CANVAS, PADX, PADY, PLOTSIZE
    PADX=Main.PADX
    PADY=Main.PADY
    PLOTSIZE = Main.PLOTSIZE

    # Frame set up variables
    global dataDisplay,toolLabel,shapeLabel,operationLabel
    global pointButton, lineButton,circleButton
    global moveButton,deleteButton,selectButton,drawButton
    global clearButton,showAnglesButton,showMetricsButton
    global achievementsOnButton
    global shapeButtonList,operationButtonList

    # creating the root TKinter component
    ROOT = Tk()
    ROOT.geometry("600x700")
    ROOT.title('Euclidean Playground')
    
    # the figure that will contain the Canvas
    FIG = Figure(figsize = (5, 5), dpi = 100, constrained_layout=True)

    # creates the canvas containing the plot
    CANVAS = FigureCanvasTkAgg(FIG, master = ROOT)  
    CANVAS.get_tk_widget().config(width=PLOTSIZE,height=PLOTSIZE)
    CANVAS.draw()

    # creates a plot 
    PLOT = FIG.add_subplot(111)
    PLOT.set_xlim(0,PLOTSIZE)
    PLOT.set_ylim(0,PLOTSIZE)
    PLOT.set_axis_off()

    # creating the Matplotlib toolbar
    tb = NavigationToolbar2Tk(CANVAS, ROOT)
    tb.update()

    # buttons and labels
    dataDisplay = Label(ROOT, text="")
    descriptLabel = Label(ROOT, text="You have been given a straightedge and a compass")
    toolbar = Frame(ROOT)
    toolLabel = Label(toolbar, text="Toolbar")
    shapeLabel = Label(toolbar, text="Shape Library")
    operationLabel = Label(toolbar, text="Operations")
    pointButton = Button(toolbar, command=lambda: [changeShape("Point"), changeButtonColor(pointButton)], height = 2, width = 10, text = "Point")
    lineButton = Button(toolbar, command=lambda: [changeShape("Line"), changeButtonColor(lineButton)], height = 2, width = 10, text = "Line")
    circleButton = Button(toolbar, command =lambda: [changeShape("Circle"),changeButtonColor(circleButton)], height = 2, width = 10, text = "Circle")
    clearButton = Button(toolbar,command=lambda:[clear()],height = 2, width = 10, text = "Clear")
    moveButton = Button(toolbar,command =lambda: [changeToolMode("Move"),changeButtonColor(moveButton)],height = 2, width = 10, text = "Move Point")
    deleteButton = Button(toolbar,command =lambda: [changeToolMode("Delete"),changeButtonColor(deleteButton)],height = 2, width = 10, text = "Delete Object")
    selectButton = Button(toolbar,command =lambda: [changeToolMode("Select"),changeButtonColor(selectButton)],height = 2, width = 10, text = "Select Object")
    drawButton = Button(toolbar, command = lambda:[changeToolMode("Draw"),changeButtonColor(drawButton)],height = 2, width = 10, text = "Draw")
    showAnglesButton = Button(toolbar, command= lambda: [showAngles()],height = 2, width = 10, text = "Show Angles")
    showMetricsButton = Button(toolbar, command = lambda: [showMetrics()],height = 2, width = 10, text = "Show Metrics")
    achievementsOnButton = Button(toolbar, command = lambda: [achievementsOnOff(Main)],height = 2, width = 20, text = "Turn Achievements On")

    # lists containing buttons that will have coloration
    shapeButtonList = [pointButton,lineButton,circleButton]
    operationButtonList = [moveButton,deleteButton,selectButton,drawButton]

    # description setup
    descriptLabel.pack()

    # tool setup
    toolLabel.grid(row=0, column=1, padx=PADX, pady=PADY)

    # Shape types
    shapeLabel.grid(row=1, column=1, padx=PADX, pady=PADY)
    pointButton.grid(row=2,column=1, padx=PADX, pady=PADY)
    lineButton.grid(row=2,column=2, padx=PADX, pady=PADY)
    circleButton.grid(row=2,column=3, padx=PADX, pady=PADY)
    changeButtonColor(pointButton)

    # Operation Types
    operationLabel.grid(row=3, column = 1, padx=PADX, pady=PADY)
    moveButton.grid(row=4,column=1, padx=PADX, pady=PADY)
    deleteButton.grid(row=4,column=2, padx=PADX, pady=PADY)
    selectButton.grid(row=4, column = 3, padx=PADX, pady=PADY)
    drawButton.grid(row=4, column=4, padx=PADX, pady=PADY)
    changeButtonColor(drawButton)

    # Other Operations
    clearButton.grid(row=5,column=1, padx=PADX, pady=PADY)
    showAnglesButton.grid(row=5,column = 2,padx=PADX,pady=PADY)
    showMetricsButton.grid(row = 5, column = 3, padx=PADX, pady=PADY)

    #achievements Button
    achievementsOnButton.grid(row = 6, column = 1, columnspan= 2, padx=PADX,pady=PADY)

    toolbar.pack()

    # placing the CANVAS on the Tkinter window
    CANVAS.get_tk_widget().pack()

    # placing the toolbar on the Tkinter window
    CANVAS.get_tk_widget().pack()

    # data display setup
    dataDisplay.pack()
