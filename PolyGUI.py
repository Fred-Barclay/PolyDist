#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Begun 20/01/2015 at 06:05 AEDT.

########################################################################
# This code (name) was written by Fred Barclay.                        #
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

import tkinter as tk
from shapely import affinity
from shapely.geometry import LinearRing, LineString, Point
import matplotlib.pyplot as plt
import xlsxwriter
from ast import literal_eval


def Dist(pt, vert, deg, d_out):

    # Sets the second x value of the 'ray' as 10000 units
    # further from the origin than the farthest-out vertice.
    x_1 = max(abs(a[0]) for a in vert) + 10000

    # Creates a "ray" (line segment, really) along the 0 degree.
    ray_main = LineString([(pt), (x_1, pt[1])])

    # Determines how many times to rotate 'ray_main'; and
    # therefore, how many distances to find.
    rot_sequence = range(0,360,deg)

    # Defines the point in Shapely that distances are calculated from.
    point = Point(pt)

    # Creates the polygon in Shapely.
    poly = LinearRing(vert)

    # Empty list to store distances in for future use.
    Distance = []

    # Empty list to store the intersections (needed for plotting).
    intersections = []

    for a in range(len(rot_sequence)):

       # Rotate "ray_main" around the point every 'deg' degrees.
       ray_rot = affinity.rotate(ray_main, rot_sequence[a], pt)

       # Find the intersection(s) of 'ray_rot' with the polygon.
       inter = poly.intersection(ray_rot)

       if inter.is_empty:
           print('No Intersection found for ray', a)

       # If there are more than 1 intersections.
       elif inter.geom_type.startswith('Multi') \
           or inter.geom_type == 'GeometryCollection':

           # If needed, group the distances together by
           # "ray_rot". See 'for' statement below:
           multidist = []

           # Find the distance from the point to each
           # intersection along 'ray_rot'.
           for multipt in inter:
               dist = point.distance(multipt)
               multidist.append(dist)
               intersections.append(list(multipt.coords))
           print('Multiple Intersections along ray',a)
           Distance.append(multidist)

       # If there is only 1 intersection.
       else:
           dist = point.distance(inter)
           intersections.append(list(inter.coords))
           Distance.append(dist)

    d_out.set(Distance)

# Define the GUI and the widgets.
def main():
	# Window and title.
    mainwin = tk.Tk()
    mainwin.title('PolyDist')
    mainwin.configure(bg = 'chartreuse2')

# Photo
    photo = '''
R0lGODlhtAC0APcAAAAAAAEBAQICAgMDAwQEBAUFBQYGBgcHBwgICAkJCQoKCgsLCwwMDA0NDQ4O
Dg8PDxAQEBERERISEhMTExQUFBUVFRYWFhgYGBkZGRoaGhsbGxwcHB0dHR4eHh8fHyAgICEhISIi
IiMjIyQkJCUlJSYmJicnJygoKCkpKSoqKisrKywsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0NDU1
NTY2Njc3Nzg4ODk5OTo6Ojs7Ozw8PD09PT4+Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdHR0hI
SElJSUtLS0xMTE1NTU5OTk9PT1BQUFFRUVJSUlNTU1RUVFVVVVZWVlhYWFlZWVpaWltbW1xcXF1d
XV5eXl9fX2BgYGFhYWJiYmNjY2RkZGZmZmdnZ2hoaGlpaWpqamtra2xsbG1tbW5ubm9vb3BwcHFx
cXNzc3R0dHV1dXZ2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CAgIGBgYKCgoODg4SEhIWF
hYaGhoeHh4iIiImJiYqKiouLi4yMjI6Ojo+Pj5CQkJGRkZKSkpOTk5SUlJWVlZeXl5iYmJmZmZqa
mpycnJ2dnZ6enp+fn6CgoKGhoaKioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqqurq6ysrK2tra6u
rq+vr7CwsLGxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8DAwMHB
wcLCwsTExMXFxcbGxsfHx8jIyMnJycrKysvLy8zMzM3Nzc7Ozs/Pz9HR0dLS0tPT09TU1NXV1dbW
1tfX19jY2NnZ2dra2tvb29zc3N3d3d7e3t/f3+Dg4OHh4eLi4uPj4+Tk5OXl5ebm5ufn5+jo6Onp
6erq6uzs7O3t7e7u7u/v7/Dw8PHx8fLy8vPz8/T09PX19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39
/f7+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAQAAAAALAAAAAC0ALQA
AAj+AOkJHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNq3Mixo8ePIEOKHEmypMmTKFOqXMmypcuX
MGPKnEmzps2bOHPq3Mmzp8+fQIMKHUq0KL13SLnRWsq0qdNdSNW9M0o14Tty4ECBCgSgq9evYMN2
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'''

    pyworks = tk.PhotoImage(data = photo)

    disp = tk.Label(mainwin, image = pyworks).pack()

    # SubPoint Entry
    tk.Label(mainwin, text = 'SubPoint: ', bg = 'chartreuse2', fg = \
        'black').pack()

    stup = tk.StringVar()
    tk.Entry(mainwin, textvariable = 'spt').pack()

    # Vertices Entry
    tk.Label(mainwin, text = 'Vertices List: ', bg = 'chartreuse2', fg = \
        'black').pack()

    vlist = tk.StringVar()
    tk.Entry(mainwin, textvariable = 'vlist').pack()

    # Degree of rotation Entry
    tk.Label(mainwin, text = 'Degrees to Rotate: ', bg = 'chartreuse2', fg = \
        'black').pack()

    dint = tk.StringVar()
    tk.Entry(mainwin, textvariable = 'dint').pack()

    # Convert from StringVar.
    stup = literal_eval(stup.get())
    vlist = literal_eval(vlist.get())
    dint = literal_eval(dint.get())

    # Calculate!
    tk.Button(mainwin, text = 'Find It!', command = Dist(stup,\
        vlist, dint, d_out)).pack()

    # I don't know precisely what I'm doing here:
    d_out = tk.StringVar()




    mainwin.mainloop()

if __name__ == "__main__":
    main()
