from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from Point import *
from Line import *
from Circle import *
from Shape import *
from Achievement import *

import FrameSetUp
import EventHandlers

""""
Class to define variables that are used throughout the program and run the program
"""

class Main:
    def __init__(self):
        # sets the epsilon value for points (allowable error for .equals)
        Point.setEpsilon(20)

        # achievements
        """
        All definitions come from a translation of Euclid's Elements
        source:
        http://aleph0.clarku.edu/~djoyce/elements/bookI/bookI.html
        """
        self.achievementsDict = {}
        self.achievementsDict["createPoint"] = Achievement("Define a Point", "A point is that which has no part.")
        self.achievementsDict["createLine"] = Achievement("Define a Line", "A line is breadthless length.\nThe ends of a line are points.\n" \
        "A straight line is a line which lies evenly with the points on itself.")
        self.achievementsDict["createAngle"] = Achievement("Define a Plane Angle", "A plane angle is the inclination to one another of two lines in a plane " \
        "which meet one another and do not lie in a straight line.")
        self.achievementsDict["createAcuteAngle"] = Achievement("Define an Acute Angle", "An acute angle is an angle less than a right angle.")
        self.achievementsDict["createRightAngle"] = Achievement("Define a Right Angle", "When a straight line standing on a straight line makes the adjacent angles" \
        " equal to one another, each of the equal angles is right")
        self.achievementsDict["createPerpendicularLines"] = Achievement("Define Perpendicular Lines", "When a straight line standing on a straight line makes the adjacent angles " \
        "equal to one another, the straight line standing on the other is called a perpendicular to that on which it stands")
        self.achievementsDict["createObtuseAngle"] = Achievement("Define an Obtuse Angle", "An obtuse angle is an angle greater than a right angle")
        self.achievementsDict["createCircle"] = Achievement("Define a Circle","A circle is a plane figure contained by one line such that all the straight lines falling " \
        "upon it from one point among those lying within the figure equal one another.\nAnd the point is called the center of the circle.")

        
        self.achievementsOn = False

        # the figure that will contain the plot
        self.fig = Figure(figsize = (5, 5), dpi = 100, constrained_layout=True)
        self.root = Tk()

        self.plot1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)  

        # frame/window settings
        self.padx = 10
        self.pady = 5
        self.plot_size = 400

        self.tb = NavigationToolbar2Tk(self.canvas, self.root)
        self.dataDisplay = Label(self.root, text="")

        # set up the frame and eventHandlers
        FrameSetUp.setUp(self)
        EventHandlers.bindEvents(self)
        

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()

