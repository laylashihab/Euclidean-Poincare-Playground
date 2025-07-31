from Shape import *
from Line import *
from Achievement import *
import EventHandlers
import poincareDisk
import constants as c

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import tkinter as tk
from tkinter import font,ttk 

""""
Class dealing with frame details
Includes setting up the frame and adjusting the frame as users interact with it (such as changing buttons)
"""

# updates button colors
def changeButtonColor(button):
    # None is passed through when there is no shape type selected, removes all coloration from that shape
    if button == None:
        for b in shapeButtonList:
            b.config(bg=c.unclickedButtonCol)
        return

    button.config(bg=c.clickedButtonCol)

    # changes other buttons to other color
    if (button in shapeButtonList):
        for b in shapeButtonList:
            if (b != button):
                b.config(bg=c.unclickedButtonCol)

    if (button in operationButtonList):
        for b in operationButtonList:
            if (b != button):
                b.config(bg=c.unclickedButtonCol)


# changes the button color for the selected shape
def changeShape(newShape):
    # ensures that the user is in draw mode
    changeToolMode(c.DRAW)
    if newShape != None:
        EventHandlers.shapeType = newShape        
    match newShape:
        case c.LINE:
            changeButtonColor(lineButton)
        case c.POINT:
            changeButtonColor(pointButton)
        case c.CIRCLE:
            changeButtonColor(circleButton)
        case None:
            changeButtonColor(None)

# changes the button color for the selected tool
def changeToolMode(newTool):
    objectSavedLabel.grid_remove()

    # ensures that any thick lines are cleared 
    if EventHandlers.toolMode == c.SELECT and newTool != c.SELECT:
        selectObjectLabel.grid_remove()
        for shape in EventHandlers.shapeList:
            shape.removeShape()
            shape.plotShape(PLOT, poincare=EventHandlers.poincareMode)
        CANVAS.draw()

    # ensures that the scale bar is removed and line is thin again
    elif EventHandlers.toolMode == c.SCALE and newTool != c.SCALE:
        scaleSlider.grid_remove()
        selectObjectLabel.grid_remove()
        scaleLabel.grid_remove()
        currentShape = EventHandlers.currentShape
        if currentShape != None:
            currentShape.removeShape()
            currentShape.plotShape(PLOT, poincare=EventHandlers.poincareMode)
            CANVAS.draw()

    # ensures that the user is told to choose an object
    if newTool == c.SCALE or newTool == c.SELECT:
        selectObjectLabel.grid()

    # ensures that the scale label and slider are shown
    if newTool == c.SCALE:
        scaleLabel.grid()
        scaleSlider.grid()

    # ensures that shape types are hidden when user clicks off of draw
    if newTool != c.DRAW and EventHandlers.toolMode == c.DRAW:
        changeShape(None)

    # changes tool mode
    EventHandlers.toolMode = newTool

    # deals with button coloration
    match newTool:
        case c.DRAW:
            changeButtonColor(drawButton)
        case c.MOVEPOINT:
            changeButtonColor(movePointButton)
        case c.DELETE:
            changeButtonColor(deleteButton)
        case c.MOVEOBJECT:
            changeButtonColor(moveObjectButton)
        case c.SCALE:
            changeButtonColor(scaleShapeButton)
            EventHandlers.clearCurrentShape()
        case c.SAVEFIGURE:
            changeButtonColor(saveFigureButton)

def achievementsOnOff(Main):
    Main.achievementsOn = not Main.achievementsOn
    if (Main.achievementsOn == True):
        achievementsOnButton.config(text="Achievements Off")
    else:
        achievementsOnButton.config(text="Achievements On")

# clears the plot
def clear():
    changeToolMode(c.DRAW)
    changeButtonColor(drawButton)
    changeShape(c.POINT)
    changeButtonColor(pointButton)

    # change sliders to original value
    zoomSlider.set(100)
    scaleSlider.set(100)

    EventHandlers.shapeList = []
    EventHandlers.plotbounds = c.PLOTBOUNDS
    PLOT.cla()

    # updates data display
    dataDisplay.config(text="")
    dataDisplay.update()

    # ensures the boundary is drawn again
    if EventHandlers.poincareMode == True:
        poincareDisk.drawBoundary()
        PLOT.set_xlim(-1,1)
        PLOT.set_ylim(-1,1)
    else:
        plotBounds = EventHandlers.plotBounds
        PLOT.set_xlim(- plotBounds + EventHandlers.xBoundDelta,plotBounds + EventHandlers.xBoundDelta)
        PLOT.set_ylim(- plotBounds + EventHandlers.yBoundDelta,plotBounds + EventHandlers.yBoundDelta)
    PLOT.set_axis_off()
    CANVAS.draw()

