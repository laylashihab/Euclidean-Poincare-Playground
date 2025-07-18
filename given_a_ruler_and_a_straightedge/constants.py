from Achievement import *

# Tool Modes
DRAW = 1
MOVEPOINT = 2
DELETE = 3
MOVEOBJECT = 4
SELECT = 5
SCALE = 6

# Shape Types
POINT = 0
LINE = 1
CIRCLE = 2
SHAPE = 3

# achievements
"""
All definitions come from a translation of Euclid's Elements
source:
http://aleph0.clarku.edu/~djoyce/elements/bookI/bookI.html
"""
ACHIEVEMENTSDICT = {}
ACHIEVEMENTSDICT["createPoint"] = Achievement("Define a Point", "A point is that which has no part.")
ACHIEVEMENTSDICT["createLine"] = Achievement("Define a Line", "A line is breadthless length.\nThe ends of a line are points.\n" \
"A straight line is a line which lies evenly with the points on it")
ACHIEVEMENTSDICT["createAngle"] = Achievement("Define a Plane Angle", "A plane angle is the inclination to one another of two lines in a plane " \
"which meet one another and do not lie in a straight line.")
ACHIEVEMENTSDICT["createAcuteAngle"] = Achievement("Define an Acute Angle", "An acute angle is an angle less than a right angle.")
ACHIEVEMENTSDICT["createRightAngle"] = Achievement("Define a Right Angle", "When a straight line standing on a straight line makes the adjacent angles" \
" equal to one another, each of the equal angles is right")
ACHIEVEMENTSDICT["createPerpendicularLines"] = Achievement("Define Perpendicular Lines", "When a straight line standing on a straight line makes the adjacent angles " \
"equal to one another, the straight line standing on the other is called a perpendicular to that on which it stands")
ACHIEVEMENTSDICT["createObtuseAngle"] = Achievement("Define an Obtuse Angle", "An obtuse angle is an angle greater than a right angle")
ACHIEVEMENTSDICT["createCircle"] = Achievement("Define a Circle","A circle is a plane figure contained by one line such that all the straight lines falling " \
"upon it from one point among those lying within the figure equal one another.\nAnd the point is called the center of the circle.")


# frame/window settings
PADX = 5
PADY = 5
PLOTSIZE = 400
PLOTBOUNDS = 5
DEFAULTPOINTSIZE = 50
THINLINE = 1
THICKLINE = 3
EPSILON = 1