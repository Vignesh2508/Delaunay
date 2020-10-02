# Simple delaunay triangle generator
# Implementation of incremental Bowyer-Watson Algorithm
# This has a time complexity of O(n^2)
# Refer to the Wikipedia page of Bowyer watson algorithm as I have implemented directly from the Pseudo-code

# Author: Vignesh Rajendiran

# This is written with ease of understanding in mind. If you want elaborate code. Then visit https://github.com/ayron
# I referred to Ayrons code for inspiration. I am planning to rewrite this code as my own in the future.

# sometimes there will be a cross division error if the n>100 because of random points used and WIDTH, HEIGHT values

import math
import random
import simple_delaunay as d

import matplotlib.pyplot as plt
import matplotlib.tri as tri

WIDTH = int(100)
HEIGHT = int(100)
n = 21  # n should be greater than 2

xs = [random.randint(1, WIDTH - 1) for x in range(n)]
ys = [random.randint(1, HEIGHT - 1) for y in range(n)]
zs = [0 for z in range(n)]

DT = d.Delaunay_Triangulation(WIDTH, HEIGHT)
for x, y in zip(xs, ys):
    DT.AddPoint(d.Point(x, y))

# Remove the super triangle on the outside
DT.Remove_Super_Triangles()

# Helps in determining the neighbours of triangles. I felt it might help in the future
# Remove this to speed up triangle generation
# DT.Find_Neighbours()

XS, YS, TS = DT.export()

# Creating a Triangulation without specifying the triangles results in the
# Delaunay triangulation of the points.

# Create the Triangulation; no triangles so Delaunay triangulation created.
triang = tri.Triangulation(xs, ys)

# Plot the triangulation.
fig, ax = plt.subplots()
ax.margins(0.1)
ax.set_aspect('equal')
ax.triplot(triang, 'bo-')

# print(XS)
# print(YS)
# print(TS)

ax.triplot(tri.Triangulation(XS, YS, TS), 'bo--')
ax.set_title('Plot of Delaunay triangulation')

plt.show()