def showAngles():
    global anglesOn
    # flips whether or not angles should be on
    anglesOn = not anglesOn
    if anglesOn:
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.showAngles(PLOT)
        showAnglesButton.config(text= "Hide Angles")
    else:
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.hideAngles()
        showAnglesButton.config(text= "Show Angles")
    CANVAS.draw()

def showMetrics():
    global metricsOn
    metricsOn = not metricsOn
    if metricsOn:
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
    selectObjectLabel.grid_remove()
    objectSavedLabel.grid()
    # ensures a copy of the shape is saved, not the actual shape object
    shape = copy.deepcopy(shape)
    if shape.getPoincare() == True:
        shape.convertToEuclidean()

    if (shape == None):
        print("Save Failed: Object type == None")
    else:
        savedFiguresList.append(shape)

# adds a saved figure to the main canvas
def addFigure(figure):
    # ensures a copy of the saved figure is added
    figure = copy.deepcopy(figure)
    # ensures the figure has the correct type of coordinates
    if figure.getPoincare() == True and EventHandlers.poincareMode != True:
        figure.convertToEuclidean()
    elif figure.getPoincare() == False and EventHandlers.poincareMode == True:
        figure.convertToPoincare()
    figure.plotShape(PLOT,poincare=EventHandlers.poincareMode)
    CANVAS.draw()
    EventHandlers.shapeList.append(figure)
    EventHandlers.currentShape = None

def removeFigure(figure):
    global savedFiguresList
    global LIBRARYROOT
    if figure in savedFiguresList:
        savedFiguresList.remove(figure)

    LIBRARYROOT.destroy()
    openFigureLibrary()

def openFigureLibrary():
    global savedFiguresList, LIBRARYROOT, figureLibraryOpen

    # if the window is already open, close it and open a new one
    if LIBRARYROOT != None and LIBRARYROOT.winfo_exists():
        LIBRARYROOT.destroy()

    # sets up the figure library window
    LIBRARYROOT = tk.Toplevel(ROOT, bg=c.backgroundCol)
    LIBRARYROOT.title("Figure Library")
    LIBRARYROOT.geometry("500x400")
    plotsize = 150
    figureLibraryTitle = tk.Label(LIBRARYROOT, text="Saved Figures")
    styleLabel(figureLibraryTitle,titleFont)
    figureLibraryTitle.pack()

    # checks there are figures saved
    if len(savedFiguresList) == 0:
        noFigures = tk.Label(LIBRARYROOT,text="No Figures Saved")
        styleLabel(noFigures,labelFont)
        noFigures.pack()
        return

    # frame to hold the scrollbar region
    frame = tk.Frame(LIBRARYROOT, width=500,height=400, bg = c.backgroundCol)

    # scroll bar
    scrollregion = tk.Canvas(frame,bg=c.backgroundCol,scrollregion=(0,0,500, 175 * len(savedFiguresList)))
    scrollbar = ttk.Scrollbar(frame, orient="vertical",command=scrollregion.yview) 
    scrollregion.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT,fill=tk.Y)                     
    scrollregion.pack(side=tk.LEFT)      
    
    # adds all figures to a component
    num = 1
    for figure in savedFiguresList:
        item = tk.Frame(frame, bg = c.backgroundCol, borderwidth=2, relief="groove")

        label = tk.Label(item,text = "Fig " + str(num))
        styleLabel(label,otherTextFont)

        fig = Figure(figsize = c.figSize, dpi = 100, constrained_layout=True)

        # creates the canvas containing the plot
        canvas = FigureCanvasTkAgg(fig, master = item)  
        canvas.get_tk_widget().config(width=plotsize,height=plotsize)

        # creates a plot 
        plot = fig.add_subplot(111)
        plot.set_xlim(-EventHandlers.plotBounds,EventHandlers.plotBounds)
        plot.set_ylim(-EventHandlers.plotBounds,EventHandlers.plotBounds)
        plot.set_axis_off()

        # creates a button associated with the plot
        b = tk.Button(item, command=lambda fig=figure: addFigure(fig), height = 2, width = 20, text = "Add to Canvas")
        styleButton(b, False)

        # creates a button to remove the figure from saved figures
        b2 = tk.Button(item, command=lambda fig=figure: removeFigure(fig),height=2, width=20, text = "Remove From Library")
        styleButton(b2, False)

        # packs all components
        label.grid(row = 0, column = 0, rowspan = 2, padx=5, pady=PADY)
        canvas.get_tk_widget().grid(row=0,column=1,rowspan=2, padx=5, pady=PADY)
        b.grid(row = 0, column =2,padx=5, pady=PADY)
        b2.grid(row = 1, column = 2,padx=5, pady=PADY)


        # plots the shape in scale to the figure library plotsize
        figure.plotShapeScaledPlotsize(plot,oldPlotSize = c.PLOTSIZE, newPlotSize=plotsize)
            
        scrollregion.create_window(0, (num-1) * 175, window=item, anchor="nw")
        num +=1

    frame.pack()
    canvas.draw()

