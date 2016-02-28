PolyDist README.
PolyDist version 0.11

Contributors:
Fred Barclay
Inspired by Matlab (R) code written by the author and W. Scott Ingram for the
University of Texas M. D. Anderson Cancer Center. This code is not affiliated
with M. D. Anderson Cancer Center and is clean of any code authored or owned by
this institution.

Requires:
Python 3.4
Matplotlib 1.4.2
Shapely 1.4.3
Xlsxwriter 0.5.2

Tested up to:
Python 3.4.2
Matplotlib 1.4.2
Shapely 1.4.3
Xlsxwriter 0.5.2

================================================================================
License is provided in the code and reproduced here:
########################################################################
# This code (PolyDist) was written by Fred Barclay.                    #
# You may:                                                             #
# (a). Use this code as you see fit.                                   #
# (b). Modify this code as needed.                                     #
# You may not:                                                         #
# (a). Change the text within this comment box or modify the box in    #
#      any way (this also means you may not remove the box.)           #
# (b). Claim original authorship. Any additional authors or modifiers  #
#      may be named as such.                                           #
#                                                                      #
# Usage of this code is at your own risk. Notwithstanding any other    #
# guarantees in any part of the code, the author of the original code, #
# known as Fred Barclay, is and shall be in no way responsible for any #
# damages arising from the use of this code. By using this code, you   #
# accept these terms and all responsibilities.                         #
########################################################################


================================================================================
PolyDist calculates the distances from a main point to other points (subpoints)
along the perimeter of a 2-dimensional field. The subpoints are not
user-defined; however, their frequency and spacing is.


================================================================================
Description:
PolyDist defines a main point and a polygon using a tuple and a list of tuples.
The tuple defines a point; the list defines the vertices of the polygon. The
user also provides a integer as the degrees that a ray radiating from the main
point should be rotated in an anti-clockwise fashion.

At each rotation of the ray, it intersects the perimeter of the polygon at a
discrete point, or (for irregular polygons) at multiple discrete points. The
distance(s) from the main point to these subpoints is then calculated and
returned.

Additionally, a graph is returned of the figure and and .xlsx spreadsheet is
created (inside the working directory) containing the distances.

For example, say I have point (3,5) that is contained inside a field whose
perimeter is (0,0), (0,9), (4,7), (8,8), and (6,2). I also want the
intersections (subpoints) to be set every 15 degrees:

python3 PolyDist.py
"Main point coordinates:" (3,5)
"Vertices coordinates:" [(0,0),(0,9),(4,7),(8,8),(6,2)]
"Angle of rotation:" 15

At this point the code should execute and return the distances, a graph of the
figure, and an .xlsx file containing the distances.


================================================================================
Notes:
While my goal is to use a true ray to intersect the perimeter, I was unable to
integrate one with Shapely. Therefore, I have used a long line segment that I
believe will serve for the time being.

Both regular and irregular polygons are supported.

================================================================================
Revision History:
0.21 Restored imports of xlsxwriter and matplotlib.pyplot to all instances.

0.2	 Corrected spelling in license, made creating an .xlsx spreadsheet and/or
     plotting a graph optional, and consistently used single quotes ('') for
     strings instead of double quotes. Importing xlsxwriter and matplotlib.pyplot 
	 were only triggered if the user chose to export the data to a spreadsheet or 
	 plot the figure, respectively, saving startup time.
     Edited README.md.

0.1  Removed the need for a Python function and migrated to a dot decimal point
     in documentation, as well as improved code commenting.

0,02 Set the .xlsx file to be created before the graph. Previously, the graph
	 had to be closed before the spreadsheet was created.

0,01 Initial release.


================================================================================
Roadmap:
(Not in any particular order)
1. Possibly move to .odt format instead of .xlsx.
2. Add GUI functionality.
3. Use a true ray instead of a really long line segment.
4. Have the .xlsx returned as a cascading filename, instead of overwriting the
   same file every run.
5. Let the user define the .xlsx file name (negate item 4).
6. Improve the README.
7. Improve colouring on the graph.


================================================================================
Contact info:
For bugs, please contact me at BugsAteFred@gmail.com, or through GitHub. You're
welcome to submit patches (or, as I like to call them, "bug squashers") as well!

For suggestions/queries/improvements, I'm still unsure of what the preferred
method of contact is. Just follow the same steps as bug squashing outlined
above.


================================================================================
Final thoughts:

If it ain't broke, fix it until it is!
