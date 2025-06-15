from Point import *
from Line import *
from Circle import *
from Shape import *
from Achievement import *

from tkinter import Button,Label,Frame

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

# clears the plot
def clear(Main):

    plot1 = Main.plot1
    plot_size = Main.plot_size
    canvas = Main.canvas

    changeToolMode("Draw")
    changeButtonColor(drawButton)
    changeShape("Point")
    changeButtonColor(pointButton)

    EventHandlers.shapeList = []
    plot1.cla()
    plot1.set_xlim(0,plot_size)
    plot1.set_ylim(0,plot_size)
    plot1.set_axis_off()
    canvas.draw()

def showAngles(Main):
    plot1 = Main.plot1
    canvas = Main.canvas

    if (showAnglesButton.cget("text")) == "Show Angles":
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.showAngles(plot1,canvas)
        showAnglesButton.config(text= "Hide Angles")

    else:
        for shape in EventHandlers.shapeList:
            if (type(shape) == Shape):
                shape.hideAngles(canvas)
        showAnglesButton.config(text= "Show Angles")


def setUp(Main):
    root = Main.root
    tb = Main.tb
    dataDisplay = Main.dataDisplay
    plot1 = Main.plot1
    canvas = Main.canvas
    padx=Main.padx
    pady=Main.pady
    plot_size = Main.plot_size
    achievementsOn = Main.achievementsOn

    global toolLabel
    global shapeLabel
    global operationLabel
    global pointButton
    global lineButton
    global circleButton
    global clearButton
    global moveButton
    global deleteButton
    global selectButton
    global drawButton
    global showAnglesButton

    #main window setup
    root.geometry("600x700")
    root.title('Euclidean Playground')
    descriptLabel = Label(root, text="You have been given a straightedge and a compass")
    toolbar = Frame(root)
    toolLabel = Label(toolbar, text="Toolbar")
    shapeLabel = Label(toolbar, text="Shape Library")
    operationLabel = Label(toolbar, text="Operations")
    pointButton = Button(toolbar, command=lambda: [changeShape("Point"), changeButtonColor(pointButton)], height = 2, width = 10, text = "Point")
    lineButton = Button(toolbar, command=lambda: [changeShape("Line"), changeButtonColor(lineButton)], height = 2, width = 10, text = "Line")
    circleButton = Button(toolbar, command =lambda: [changeShape("Circle"),changeButtonColor(circleButton)], height = 2, width = 10, text = "Circle")
    clearButton = Button(toolbar,command=lambda:[clear(Main)],height = 2, width = 10, text = "Clear")
    moveButton = Button(toolbar,command =lambda: [changeToolMode("Move"),changeButtonColor(moveButton)],height = 2, width = 10, text = "Move Point")
    deleteButton = Button(toolbar,command =lambda: [changeToolMode("Delete"),changeButtonColor(deleteButton)],height = 2, width = 10, text = "Delete Object")
    selectButton = Button(toolbar,command =lambda: [changeToolMode("Select"),changeButtonColor(selectButton)],height = 2, width = 10, text = "Select Object")
    drawButton = Button(toolbar, command = lambda:[changeToolMode("Draw"),changeButtonColor(drawButton)],height = 2, width = 10, text = "Draw")
    showAnglesButton = Button(toolbar, command= lambda: [showAngles(Main)],height = 2, width = 10, text = "Show Angles")

    global shapeButtonList
    global operationButtonList

    shapeButtonList = [pointButton,lineButton,circleButton]
    operationButtonList = [moveButton,deleteButton,selectButton,drawButton]
    # description setup
    descriptLabel.pack()

    # tool setup
    row = 0
    toolLabel.grid(row=row, column=1, padx=padx, pady=pady)
    row += 1
    shapeLabel.grid(row=row, column=1, padx=padx, pady=pady)
    row += 1
    if (achievementsOn == False):
        pointButton.grid(row=row,column=1, padx=padx, pady=pady)
        changeButtonColor(pointButton)
        lineButton.grid(row=row,column=2, padx=padx, pady=pady)
    circleButton.grid(row=row,column=3, padx=padx, pady=pady)

    row +=1 
    operationLabel.grid(row=row, column = 1, padx=padx, pady=pady)
    row += 1
    moveButton.grid(row=row,column=1, padx=padx, pady=pady)
    deleteButton.grid(row=row,column=2, padx=padx, pady=pady)
    selectButton.grid(row=row, column = 3, padx=padx, pady=pady)
    drawButton.grid(row=row, column=4, padx=padx, pady=pady)
    changeButtonColor(drawButton)

    row += 1
    clearButton.grid(row=row,column=0, padx=padx, pady=pady)
    showAnglesButton.grid(row=row,column = 1,padx=padx,pady=pady)
    toolbar.pack()


    # creating the Tkinter canvas containing the Matplotlib figure
    canvas.get_tk_widget().config(width=plot_size,height=plot_size)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # adding the subplot
    plot1.set_xlim(0,plot_size)
    plot1.set_ylim(0,plot_size)
    plot1.set_axis_off()

    # creating the Matplotlib toolbar
    tb.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

    # data display setup
    dataDisplay.pack()

toolLabel = None
shapeLabel = None
operationLabel = None
pointButton = None
lineButton = None
circleButton = None
clearButton = None
moveButton = None
deleteButton = None
selectButton = None
drawButton = None
showAnglesButton = None

shapeButtonList = None
operationButtonList = None

