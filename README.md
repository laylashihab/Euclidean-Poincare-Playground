## Project Title and Description
Given a Ruler and a Straightedge.

An interactive geometry tool to visualize the interaction of shapes in a Euclidean plane and in the Poincare Disc.

## Why it's made
Inspired by the work of the ancient Egyptians, this project served as a way to strip geometry back to its very basics. Euclid's Elements focussed on defining geometric objects and setting out 5 axioms of mathematics. These axioms were assumptions that provided a basis for all other mathematical definitions and theories to be constructed atop of. In the modern era, children in grade school learn and use these ideas. The geometric assumptions people commonly make give no credit to the axioms from which they are derived. This project was born from a goal to better understand the interaction of basic geometric objects and the axioms they are built from. The first four axioms in Elements boil down to the idea that it is possible to construct shapes using a ruler/straightedge of infinite length and a compass that can produce any radius. This inspired the basic shapes available to the user: points, circles, and lines. The fifth axiom, however, stirred much mathematical debate as it does not hold true in all types of geometry. This axiom motivated the inclusion of the Poincare Disc - a model of hyperbolic geometry. 

The Poincare Disc was included to serve as an interactive tool to understand how hyperbolic geometry differs from a Euclidean one. While it is only a model, restricted especially in its angle preservations, it does provide insights to how shapes in different geometries interact in a unique and unintuitive manner.

Defining every geometric object from scratch allowed for a thorough investigation of the assumptions made in the creation of such objects. For example, the classic slope calculated from a line relies on a Euclidean distance metric. However, since hyperbolic geometry is ruled by an alternate metric, there exists different definitions of slope. 

The Achievements setting is a hat tip to the inspiration found in Euclid's Elements and helps connect the user to the work of Euclid. Different achievements mirror different definitions that Euclid formalized. 

The Tkinter framework was selected for its simplicity allowing more focus on the creation of geometric shapes and manipulations during the short timespan of this project.

## How it's made
Tech used: Python, Tkinter, Matplotlib

The geometric shapes were defined in the Point.py, Line.py, Circle.py, and Shape.py classes. Shapes were largely defined by the coordinates of their points in a coordinate plane. These shapes could be manipulated in various ways such as moving one point, many points, or changing the shape's size. All shapes may be plotted in a Euclidean mode or a Poincare mode which reflects the visuals of the shape objects in a Euclidean vs Hyperbolic model.

The Tkinter framework holds the buttons a user may interact with to perform different actions such as drawing or moving points. The window contains a Matplotlib canvas in which geometric objects are displayed. The Tkinter code is managed in FrameHandler.py.

User interactions are handled in EventHandlers.py which sets up various bindings between frame events and geometric changes. 

The app is set up and run from Main.py

The poincareDisc.py file defines an invertible mapping from the Euclidean plane to the Poincare model allowing shapes to be converted between the two models.

All constants for the project are managed in constants.py

The achievements class, Achievements.py defines how achievements can be interacted with. Specific achievements are set up in constants.py.

## Installation Instructions
$ git clone https://github.com/laylashihab/Euclidean-Poincare-Playground.git

$ cd Euclidean-Poincare-Playground

$ pip install -r requirements.txt

$ python Main.py

## Credits and acknowledgements
- Translation of [Euclid's Elements](http://aleph0.clarku.edu/~djoyce/elements/bookI/bookI.html)
- Hyperbolic Distance Metric Derivation from [Poincare Disk Distance Function](https://xnought.github.io/files/poincare-disk-distance-function.pdf)

The structure of the project and much of the inspiration for the available tools are derived from pre-existing geometric tools such as Desmos and GeoGebra.

## Known Issues and Bugs
 - Moving Line objects in the Poincare mode will not be an accurate representation of moving the points within the space. The distance between the points will not visibly change as it should when one point is dragged towards the edge. The shape should change in a similar manner to how Circle objects are altered as they approach the edge of the disk. 
 - When connecting a figure back to itself, the most recently drawn line should shift to a "snapped" position, however other lines do sometimes move instead.