# styles all buttons and labels
def styleButton(button, normalizeSize = True):
    button.config(fg=c.buttonTextCol)
    button.config(font=buttonFont)
    if normalizeSize == True:
        button.config(width = c.buttonWidth)
        button.config(height = c.buttonHeight)

def styleLabel(label, font):
    label.config(fg=c.textCol, bg=c.backgroundCol)
    label.config(font = font)

def defineFonts():
    global labelFont,otherTextFont,titleFont,buttonFont,instructionsFont
    labelFont = font.Font(family=c.fontFamilyLabels,size = c.fontSizeLabels, weight=c.fontWeightLabels)
    instructionsFont = font.Font(family=c.fontFamilyLabels,size=c.instructionsSize, weight=c.fontWeightLabels)
    otherTextFont = font.Font(family = c.fontFamilyOtherText, size = c.fontSizeOtherText, weight=c.fontWeightOtherText)
    titleFont = font.Font(family=c.fontFamilyTitle,size=c.fontSizeTitle,weight=c.fontWeightTitle)
    buttonFont = font.Font(family=c.fontFamilyButton,size=c.fontSizeButton,weight=c.fontWeightButton)

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
pointButton,lineButton,circleButton= None, None, None
movePointButton,deleteButton,moveObjectButton,drawButton = None,None,None,None
clearButton,showAnglesButton, showMetricsButton= None, None, None
achievementsOnButton, saveFigureButton = None, None
shapeButtonList,operationButtonList = None, None
scaleShapeButton,scaleSlider = None,None
zoomLabel,zoomSlider = None,None
poincareButton = None
selectObjectLabel,objectSavedLabel,scaleLabel = None, None,None
figureLibraryOpen = False
savedFiguresList =[]
anglesOn = False
metricsOn = False

