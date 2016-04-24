#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PolyDist.py (Multi-point distance finder)
# Copyright (C) 2015,2016 Fred Barclay (https://github.com/Fred-Barclay);
# (BugsAteFred@gmail.com)
#
# Dual-licensed under the GPL v2 and custom license terms.
# GPL v2:
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Custom license terms:
#   You are hereby granted a perpetual, irrevocable license to copy, modify,
#   publish, release, and distribute this program as you see fit. However,
#   under no circumstances may you claim original authorship of this program;
#   you must credit the original author(s). You may not remove the listing of
#   the original author(s) from the source code, though you may change the
#   licensing terms. If you publish or release binaries or similarly compiled
#   files, you must credit the author(s) on your home and/or distribution page,
#   whichever applies. In your documentation, you must credit the author(s) for
#   the portions of their code you have used. This, of course, does not revoke
#   or change your right to claim original authorship to any portions of the
#   code that you have written.
#
#   You must agree to assume all liability for your use of the program, and to
#   indemnify and hold harmless the author(s) of this program from any liability
#   arising from use of this program, including, but not limited to: loss of
#   data, death, dismemberment, or injury, and all consequential and
#   inconsequential damages.
#
#   For clarification, contact Fred Barclay:
#       https://github.com/Fred-Barclay
#       BugsAteFred@gmail.com
#
# Written in Python 3.
#
# Please email all complaints, comments, suggestions, questions, or bugs to
# BugsAteFred@gmail.com or contact me through GitHub.
#
# Dependencies are shapely, matplotlib, and xlsxwriter. You can get by with only
# shapely if you either:
#   (a). Answer "N" when prompted to graph and export to a spreadsheet (default
#        option) and comment out lines 63-64, or
#   (b). Comment out lines 63-64 and 135-189.
#
# Version 0.2.3 RC
#
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

#	Rotate "ray_main" around the point every 'deg' degrees.
	ray_rot = affinity.rotate(ray_main, rot_sequence[a], pt)

#	Find the intersection(s) of 'ray_rot' with the polygon.
	inter = poly.intersection(ray_rot)

	if inter.is_empty:
		print('No Intersection found for ray', a)

#	If there are more than 1 intersections.
	elif inter.geom_type.startswith('Multi') \
	or inter.geom_type == 'GeometryCollection':

#		If needed, group the distances together by
#		`ray_rot`. See 'for' statement below:
		multidist = []

#		Find the distance from the point to each
#		intersection along 'ray_rot'.
		for multipt in inter:
			dist = point.distance(multipt)
			multidist.append(dist)
			intersections.append(list(multipt.coords))
		print('Multiple Intersections along ray',a)
		Distance.append(multidist)

#	If there is only 1 intersection.
	else:
		dist = point.distance(inter)
		intersections.append(list(inter.coords))
		Distance.append(dist)

print('Distance =',Distance)


#++++++++++++Export to Excel/Calc

xL = input('\nExport data to .xlsx spreadsheet? y/N ')

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

#	Vertices
	plt.plot([f[0] for f in list(poly.coords)],
			[f[1] for f in list(poly.coords)],'b*-' )

#	"...and so my Main Point is this:"
	plt.plot(pt[0], pt[1], 'ro')

#	Intersections
	plt.plot([g[0][0] for g in intersections], [g[0][1] for g in
		intersections],'g^' )

#	Rays
	for h in range(len(intersections)):
		plt.plot([ pt[0], intersections[h][0][0]], [pt[1],
			intersections[h][0][1]], 'r--')

#	Make the coordinate plane 3 units larger than the polygon.
	plt.axis([min(i[0] for i in vert) - 3, max(i[0] for i in vert)
		+ 3, min(i[1] for i in vert) - 3, max(i[1] for i in vert) +
		3 ])

#	Grid
	plt.grid()

#	two for the Show
	plt.show()

	print('Figure graphed sucessfully!')
