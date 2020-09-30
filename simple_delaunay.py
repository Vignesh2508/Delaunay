import numpy as np


def SharedEdge(line1, line2):
    if (line1[0] == line2[0] and line1[1] == line2[1]) or (line1[0] == line2[1] and line1[1] == line2[0]):
        return True
    return False


class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(s):
        return "( " + str(s.x) + ", " + str(s.y) + " )"

    def __add__(self, b):
        return Point(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        return Point(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        return Point(b * self.x, b * self.y)

    __rmul__ = __mul__

    def IsInCircumcircleOf(self, T):

        a_x = T.v[0].x
        a_y = T.v[0].y

        b_x = T.v[1].x
        b_y = T.v[1].y

        c_x = T.v[2].x
        c_y = T.v[2].y

        # The point coordinates

        d_x = self.x
        d_y = self.y

        # If the following determinant is greater than zero then point lies inside circumcircle
        incircle = np.array([[a_x - d_x, a_y - d_y, (a_x - d_x) ** 2 + (a_y - d_y) ** 2],
                             [b_x - d_x, b_y - d_y, (b_x - d_x) ** 2 + (b_y - d_y) ** 2],
                             [c_x - d_x, c_y - d_y, (c_x - d_x) ** 2 + (c_y - d_y) ** 2]])

        if np.linalg.det(incircle) > 0:
            return True
        else:
            return False


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.v = [None] * 3
        self.v[0] = a
        self.v[1] = b
        self.v[2] = c

        self.edges = [[self.a, self.b],
                      [self.b, self.c],
                      [self.c, self.a]]

    def HasVertex(self, point):
        if (self.a == point) or (self.b == point) or (self.c == point):
            return True
        return False

    def __repr__(s):
        '''
        return '<%s, [%s, %s, %s]>' % (
                hex(id(s)),
                hex(id(s.neighbour[0])),
                hex(id(s.neighbour[1])),
                hex(id(s.neighbour[2])))
        '''
        return '< ' + str(s.v) + ' >'


class Delaunay_Triangulation:
    def __init__(self, WIDTH, HEIGHT):
        self.triangulation = []

        # Declaring the super triangle coordinate information
        self.SuperPointA = Point(-100, -100)
        self.SuperPointB = Point(2 * WIDTH + 100, -100)
        self.SuperPointC = Point(-100, 2 * HEIGHT + 100)

        superTriangle = Triangle(self.SuperPointA, self.SuperPointB, self.SuperPointC)

        self.triangulation.append(superTriangle)

    def AddPoint(self, p):

        bad_triangles = []

        for triangle in self.triangulation:
            # Check if the given point is inside the circumcircle of triangle
            if p.IsInCircumcircleOf(triangle):
                # If it is then add the triangle to bad triangles
                bad_triangles.append(triangle)

        polygon = []

        # Routine is to find the convex hull of bad triangles
        # This involves a naive search method, which increases the time complexity
        for current_triangle in bad_triangles:
            for this_edge in current_triangle.edges:
                isNeighbour = False
                for other_triangle in bad_triangles:
                    if current_triangle == other_triangle:
                        continue
                    for that_edge in other_triangle.edges:
                        if SharedEdge(this_edge, that_edge):
                            # Check if the Edge is shared between two triangles
                            # If the edge is shared it won't be included into the convex hull
                            isNeighbour = True
                if not isNeighbour:
                    polygon.append(this_edge)

        # Delete the bad triangles
        for each_triangle in bad_triangles:
            self.triangulation.remove(each_triangle)

        # Re-triangle the convex hull using the given point
        for each_edge in polygon:
            newTriangle = Triangle(each_edge[0], each_edge[1], p)
            self.triangulation.append(newTriangle)

    def export(self):

        # Removing the super triangle using Lamba function
        onSuper = lambda triangle: triangle.HasVertex(self.SuperPointA) or triangle.HasVertex(
            self.SuperPointB) or triangle.HasVertex(self.SuperPointC)

        for triangle_new in self.triangulation[:]:
            if onSuper(triangle_new):
                self.triangulation.remove(triangle_new)

        ps = [p for t in self.triangulation for p in t.v]

        x_s = [p.x for p in ps]
        y_s = [p.y for p in ps]

        # xs = list(set(xs))
        # ys = list(set(ys))

        ts = [(ps.index(t.v[0]), ps.index(t.v[1]), ps.index(t.v[2])) for t in self.triangulation]

        return x_s, y_s, ts
