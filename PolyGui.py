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
# PolyDist.py
# Version 1.0 RC

import tkinter as tk
from shapely import affinity
from shapely.geometry import LinearRing, LineString, Point
import matplotlib.pyplot as plt
import xlsxwriter
from ast import literal_eval

# Calculate the distances
def PolyDist(pt, vert, deg, D_out):
	pt = literal_eval(pt)
	vert = literal_eval(vert)
	deg = literal_eval(deg)

#	Sets the second x value of the 'ray' as 10000 units
#	further from the origin than the farthest-out vertice.
	x_1 = max(abs(a[0]) for a in vert) + 10000

#	Creates a "ray" (line segment, really) along the 0 degree.
	ray_main = LineString([(pt), (x_1, pt[1])])

#	Determines how many times to rotate 'ray_main'; and
#	therefore, how many distances to find.
	rot_sequence = range(0,360,deg)

#	Defines the point in Shapely that distances are calculated from.
	point = Point(pt)

#	Creates the polygon in Shapely.
	poly = LinearRing(vert)

#	Empty list to store distances in for future use.
	Distance = []

#	Empty list to store the intersections (needed for plotting).
	intersections = []

	for a in range(len(rot_sequence)):

#		Rotate "ray_main" around the point every 'deg' degrees.
		ray_rot = affinity.rotate(ray_main, rot_sequence[a], pt)

#		Find the intersection(s) of 'ray_rot' with the polygon.
		inter = poly.intersection(ray_rot)

		if inter.is_empty:
			print('No Intersection found for ray', a)

#		If there are more than 1 intersections.
		elif inter.geom_type.startswith('Multi') \
		or inter.geom_type == 'GeometryCollection':

#			If needed, group the distances together by
#			`ray_rot`. See 'for' statement below:
			multidist = []

#			Find the distance from the point to each
#			intersection along 'ray_rot'.
			for multipt in inter:
				dist = point.distance(multipt)
				multidist.append(dist)
				intersections.append(list(multipt.coords))
			print('Multiple Intersections along ray',a)
			Distance.append(multidist)

#		If there is only 1 intersection.
		else:
			dist = point.distance(inter)
			intersections.append(list(inter.coords))
			Distance.append(dist)

#	D_out.set(Distance)
	print(D_out)
################################################################################
# # Define the GUI window.
def main():
	mainwin = tk.Tk()
	mainwin.title('PolyGUI')


#	Menu Bar.
	menubar = tk.Menu(mainwin)

#	File menu
	filemenu = tk.Menu(menubar, tearoff = 0)
#	filemenu.add_separator()
	filemenu.add_command(label = 'Exit', command = mainwin.quit)
	menubar.add_cascade(label = 'File', menu = filemenu)

#	Help menu
	helpmenu = tk.Menu(menubar, tearoff = 0)
	helpmenu.add_command(label = 'Documentation', command = docs)
	helpmenu.add_command(label = 'About', command = aboutme)
	menubar.add_cascade(label = 'Help', menu = helpmenu)

#	Display the menu
	mainwin.config(menu=menubar)

#	Display window
	canvas = tk.Canvas()
	canvas.configure(width = 400, height = 100)
	canvas.pack()

#	SubPoint Entry
	tk.Label(mainwin, text = 'SubPoint: ', bg = 'chartreuse2', fg = \
		'black').pack()

	mainpoint = tk.StringVar()
	tk.Entry(mainwin, textvariable = mainpoint).pack()

#	Vertices Entry
	tk.Label(mainwin, text = 'Vertices List: ', bg = 'chartreuse2', fg = \
		'black').pack()

	vertices = tk.StringVar()
	tk.Entry(mainwin, textvariable = vertices).pack()

#	Degree of rotation Entry
	tk.Label(mainwin, text = 'Degrees to Rotate: ', bg = 'chartreuse2', fg = \
		'black').pack()

	degrees = tk.StringVar()
	tk.Entry(mainwin, textvariable = degrees).pack()

