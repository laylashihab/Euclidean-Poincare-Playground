from Point import *
from Line import *
from Circle import *
from Shape import *

import FrameSetUp
import EventHandlers
import constants as c

""""
Class to define variables that are used throughout the program and run the program
"""
class Main:

    def __init__(self):
        self.achievementsOn = False

        # sets the epsilon value for points (allowable error for .equals)
        Point.setEpsilon(20)

        # set up the frame and eventHandlers
        FrameSetUp.setUp(self)
        EventHandlers.bindEvents(self)

        # sets dps and lw
        Point.setDPS(c.DEFAULTPOINTSIZE)
        
    def run(self):
        FrameSetUp.ROOT.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()

