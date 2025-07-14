from Shape import *
from Line import *
from Achievement import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import tkinter as tk

import EventHandlers
import constants as c


""""
Class dealing with frame details
Includes setting up the frame and adjusting the frame as users interact with it (such as changing buttons)
"""

# button type colors
clickedButtonCol = "light grey"
unclickedButtonCol = "white smoke"
unavailableButtonCol = "thistle4"

# other colors
backgroundCol = "lavender"
textCol = "black"
buttonTextCol = "black"

# frame set-up
frameSize = "600x800"
figSize = (6, 5)

# updates button colors
def changeButtonColor(button):
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
        case c.LINE:
            changeButtonColor(lineButton)
        case c.POINT:
            changeButtonColor(pointButton)
        case c.CIRCLE:
            changeButtonColor(circleButton)

# changes the button color for the selected tool
def changeToolMode(newTool):
    # ensures that any thick lines are cleared 
    if EventHandlers.toolMode == c.SELECT and newTool != c.SELECT:
        for shape in EventHandlers.shapeList:
            shape.removeShape()
            shape.plotShape(PLOT)
            CANVAS.draw()
    # ensures that scaled values are saved
    elif EventHandlers.toolMode == c.SCALE and newTool != c.SCALE:
        scaleVal = float(scaleSlider.get())
        currentShape = EventHandlers.currentShape
        currentShape.confirmScaleSize(scaleVal,PLOT)
        CANVAS.draw()

        dataDisplay.config(text=currentShape.measure())
        dataDisplay.update()

        # ensures the scale slider is hidden
        scaleSlider.set(100)
        scaleSlider.grid_forget()
    
    EventHandlers.toolMode = newTool
    match newTool:
        case c.DRAW:
            changeButtonColor(drawButton)
        case c.MOVEPOINT:
            changeButtonColor(movePointButton)
        case c.DELETE:
            changeButtonColor(deleteButton)
        case c.MOVEOBJECT:
            changeButtonColor(moveObjectButton)
        case c.SELECT:
            changeButtonColor(selectButton)
    
    # ensures that all lines are thin
    for shape in EventHandlers.shapeList:
        shape.removeShape()
        shape.plotShape(PLOT)

def achievementsOnOff(Main):
    Main.achievementsOn = not Main.achievementsOn
    if (Main.achievementsOn == True):
        achievementsOnButton.config(text="Turn Achievements Off")
    else:
        achievementsOnButton.config(text="Turn Achievements On")


# clears the plot
def clear():
    changeToolMode(c.DRAW)
    changeButtonColor(drawButton)
    changeShape(c.POINT)
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
                shape.showAngles(PLOT)
                CANVAS.draw()
        showAnglesButton.config(text= "Hide Angles")

    else:
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.hideAngles()
                CANVAS.draw()
        showAnglesButton.config(text= "Show Angles")

def showMetrics():
    if (showMetricsButton.cget("text") == "Show Metrics"):
        for shape in EventHandlers.shapeList:
            shape.showMetrics(PLOT)
        showMetricsButton.config(text = "Hide Metrics")
    else:
        for shape in EventHandlers.shapeList:
            shape.hideMetrics()

        showMetricsButton.config(text = "Show Metrics")
    CANVAS.draw()

def saveFigure(shape):
    global savedFiguresList
    # ensures a copy of the shape is saved, not the actual shape object
    shape = copy.deepcopy(shape)

    if (shape == None):
        print("Save Failed: Object type == None")
    else:
        savedFiguresList.append(shape)

def addFigure(figure):
    # ensures a copy of the saved figure is added
    figure = copy.deepcopy(figure)
    figure.plotShape(PLOT)
    CANVAS.draw()
    EventHandlers.shapeList.append(figure)
    EventHandlers.currentShape = None