#	Calculate
	tk.Button(mainwin, text = 'Find It!', command = lambda: \
		PolyDist(mainpoint.get(), vertices.get(), degrees.get(), Dist)).pack()

# ANSWERS?????
	Dist = tk.StringVar()

#	Loop the program.
	mainwin.mainloop()

################################################################################
# The 'About Me' GUI window
def aboutme():
	aboutwin = tk.Toplevel()
	aboutwin.title('About PolyDist')

	aboutwin.geometry('400x200')

# 	photo = '''\
# iVBORw0KGgoAAAANSUhEUgAAAGQAAABOCAYAAADW1bMEAAAABGdBTUEAALGPC/xhBQAAACBjSFJN
# AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAA
# CXBIWXMAAA9hAAAPYQGoP6dpAAAAB3RJTUUH4AMREyki+tM4LgAAGX9JREFUeNrtXHlwU/ed/7xD
# T7IOy6ds2QaMMdjG5gYDAewACdA2Idsck2S72XYz07vbSXfbTabTnc3s7HQy+Se90mbbdNu022k2
# TUggF0kgHIZAAuEKYGODARvbGNuyZVmXpae3f3z88mxLtmSwgbR8ZzS2pPd+7/e+5+d7PAmapmm4
# RTcNiTd6A7doJN0SyE1GCQWiaRo0LTahhVRVndDxV3ONm5Mm9z7k0R/EYjEcPHgGHk8YlZWV0DRT
# 0kVCg/04cOo1rJp3HxTZlvR4QYihtfUsLnddwuYvrITFknadmThZpKG+vgX19ZexadM8WK3Wa14x
# TiCaFsVf/tKCc+fCeOyxUsiyCeOFfUkEdhzbjd8d+iG+ccWNNVV3Qk2iMKKo4aWXTmH/kZ8hf8aT
# qFlae6M5e9W0a1crnn++A0VFM1BdPQUCkSQF69ZXYuOmMNats6e0SMyeDvu0x7CqxIqV81M5Q0LA
# E4PW2ozfvX4ATrkW8+YD4mcuoglYtGgBHn98Njo6cnD4MLBoESBJ17BiItj77NbfwePvxL8//AQg
# pLBKLAZ09QC5OYCYyglAsKMdwa7L8OfOwOkTWZBlAatWARbLjWLu1dHx47z9qipg714gGgXWrAGu
# 1nvF6aTP58M79W/i7ca30X6lPbVVBgeBDw8A0UjKF05zFyBr/mJMc2fjjjsEOJ3A228D3d03hK9X
# Tbo6m0zA2rVAfj7vo7Pz6taLc1lWqwVfqXwa9rbTyE5LMdgKApCezr+pkNcLdHUBpaUAaOJLlwI5
# OcCuXcDChcDs2debtddOoggsWABkZwN1dUBlJVBenjpbgAQWIkkmFLhKME2zw9yVoroqCrBqFdUk
# FWpqAvr64j4uLgbuvBOorwcOHKD5fxapqAjYuBFobgb27QMG/IMIhUIpnZs4DwGAiorUGQwAqgqk
# WoVxOMY0gYwMYNMmesF33wV8PkCLffbyFYeDQlEk4Oc/2YIX3/9TSuclxjUxAHl5wPTi1K4+OAjs
# 35+6SpeVAU7nmF8rClBTA8yYAWx73YffvvYSgqHAdWTnJFA4DBlRVFb0obnn1/jN/t/jTFNX0tPk
# Mb8RAPR0AdEYhTMeaRoQDKa20dZWxptxBALQ71ZWAkcv7cEPX/835Oa4cM+adamhvhtJsRjwySfA
# hQvA6tWQ7DZ89atPIRhUceK4BYEBoLIyApNJhpAguIyN/AUAoRBw9GjyTSgKsGIFIMvjH6eqwMcf
# c9OpkMeDgtgAvrv2a2htlrF7DxAO3zheJyJN0xCNRIDebmBggB86ncC6dUB2NtLMFlRXVKN28Urc
# fZcDjY0e/OAHe3D8+LmE640tkBiA/DzA5UruikSRECkZnBgcpB/KyEh+p6EQsGcP1i2owY/u+xG+
# +UgNrFZCSo/nxglgNPWHGnHslf8A6vZTW0SR6MThiDvWYgGWLQvj0KEBnDvXn5iV415NUph6JtP8
# SAQ4dowWMB6lpRHTpoIDg0Fg7lygoIBbkYDqamD+fGDnTuDcueRLTBmFQrzfllbsPP9n/CT4R9SX
# lxDvJqGCgjx861trsX59ZcLvkxcrolGgpWV8BKWqwMWL4wsklXV0ikRoRWVlcV+VlADr1wMnTwIf
# fphcByadNI1JRnMzYmlmFFtq8KXFT8PmSE/pdEkS4XA4YbGYE34vJ11BEIAjRxiIx3I1sgzMmTN+
# EefyZeDUKWD69PGvd+UKj6utHdOSsrIIjT/4AHjvPWBWWQemuTOmrmrc0wN89BH3XllJCKgoEAUB
# S2atgxYDprsn51LJLUSWmVEHAuMfU1ExvkBCoYQaP4I0jcIoLk5aaTSbgdtvB/IyB/Djp36IPSd2
# Tw5HdFJVxjwAOHsWsNu5L/3iQ8qiaUN52yRRcgsBqBXJNn/5MuB2j83IWbNS29Hy5Yw1KZAgAOa0
# evgtR/G/7+ShMG0DKqukCZUqEtLFi3RLZWXAsmUMXte8aGqUmkAEgbUnmy1xGTMSAQ4fBj73OULg
# 0eTzMYZkZo59jbY2CiIrK7WdX7gAKApmzKnCM//+FtSwCZ8cE9DjAVauTLyNccnvJ5DIyaFlLF8O
# zJxp3P91otQ7EBcvAmfOjLGKSGaPZR1HjlCgY1FvL4tXqTYSzp0jyrFaYbOkoTCnANMLc7Fxowiz
# mdC4t3cCXKivB/70JwoZYFln9uzk6HIKKHWBFBcbPnU0KQpw222JbyAWI6MLC8dee3CQiWWS7P3T
# epnLxag+CmTIMpeZOxfYsQM4f36MdTSNFtnYyPe5ucADD7DkfIMpdRXIzh4bZWka3ZYkxZu3KNKH
# JNJ+TWMylaw0AwAdHcS6q1cnTLqG0+zZ9Hx1dQRIcV28U6eImlas4PucnKnndIo0hoVo8fmCIFBD
# E5TNMTjIOnOijL6nZ+zco7mZsScZRaPU5vLylAN+djaNqL8feHurB+e2vEqcrGlEjY88QlO6ySih
# QK4MHEH9pV3xXwQCrOqOzsY0LbE7CwbHrgJHo4wF5eVj7y4cZp1EktgXnTZtQjdnkSK4fS0w0P4X
# /PyFx3FetFCxLJaJtRYmmcaDCHECiQxG8Nq5X+C5Y0+hf8A38kunk0jL7x/5uaLQLY2OIV4v/XOi
# RrkkMfkby134/WyItLWRiROZgPD5gG3bgG3bEAuFcNk9gPa1y/DKUQENDam3baaGNHR5TyAUHkj4
# bVwMCUdCKMBKuNUWhBrrkb642vhSFNkZHB0PRDExXM3NTVzfOXuWcWO8WBAOc3JAT8aSke5Os7Ko
# CE4nsHAh5DQL/vnvHsN3AfgGBOzbR8C3YsV1NJJYjGWjri50Oa144cL3kNvwGDYvvzvu0Di1s9sc
# uHvh1/CP6x+H62IrY8BwkmVq4PASeiTCsvpw1xSJUMtH33VLC4OzOUEtR1UZcD0eMnbmzNRyAI8H
# +MMfaFGDg+yh1tZ+itokSYIoSXA6RWzcSH3avp1yu2bSNKj6feumFwwS6u/bx/9VlTjc4cDZrnYE
# fGY0tZxFLEEbQh7jGtDSHUDxbYmD++HDDIhut8HIS5eAefOM4y5c4AjJypXxAl2zJnHmdvQotXxo
# +GFcGhigcGfNMmJMcXHS3EGWidDPnKH8qqvZEZgwqSogAL3hZhzetw1L+xcAVhsTyliMCud2868o
# EuoBWBYsxRMdNdiwQYCYwA2PvXsNgGuI4YEA0Y2urW437V4XSKJaVnf3yNxDrw0NldNHUCRiFCht
# tuQJYlcX8MorXGvWLFpCshxmFJWVjYTGCxeOE6Y0jTyQZTL4+HF6hLlV2H1hO1688Etsrv4DyhYM
# LWKzjVlukmUZJpM8ZiUh4aDcwQOAM4M8BsBd5+WRYQBdUzQ6/lRbMGhoB8AbEARg8eKRN9rQwArv
# mjVjc0RP5BoaqIFmM9efoBDG2ub+D6h/SxeH4HDIkKNR4uX0dLrcd98F2tuZA5WVcb8AYk4Hfrtt
# L9r7L+PLn6tFcUFx0utFIsBbb3EAIhH7ElrIQKgVod4gKjAkgMpKupOSEmqJLFPjw2EyR1W54cJC
# MjUU4jE6gwMB+tDbbht5Ib+fE2VjqWcsxs89Hqbec+YYkHXCxarElKaoWFfVjWN7fHjip9vw9xsq
# UNsRIOfuvJOgZOVK3qfOQZcLAANw9ZyN0GJAccHV72F8gWjAjrbnEOi8iNr5/w3BbqNt19SMdCVt
# bdSUFSu4+SNHaEWKwgSsqurTjcNiYZDVA7zPRyFmZCTue6gq3UJ9PQuWWVlM5K5laFYnn4+DFpEI
# p9paWyHu2IGMaAB1A79Cyxu1cN3/DCoW2Y19jdNynvLye7/Pi/YOP7K6BuHfugX2u+4BnEOm6/XS
# EioqCGnPnCHz9J66KNIawmEWG1WVTC0tNbTr8mUmi8uX80aHC8Pvp0DDYZZKhh9ztcLo6KCrc7lo
# 6WfPciqkspLcnD4d+KdH4fT14pcX5gMRKxpaLPAEBVRXX//8MUEM0bCvToUzU8C8zHbAYjVyicFB
# 4sUFCwhNfD42bgTBcC+qSpdlsxHednQAd9xhML6jg8zVrQdgPNq1i8y6997Ualsjtqxx/WiUzG5u
# JnyaNo3C7+tjM37aNOPYcSgSYXu4r4+OIX2c7uyxY1xyCEQlpauIIQKimheBYBioGipV9PURxlZV
# cYd6mcRu5/+KwuiYlkam2IYe2snMZNwJhWgpFRUGMovF6PYcDh6fm8tq63g9E535qmrkQ3v3cn+b
# NpFzfj/hr77OqlWjbi95XmMy8bSGBuCdd+iVJ1i1uWpKCGtOXfgfHNn9NGJ6zcpu580fOkQX4nIx
# DwgGicD6+xk3enr4Nxym6yosZDDUi3q6SkSjwNatwJtvUlgmEwN7ImEMDhrt49ZW4IUXCHnDYa6Z
# n0+ElpHBdVavBpYs4Z6vgQSB+lNTw8LwsWOpj5NdC8VZiLffi7pLpxANerC5qwOFkKl1y5eTObqG
# NjbyryQxL9A0xherlfaen0/rEEWqmCBQoG43M+mVK+kKhztpVaVwZZmWc+gQcPAgk9D168nk1aup
# EIpCYS9ZMqUMyssjrti3j151qp9hiROIMz0dDy38PiRTAAV5BUCfFzhxghaycCEZ/9FHFEQgQDdm
# tZJJgkCGNjZSSIEAzzGbWeyLRhngBYF36vfTbeXk0N299RZd49q1XHf2bApVRzmZmcld2hSQ1Up9
# OHqU3cg1a6auhZIA9go46PkzOvrbsLH6p1C8/Wz063Hh3DlaSjjMwKmjKT1YOhy0ig8/pMWkpTGZ
# 2rDBQGlWK8959VX+3bCB2l9bOzQyPpRjpDLheJ3oej3DkhD2dnQEEIxJ6OrpRGFnD9B8jm5HksjU
# 7m72MTIziZpeeokWUVgIPPgg3ZWeXefnM6EbGGByl5dHK7HZgIceonvSA216asNmN5KKi6kne/cy
# 1xUlQBQ0TGwKfOzj4wSSnu7E/fMfBcQBFM4sBQqGBtv0jFySyDgdmr7yCmJPPQVhYACwWCCoKvCd
# 77DG5PUakNjlAu67j9ajxw1VNUosZjMxYSjEY6xWo4akaXwvSTw+Ehl5TjBIwVqtvJYOAqxWIzfS
# Sz2KQgvXwURaGvcRCHCvViv/BgJcS68MhMN8KQoyMizYdEcUH+0OYdf+S8goacS8qo0wxTSjsChJ
# vE40yvNNpqHrhNDaUQfvwDJYLPGtiTiUpUZVvH3pOTx/6mn4m5up1YcPc7FIhFXdS5f4PwB0d0Pz
# +YCBAWiBAGONLkCPh1YSDnNzu3YRIbUPPbv48cfAyy8zKwe47pYtwPvvG+hq+3bGn+5uCubAAa7R
# 0MBzmpv5fu9e7tHrBd54g6++Pn5WV8djmpt5TkMD3x84wDV7eniN7dsZ1yIR7mHLFiI7gHH05Zc/
# bTkrvZdxW9erMDV9Hz87+BhOn/6EbnrnTmMavL6euLmpie+vXEHnS7/H+x9+E+8cfyM1CwmE/BD7
# XchDGnxWM2xLljBQ69MjFgu1StfCtWuBjz5C+Px5mMrLgbvu4ufBIK3I7eY5oRCtJjPTSApXriR6
# 013WjBnAww/zvV6vuuceMs1k4uc1NcZeADpyvW8iSfQn997L7/Rz1q8feY7+8J8o8nt96kQQDBe6
# aROvq5fzFy9mQqzX3AoKEbv/Priy/NjcMwei1QzMXwLEVOM6VVW8ln6O2432pUugXtgMNSQgpsYg
# SiNtIk4gDns6ls6eD2+oG/lWJ3D4kIFsFIWQ1edjzCgqAmpqIM2YAampifC0sJAC9HoZJ2bONDbk
# 9bL+lZlJBjU08JiiIt6EKI4sGuqCGbHjUVtOdM7owuPocyRpZCkm0Tmjr5vgHNlmxaN3f2PUfuSR
# 54yihZUr8OjFFdiwjvEnqYX4/X68Wv9HdPo78WDt3chft45m29pKDZ82ja6gp4cuoKSEml1cTI3y
# +ThU19dHYeTm8vOWFr7PyzMmWBSFLi0zkww4eZLurbT0pkJYk0mCAEAYu2AQJxBFkbF52mMwKUE4
# HA4yvbGROA+guyoqIry9eJH+Njubn/f00Pc3Nxv5iZ5FWSyMGYsXGzPAZWUjB7Dz8iigYJACaWri
# NUpLKXA9Vf7s/eRDyhR3ZyaTGYp4FmLLPtjMVjJC96dHj1K0RUUUwNKlZJgsM6OWZQZsvYnkdhNl
# HDpEZPb5z5PpqsrjT540wAHA2LJokVHvKiw0WrQAeydvvcVSv6pSQHr14K+E4gTS7+vH1qa38cKV
# vWjrbDdyj48/JjP1GaySErqahQupzVYrGVlezuOKiuh+JIn9jIMHDUgrScxN+vv5AhLPdVmtdHN6
# Zc/lYpPL7aZi+P1ENTt3GvDY5xt75PUzQHHldzUWwevbO2BPB2oWZ0IxWQyfbzazbJKePnLATRfS
# 6EmSw4fJ1LlzKQxFMfrnwwNeJELYqiisCqRaLNKv6/cbSeWBA4SdK1ZQMXp7jQrCZDS4rpGSld/j
# f8lBNCHHmQcXFCh1dURFenO/t5evmTNHjv4Iw6JUIGA8uTtnDoN5KMSriyJd3I4dIx8A0uvd+flc
# T1UZj5I9ryYI3FdWltFaXr2apRh9Tqy9Hdi9m70WgPtvbR3/AaQbSAknF3ee+BV+/Ztvo9VUgGhe
# ITRNgz8QgOZwMO8wm9n504UVDrMRFIlQy3WUlZ7O44dDytJSxoahQYFPyWJhTmG3Gy3c996bOOME
# gfFNh62VlcDmzcYDQ3pv5vRpvu/v5yzYlSs3RSyKh72BAOo638AZ8xXMO5+FggEgHLuM800/x71f
# /Fe4C7JhUYCwBlgWLWJFRtOM8VJZJpLSkZA+IdLaSoaLIhGYzhy9BjYcOSkKn1fr7SVjQyFaWmGh
# UeScCIniiOQMbrfBfEni3r1exkJNI9iw2+kJJmmY4qoFYkkz4+mHn4Yai6J8WiYUCfjFlnfxk8bn
# 0bNlGVaVfxGD6gD2tbyAB2u+jDIzYLVI6CuegVxRpMmNfrBTUYzygT5KpDPq9GlC3eEZu/7d8DHU
# 3l7C6dralCfgxyX9WjYbq9Y6RaMcL+rpoeXLMl3w4KBRUE2hDXy1JD355JNPjpCQLMOd40ZhbiHM
# ihmyCchxpuHOeZuwfvkcLF+ShdNte/Gf+5/AYIcb9ugy7D18Ac8c/DHy5GookhOyCYjVn0QwOghz
# ejqZq8Pd4bNUkkThybLR4Ut0o5JE1DZ9Oi3O5yNgUBQydDKZo88pFxUZIEUvYlqtfJ0+Tegty7Sq
# WMyYKUhCsRh1s7Q08ZBlSg/szJlRhjkzjARucUUJXsz4PQozCzBvFvDc1r040rcfu4/uRyz4EPxB
# oO1gHQL2Ftx9/4+RmyMgPd0J2ekEwiFokgxB342iGBOOx45RYPqzfaNJdx82GxsTTU1Glq9pU4Oi
# BIGWOtxa9WlJPU61tVFARUXMo4ajzgkmscJk/LJ1l6cLvqAPGbZ0ZGXkwOsN4uu//jpOtp/BEyte
# RKZ9JiIRwOYAXF2n4e+rQ/nD/4DMdNtI5e7uZsV0+fLUWnK66+jp4XmlpYxT1/EhTQBU+4EBCiEn
# h/Fo3z4KZNUq/vV6gbQ0REQzXtvqwxe+YIPVGq9AkyKQ0RSNRtDa2YpoLIrCnEKkWWwIBAi89uw/
# gqdefxCb5j+D2+feBWcG872cHMCRDsiIABAANUaGJ5qSTySYri6+ysuNUderAQCTRXpvR+/RHDgA
# eL0YmD8f33v5WXz7ni9hYemCuNOm5DFTWTZhZmHJiM9sNr4KS71YWbse84v8qF5Ko9Bn2VQVsNtN
# yMkFXLFOZDV+CN+C2ZDdbmQ6M8a+oCBQqnpZv7eXGjp9Ol3I9bYYwGhKAXSlNTVAVMXR43V489L/
# YfrhdCyctSCucTglFjIeaZoGAQKAkUhFb/R5PEwJejxAqKEF2479APmrl+PRmn9BVjYT7pSeVg4G
# 6Sby8miagcD4P2xwnai98wpefK0VG9c5Mbe0BIKQpB8y1WT8aNdI1RBFAi273UDNFysVPOvz4eL5
# g1ie0wtRzISqGjHd5WJMt1gSGEFamgGPNY2A4dKl6/qrDIkoN8uF0nwXZk1LvI3rbiETocHIIPr6
# +yAIQKYzC6Igf2pFnZ2M5XprXG9E5uRQqHFWpE/rW60UjMdDADAZOc0E6KoeR7hZSDEpcGW7Rnw2
# 2ooGB41fnW1rY4qgaTxGt6KMDMBikSDoPwuS4eT8V0MDY0wsNrIedwPpphZIKqQobErm5vJ9LMZK
# iB6Ljh83Cs2ZmYArF8jOdcBx22pIwlDD69xZoPUSWwmp/tbKFNFnXiCjSRQZ+B0O49nB4VbUegk4
# 9akViRSmsxiZmSrM3T0QsrKA8NADR9L1Z89fnUAS0XArmjvXsKKeniEralcQGqyAYgIyPYCrqxk5
# nibY1y6FNL0QsVgMgiAk/BXRyaa/CYGMpuFWpD8GHw4Ps6JgBU515kB7R0N6KdDa+SoWLFiAipJS
# mJSpDTV/kwJJRGbzsNyyUkDsdhcCAeDIiYv4r71PourEfXhk6ZMwWxhmXC6Wt+z2yS2h3RLIGCQK
# gN0GFBVF8Y2NX0GBoxB3VkcQCJhw5Qp7cCdPMhY5HHSHOqJTrsGKbuo85GYnVR0Zizwe48Hk4VY0
# /NH7SISPNGzY8BnMQ2520ufO09PZMdCr7n19jEUXLnAkWJ+xyM0FMjI09PVdRiSSlfCnYm8JZBJJ
# n7nIyzMeDtCtqLubQjp6tBXPPvsB0tKK8cADK+LWuCWQKabhVlRSApSXZyEQKEF5eeJfGrgVQ24y
# +usdkv2M0i2B3GT0/6olFPglNIFBAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDE2LTAzLTA4VDA5OjU3
# OjEzKzExOjAwtE31rAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAxNi0wMy0wOFQwOTo1NzoxMysxMTow
# MMUQTRAAAAAASUVORK5CYII='''
# 	whale = tk.PhotoImage(data = photo)
# 	image = tk.Label(aboutwin, image = whale)
# #	As per http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
# 	image.image = whale
# 	image.pack(anchor = 'nw')

	msg =\