def setUp(Main):
    # constants
    global ROOT, LIBRARYROOT, FIGURES, PLOT, CANVAS, PADX, PADY, PLOTSIZE
    PADX=c.PADX
    PADY=c.PADY
    PLOTSIZE = c.PLOTSIZE

    # Frame set up variables
    global dataDisplay
    global pointButton, lineButton,circleButton
    global movePointButton,deleteButton,drawButton,moveObjectButton
    global clearButton,showAnglesButton,showMetricsButton
    global achievementsOnButton,saveFigureButton,openFigureLibraryButton
    global shapeButtonList,operationButtonList
    global scaleShapeButton,scaleSlider
    global zoomLabel,zoomSlider
    global poincareButton
    global selectObjectLabel,objectSavedLabel,scaleLabel
    global labelFont,otherTextFont,titleFont,buttonFont,instructionsFont

    # creating the root TKinter component
    ROOT = tk.Tk()
    ROOT.geometry(c.frameSize)
    ROOT.title('Euclidean Playground')
    ROOT.config(bg=c.backgroundCol)
    
    # the figure that will contain the Canvas
    FIG = Figure(figsize = c.figSize, dpi = 100, constrained_layout=True)

    CANVASBAR = tk.Frame(ROOT, bg=c.backgroundCol, width = c.frameWidth)

    # creates the canvas containing the plot
    CANVAS = FigureCanvasTkAgg(FIG, master = CANVASBAR)  
    CANVAS.get_tk_widget().config(width=PLOTSIZE,height=PLOTSIZE)
    CANVAS.draw()

    # creates a plot 
    PLOT = FIG.add_subplot(111)
    PLOT.set_xlim(-c.PLOTBOUNDS,c.PLOTBOUNDS)
    PLOT.set_ylim(-c.PLOTBOUNDS,c.PLOTBOUNDS)
    PLOT.set_axis_off()

    # buttons and labels
    descriptLabel = tk.Label(ROOT, text="You Have Been Given a Straightedge and a Compass")
    TOOLBAR = tk.Frame(ROOT, bg=c.backgroundCol,width=c.frameWidth)
    EXTRATOOLS = tk.Frame(ROOT, bg=c.backgroundCol)
    shapeLabel = tk.Label(TOOLBAR, text="Shape Options")
    operationLabel = tk.Label(TOOLBAR, text="Operations")
    zoomLabel = tk.Label(CANVASBAR, text="Zoom")
    scaleLabel = tk.Label(CANVASBAR, text="Scale")
    otherToolsLabel = tk.Label(TOOLBAR, text = "Other Tools")
    selectObjectLabel = tk.Label(TOOLBAR, text = "Click on an object")
    objectSavedLabel = tk.Label(TOOLBAR, text = "Figure Saved!")
    dataDisplay = tk.Label(EXTRATOOLS, text="")
    canvasInstructionsLabel = tk.Label(EXTRATOOLS, text="Use Arrow Keys to navigate canvas")

    # Shape Buttons
    pointButton = tk.Button(TOOLBAR, command=lambda: [changeShape(c.POINT)], text = "Point")
    lineButton = tk.Button(TOOLBAR, command=lambda: [changeShape(c.LINE)], text = "Line")
    circleButton = tk.Button(TOOLBAR, command =lambda: [changeShape(c.CIRCLE)], text = "Circle")
    
    # Basic Operation Buttons
    movePointButton = tk.Button(TOOLBAR,command =lambda: [changeToolMode(c.MOVEPOINT),changeButtonColor(movePointButton)],text = "Move Point")
    deleteButton = tk.Button(TOOLBAR,command =lambda: [changeToolMode(c.DELETE),changeButtonColor(deleteButton)], text = "Delete Object")
    moveObjectButton = tk.Button(TOOLBAR,command =lambda: [changeToolMode(c.MOVEOBJECT),changeButtonColor(moveObjectButton)],text = "Move Object")
    drawButton = tk.Button(TOOLBAR, command = lambda:[changeToolMode(c.DRAW),changeButtonColor(drawButton)],text = "Draw")
    
    # additional operations
    scaleShapeButton = tk.Button(TOOLBAR,command=lambda: [changeToolMode(c.SCALE)],text="Scale")
    saveFigureButton = tk.Button(TOOLBAR, command= lambda: [changeToolMode(c.SELECT),changeButtonColor(saveFigureButton)], text = "Save Figure")
    openFigureLibraryButton = tk.Button(TOOLBAR, command= lambda:[openFigureLibrary()], text = "Open Figure Library")
    poincareButton = tk.Button(TOOLBAR,command=lambda: [poincareDisk.run()],text = "Poincare Disc")
    achievementsOnButton = tk.Button(TOOLBAR, command = lambda: [achievementsOnOff(Main)],text = "Achievements On")

    # sliders
    scaleSlider = tk.Scale(CANVASBAR, from_=1, to=200, orient=tk.VERTICAL, resolution=1,width=20, length = 200)
    zoomSlider = tk.Scale(CANVASBAR, from_=1, to =200, orient=tk.VERTICAL, resolution = 1, width=20,length = 200)

    # Extra tools
    showAnglesButton = tk.Button(EXTRATOOLS, command= lambda: [showAngles()], text = "Show Angles")
    showMetricsButton = tk.Button(EXTRATOOLS, command = lambda: [showMetrics()],text = "Show Metrics")
    clearButton = tk.Button(EXTRATOOLS,command=lambda:[clear()],text = "Clear")

    # lists containing buttons that will have coloration
    shapeButtonList = [pointButton,lineButton,circleButton]
    operationButtonList = [movePointButton,deleteButton,moveObjectButton,drawButton, scaleShapeButton,saveFigureButton]

    # list containing all button components
    buttons = [pointButton,lineButton,circleButton,clearButton,movePointButton,deleteButton,drawButton,showAnglesButton,
               showMetricsButton,achievementsOnButton,saveFigureButton,openFigureLibraryButton, moveObjectButton, scaleShapeButton,poincareButton]
    
    # lists containing all label components
    labels = [shapeLabel,operationLabel,zoomLabel,scaleLabel,otherToolsLabel]
    otherText = [dataDisplay,objectSavedLabel,selectObjectLabel,canvasInstructionsLabel]
    instructions = [selectObjectLabel,objectSavedLabel]
    titles = [descriptLabel]

    # sets up fonts
    defineFonts()

    for button in buttons:
        styleButton(button)
    for label in labels:
        styleLabel(label,labelFont)
    for label in otherText:
        styleLabel(label, otherTextFont)
    for label in titles:
        styleLabel(label,titleFont)
    for label in instructions:
        styleLabel(label, instructionsFont)

    def placeRow(list, row, startCol, padx= PADX, pady=PADY):
        col = startCol
        for item in list:
            item.grid(row=row, column=col,padx=padx,pady=pady)
            col+=1

    TOOLBAR.grid_columnconfigure([0,1,2,3,4],minsize = c.frameWidth/5) # ensures the space is kept for the labels
    # Shape types
    shapeLabel.grid(row=1, column=2, padx=PADX, pady=PADY)
    placeRow([pointButton,lineButton,circleButton],2,1)
    changeButtonColor(pointButton)

    # Operation Types
    operationLabel.grid(row=3, column = 2, padx=PADX, pady=PADY)
    placeRow([movePointButton,moveObjectButton,scaleShapeButton,deleteButton,saveFigureButton],4,0)
    changeButtonColor(drawButton)

    # Other Tools
    otherToolsLabel.grid(row = 5, column = 2, padx=PADX,pady=PADY)
    placeRow([achievementsOnButton,poincareButton,openFigureLibraryButton],6,0)

    # spacing and setup for labels
    TOOLBAR.grid_rowconfigure(8,minsize = 40) # ensures the space is kept for the labels
    selectObjectLabel.grid(row = 8, column = 1,columnspan= 3, padx=PADX, pady=PADY)
    objectSavedLabel.grid(row = 8, column = 1,columnspan=3, padx=PADX, pady=PADY)
    selectObjectLabel.grid_remove()
    objectSavedLabel.grid_remove()

    # setting up canvas bar with sliders for zoom and scale on either side of the canvas
    x = c.frameWidth - c.PLOTSIZE 
    CANVASBAR.grid_columnconfigure([0,1,9], minsize = x/3 + 5) # ensures the cells do not shift after slider is hidden
    scaleLabel.grid(row=1, column = 0, pady=PADY)
    scaleSlider.grid(row=2,column=0, pady=PADY)
    scaleSlider.set(100)
    zoomLabel.grid(row=1, column = 1, pady=PADY)
    zoomSlider.grid(row=2,column=1, pady=PADY)
    zoomSlider.set(100)
    CANVAS.get_tk_widget().grid(row = 1, column = 2, columnspan=6, rowspan=6, pady=PADY)

    # places datadisplay and show angles/metrics buttons 
    EXTRATOOLS.grid_rowconfigure(1,minsize = 60) # ensures the space is kept for the labels
    canvasInstructionsLabel.grid(row=0,column=1,columnspan=3)
    dataDisplay.grid(row = 1, column=1, columnspan=2,padx=PADX)
    placeRow([showAnglesButton,showMetricsButton,clearButton],2,0, padx=10)

    # places all root objects
    descriptLabel.grid(row=0, padx=PADX, pady=PADY)
    TOOLBAR.grid(row = 1, padx=PADX,pady=PADY)
    CANVASBAR.grid(row=2, padx=PADX)
    EXTRATOOLS.grid(row=4, padx=PADX)

    scaleSlider.grid_remove()
    scaleLabel.grid_remove()
