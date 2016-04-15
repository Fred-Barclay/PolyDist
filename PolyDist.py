#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Begun on Wed May 27 11:01:28 2015

########################################################################
# This code (PolyDist) was written by Fred Barclay.                    #
# You may:                                                             #
# (a). Use this code as you see fit.                                   #
# (b). Modify this code as needed.                                     #
# (c). Redistribute copies, whether modified or unchanged, freely.     #
#                                                                      #
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

# PolyDist.py
# Version 0.2.3 RC
#
#
# This code was written in Python 3.
#
# Please email all complaints, comments, suggestions, or bugs to
# BugsAteFred@gmail.com or contact me through github.
#
# Dependencies are shapely, matplotlib, and xlsxwriter.
from shapely import affinity
from shapely.geometry import LinearRing, LineString, Point
from ast import literal_eval
import xlsxwriter
import matplotlib.pyplot as plt

# User Input
pt = input('Main point coordinates: ')
vert = input('Vertices coordinates: ')
deg = int(input('Angle of rotation: '))

# Change from string to numerical value.
pt = literal_eval(pt)
vert = literal_eval(vert)

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

print('Distance =',Distance)


#++++++++++++Export to Excel/Calc

xL = input('\nExport data to .xlsx file? y/N ')

if xL == 'y' or xL == 'Y':

    workbook = xlsxwriter.Workbook('PolyDist.xlsx')
    worksheet = workbook.add_worksheet()

    for s in range(len(Distance)):
        try:
            if len(Distance[s]) != 1:
                for t in range(len(Distance[s])):
                    worksheet.write( s, t, Distance[s][t])
        except TypeError:
            worksheet.write( s, 0, Distance[s])

    workbook.close()
    print('Data exported sucessfully!')

#++++++++++++++++Plotting Segment!
u_plot = input('\nPlot figure on unit graph? y/N ')

if u_plot == 'y' or u_plot == 'Y':

    # Vertices
    plt.plot([f[0] for f in list(poly.coords)],
             [f[1] for f in list(poly.coords)],'b*-' )

    # "...and so my Main Point is this:"
    plt.plot(pt[0], pt[1], 'ro')

    #

    # Intersections
    plt.plot([g[0][0] for g in intersections], [g[0][1] for g in
        intersections],'g^' )

    # Rays
    for h in range(len(intersections)):
        plt.plot([ pt[0], intersections[h][0][0]], [pt[1],
          intersections[h][0][1]], 'r--')

    # Make the coordinate plane 3 units larger than the polygon.
    plt.axis([min(i[0] for i in vert) - 3, max(i[0] for i in vert)
        + 3, min(i[1] for i in vert) - 3, max(i[1] for i in vert) +
        3 ])

    # Grid
    plt.grid()

    # two for the Show
    plt.show()
