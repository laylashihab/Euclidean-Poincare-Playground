from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


# plot function is created for 
# plotting the graph in 
# tkinter window
def plot(x_data,y_data):

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
                 dpi = 100)

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(x_data,y_data)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = root)  
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# function to deal with user clicking.
def click_handler(event):
    x = event.x
    y = event.y
    print(x,y)

#main window setup
root = Tk()
root.geometry("500x500")
root.title('Euclidean Playground')
root.bind("<Button>", click_handler)

descriptLabel = Label(root, text="You have been given a straightedge and a compass")
descriptLabel.pack()

x = np.linspace(0,10,100)
y = np.linspace(0,10,100)
plot(x,x**2)



root.mainloop()
