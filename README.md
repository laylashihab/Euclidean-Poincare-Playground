## Project Description
Given a Ruler and a Straightedge.

An interactive geometry tool to visualize the interaction of shapes in a Euclidean plane and in the Poincare Disc.

## Project Inspiration
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

$ pip install -r requirements.txt

$ python Main.py

## Credits and acknowledgements
- Translation of [Euclid's Elements](http://aleph0.clarku.edu/~djoyce/elements/bookI/bookI.html)
- Hyperbolic Distance Metric Derivation from [Poincare Disk Distance Function](https://xnought.github.io/files/poincare-disk-distance-function.pdf)
- Hyperbolic Distance [Math Stack Exchange](https://math.stackexchange.com/questions/3910376/how-to-determine-distance-between-two-points-in-poincare)
- Find Circle Intersection [Math Stack Exchange](https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect)

The structure of the project and much of the inspiration for the available tools are derived from pre-existing geometric tools such as Desmos and GeoGebra.

## How to Use
Select one of the three shape types in the top of the window to draw the selected shape. To draw a point, select "Point" and click on the canvas where you would like the point. To draw a line, select "Line" and click and drag the mouse on the canvas. To draw a circle, click to draw the center point and drag to set the radius. 

The "Move Point" button allows the user to click on a plotted point and drag it to a new location. Only that point will move. Lines/circles will adjust accordingly.

The "Move Object" button allows the user to click on a plotted point from a shape and drag it to a new location. The entire shape containing point will move.

The "Scale" button will trigger a slider to pop up to the left of the window. The user must click on an shape. That shape will become bold and the user can scale the shape using the slider.

The "Delete Object" button allows the user to click on any shape and that shape will be deleted from the canvas.

The "Save Figure" button allows the user to click on any shape to save that shape. 

The "Achievements On/Off" button allows the user to switch achievements feature on or off. When a user completes an achievement, a pop-up will describe their achievement. All achievements are based on definitions from Euclid's Elements.

The "Poincare Disc" button will transform the current Euclidean plane into the poincare disc model. All points are mapped to a new location within the disc and shapes are drawn in accordance with the model. To return from the model back to the Euclidean plane, the button will change its text to read "Euclidean Plane"

The "Open Figure Library" button will open a new window featuring any shapes that have been saved. The user has the option to delete such shapes from the list or add the shapes to the canvas.

The "Zoom" slider allows the user to zoom in and out of the canvas. No shapes are altered in this interaction.

The user may use the arrow keys on their keyboard at any time to navigate left or right on canvas. In the Poincare model, the user navigates to the left and right of the model, rather than the plane in which the model is embedded.

The "Show/Hide Angles" Button will show the value of any angles that have been drawn in the canvas.

The "Show/Hide Metrics" Button will show any length values on lines that have been drawn in the canvas.

The "Clear" button will clear all drawn shapes from the canvas.

NOTE: to select any shape, the user must click on one of its points

## Known Issues and Bugs
- still searching! 
- if you find any bugs or issues, please let me know at laylashihab60@gmail.com

## Fixed Bugs and Issues
 - Circle center points near boundary do not properly map between Euclidean and Poincare mode (Fixed 8/13/25)
 - Moving Line objects in the Poincare mode will not be an accurate representation of moving the points within the space. The distance between the points will not visibly change as it should when one point is dragged towards the edge. The shape should change in a similar manner to how Circle objects are altered as they approach the edge of the disk. (Fixed 8/13/25)
 - Moving Shapes in Poincare mode will allow for points to move outside of the circle; only checks that the point the user clicks on is inside the circle (Fixed 8/13/25)
 - Objects on or close to the boundary in Poincare mode will not be properly mapped during a conversion back to Euclidean mode. (Fixed 8/13/25) 
 - When connecting a figure back to itself, the most recently drawn line should shift to a "snapped" position, however other lines do sometimes move instead. (Fixed 8/13/25)