'''PolyDist is a Python 3
geometry program
designed to make 2D
calculations easier.'''

	tk.Message(aboutwin, text = msg, width = 150).pack(expand = True, anchor = 'ne')

#	Button frame
	frame = tk.Frame(aboutwin, width = 400)

	Credits = tk.Button(frame, text = 'Credits', command = polycredits).grid(row = 0, column = 0)

	License = tk.Button(frame, text = 'License', command = polylicense).grid(row = 0, column = 1)

	Close = tk.Button(frame, text = 'Close', command = aboutwin.destroy,\
		).grid(row = 0, column = 2)

	frame.pack(anchor = 's')


################################################################################
# Credits window.
def polycredits():
	pcwin = tk.Toplevel()
	pcwin.geometry('300x150')
	msg =\
'''Written and maintained by
Fred Barclay (Fred-Barclay).

Linux tester: Fred Barclay.

Windows (R) tester: Scott Ingram.'''

	tk.Message(pcwin, text = msg).pack(anchor = 'center', expand = True)

	tk.Button(pcwin, text = 'Close', command = pcwin.destroy).pack()

################################################################################
# Licensing window
def polylicense():
	plwin = tk.Toplevel()
	plwin.geometry('425x300')
	msg = '''
FILL ME IN!!!!!
'''
	tk.Message(plwin, text = msg).pack()

	tk.Button(plwin, text = 'Close', command = plwin.destroy).pack()

################################################################################
# Documentation links window
def docs():
	docswin = tk.Toplevel()
	docswin.title('Documentation')

	docswin.geometry('300x300')

################################################################################

if __name__ == "__main__":
	main()