def openFigureLibrary():
    global savedFiguresList, figureButtonList

    # sets up the figure library window
    LIBRARYROOT = tk.Toplevel(ROOT)
    LIBRARYROOT.title("Figure Library")
    plotsize = 100

    # adds all figures to a component
    num = 1
    for figure in savedFiguresList:
        item = tk.Frame(LIBRARYROOT)

        label = tk.Label(item,text = str(num))
        num +=1

        fig = Figure(figsize = figSize, dpi = 100, constrained_layout=True)

        # creates the canvas containing the plot
        canvas = FigureCanvasTkAgg(fig, master = item)  
        canvas.get_tk_widget().config(width=plotsize,height=plotsize)
        canvas.draw()

        # creates a plot 
        plot = fig.add_subplot(111)
        plot.set_xlim(0,plotsize)
        plot.set_ylim(0,plotsize)
        plot.set_axis_off()

        # creates a button associated with the plot
        b = tk.Button(item, command=lambda fig=figure: addFigure(fig), height = 2, width = 10, text = "Add to Canvas")
        figureButtonList.append(b)

        # packs all components
        label.grid(row = 0, column = 0,padx=PADX, pady=PADY)
        canvas.get_tk_widget().grid(row=0,column=1,padx=PADX, pady=PADY)
        b.grid(row = 0, column =2,padx=PADX, pady=PADY)

        item.pack()
                
        # plots the shape in scale to the figure library plotsize
        figure.plotShapeScaledPlotsize(plot,oldPlotSize = PLOTSIZE, newPlotSize=plotsize)
        CANVAS.draw()

def styleButton(button):
    button.config(fg=buttonTextCol)

def styleLabel(label):
    label.config(fg=textCol, bg=backgroundCol)

def scaleChange(value):
    currentShape = EventHandlers.currentShape
    if (type(currentShape) != Point):
        value = float(value)
        currentShape.scale(value, PLOT)
        CANVAS.draw()

# constants
ROOT = None
LIBRARYROOT = None
FIGURES = None
PLOT = None
CANVAS = None
PADX = None
PADY = None
PLOTSIZE = None

# Frame Set Up global variables
dataDisplay = None
toolLabel,shapeLabel,operationLabel = None, None, None
pointButton,lineButton,circleButton= None, None, None
movePointButton,deleteButton,moveObjectButton,drawButton = None,None,None,None
clearButton,showAnglesButton, showMetricsButton,selectButton= None, None, None, None
achievementsOnButton, saveFigureButton = None, None
shapeButtonList,operationButtonList = None, None
scaleShapeButton,scaleSlider = None,None
savedFiguresList =[]
figureButtonList = []

def setUp(Main):
    # constants
    global ROOT, LIBRARYROOT, FIGURES, PLOT, CANVAS, PADX, PADY, PLOTSIZE
    PADX=c.PADX
    PADY=c.PADY
    PLOTSIZE = c.PLOTSIZE

    # Frame set up variables
    global dataDisplay,toolLabel,shapeLabel,operationLabel
    global pointButton, lineButton,circleButton
    global movePointButton,deleteButton,drawButton,moveObjectButton
    global clearButton,showAnglesButton,showMetricsButton
    global achievementsOnButton,selectButton,saveFigureButton,openFigureLibraryButton
    global shapeButtonList,operationButtonList
    global scaleShapeButton,scaleSlider
    
    # creating the root TKinter component
    ROOT = tk.Tk()
    ROOT.geometry(frameSize)
    ROOT.title('Euclidean Playground')
    ROOT.config(bg=backgroundCol)
    
    # the figure that will contain the Canvas
    FIG = Figure(figsize = figSize, dpi = 100, constrained_layout=True)

    # creates the canvas containing the plot
    CANVAS = FigureCanvasTkAgg(FIG, master = ROOT)  
    CANVAS.get_tk_widget().config(width=PLOTSIZE,height=PLOTSIZE)
    CANVAS.draw()

    # creates a plot 
    PLOT = FIG.add_subplot(111)
    PLOT.set_xlim(0,PLOTSIZE)
    PLOT.set_ylim(0,PLOTSIZE)
    PLOT.set_axis_off()

    # buttons and labels
    dataDisplay = tk.Label(ROOT, text="")
    descriptLabel = tk.Label(ROOT, text="You have been given a straightedge and a compass")
    TOOLBAR = tk.Frame(ROOT, bg=backgroundCol)
    shapeLabel = tk.Label(TOOLBAR, text="Shape Library")
    operationLabel = tk.Label(TOOLBAR, text="Operations")
    
    # Shape Buttons
    pointButton = tk.Button(TOOLBAR, command=lambda: [changeShape(c.POINT), changeButtonColor(pointButton)], height = 2, width = 10, text = "Point")
    lineButton = tk.Button(TOOLBAR, command=lambda: [changeShape(c.LINE), changeButtonColor(lineButton)], height = 2, width = 10, text = "Line")
    circleButton = tk.Button(TOOLBAR, command =lambda: [changeShape(c.CIRCLE),changeButtonColor(circleButton)], height = 2, width = 10, text = "Circle")
    
    # Basic Operation Buttons
    clearButton = tk.Button(TOOLBAR,command=lambda:[clear()],height = 2, width = 12, text = "Clear")
    movePointButton = tk.Button(TOOLBAR,command =lambda: [changeToolMode(c.MOVEPOINT),changeButtonColor(movePointButton)],height = 2, width = 12, text = "Move Point")
    deleteButton = tk.Button(TOOLBAR,command =lambda: [changeToolMode(c.DELETE),changeButtonColor(deleteButton)],height = 2, width = 12, text = "Delete Object")
    moveObjectButton = tk.Button(TOOLBAR,command =lambda: [changeToolMode(c.MOVEOBJECT),changeButtonColor(moveObjectButton)],height = 2, width = 12, text = "Move Object")
    drawButton = tk.Button(TOOLBAR, command = lambda:[changeToolMode(c.DRAW),changeButtonColor(drawButton)],height = 2, width = 12, text = "Draw")
    
    # Measurements Buttons
    showAnglesButton = tk.Button(TOOLBAR, command= lambda: [showAngles()],height = 2, width = 15, text = "Show Angles")
    showMetricsButton = tk.Button(TOOLBAR, command = lambda: [showMetrics()],height = 2, width = 15, text = "Show Metrics")

    scaleShapeButton = tk.Button(TOOLBAR,command=lambda: [showSlider(),changeButtonColor(scaleShapeButton),changeToolMode(c.SCALE)],height=2,width=15,text="Scale")
    scaleSlider = tk.Scale(TOOLBAR, from_=0, to=200, orient=tk.HORIZONTAL,command=scaleChange, resolution=1,width=20)

    # bottom TOOLBAR setup
    EXTRATOOLS = tk.Frame(ROOT,bg=backgroundCol)

    saveFigureButton = tk.Button(EXTRATOOLS, command= lambda: [saveFigure(EventHandlers.selectedShape)], height = 2, width = 15, text = "Save Figure")
    openFigureLibraryButton = tk.Button(EXTRATOOLS, command= lambda:[openFigureLibrary()], height = 2, width = 20, text = "Open Saved Figure Library")
    selectButton = tk.Button(EXTRATOOLS,command =lambda: [changeToolMode(c.SELECT),changeButtonColor(selectButton)],height = 2, width = 15, text = "Select Object")


    achievementsOnButton = tk.Button(EXTRATOOLS, command = lambda: [achievementsOnOff(Main)],height = 1, width = 20, text = "Turn Achievements On")

    # lists containing buttons that will have coloration
    shapeButtonList = [pointButton,lineButton,circleButton]
    operationButtonList = [movePointButton,deleteButton,moveObjectButton,drawButton, selectButton, scaleShapeButton]

    # list containing all button components
    buttons = [pointButton,lineButton,circleButton,clearButton,movePointButton,deleteButton,selectButton,drawButton,showAnglesButton,
               showMetricsButton,achievementsOnButton,saveFigureButton,openFigureLibraryButton, moveObjectButton]
    # list containing all label components
    labels = [dataDisplay,descriptLabel,shapeLabel,operationLabel]

    # styles all buttons and labels
    for button in buttons:
        styleButton(button)
    for label in labels:
        styleLabel(label)

    # description setup
    descriptLabel.pack()

    def placeRow(list, row, startCol):
        col = startCol
        for item in list:
            item.grid(row=row, column=col,padx=PADX,pady=PADY)
            col+=1

    # Shape types
    shapeLabel.grid(row=1, column=1, padx=PADX, pady=PADY)
    placeRow([pointButton,lineButton,circleButton],2,1)
    changeButtonColor(pointButton)

    # Operation Types
    operationLabel.grid(row=3, column = 1, padx=PADX, pady=PADY)
    placeRow([drawButton, movePointButton,moveObjectButton,deleteButton,clearButton],4,0)
    changeButtonColor(drawButton)

    # Measurement Buttons
    def showSlider():
        scaleSlider.grid(row=5,column=2,columnspan=2)
    placeRow([showAnglesButton,showMetricsButton],5,0)
    showSlider()
    scaleShapeButton.grid(row=5,column=4,padx=PADX, pady=PADY)
    scaleSlider.set(100)

    # figure library tools
    placeRow([selectButton,saveFigureButton,openFigureLibraryButton],6,1)

    # placing achievements option
    achievementsOnButton.grid(row=7,column = 1, padx=PADX, pady=PADY)

    # placing the TOOLBAR on the Tkinter window
    TOOLBAR.pack()

    # placing the canvas
    CANVAS.get_tk_widget().pack()

    # data display setup
    dataDisplay.pack()

    EXTRATOOLS.pack()
    saveFigureButton.grid_forget()
    scaleSlider.grid_forget()
