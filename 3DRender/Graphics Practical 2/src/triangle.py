import math
from math import sqrt

import point


def determinant(a, b, c, d):
    '''
    :return The determinant of a 2X2 matrix
    '''
    return a * d - b * c

'''
A class for storing all relevant characteristics of each triangle from the mesh
'''
class Triangle:
    # The light source
    light_source = point.Point(10, 0.5, 0.5)
    # The vertices
    point1: point.Point
    point2: point.Point
    point3: point.Point
    # The colour of each vertex
    colour1: list
    colour2: list
    colour3: list
    # The centroid
    centroid: point.Point
    # The polygoon normal
    normal: point.Point
    # The vector of incidence
    w: point.Point
    # The depth of the polygon
    depth: float

    def __init__(self, point1, point2, point3):
        self.point1, self.point2, self.point3 = point1, point2, point3
        self.centroid()
        self.compute_normal()
        self.depth()

    def set_colors(self, colour1, colour2, colour3):
        self.colour1, self.colour2, self.colour3 = colour1, colour2, colour3

    def get_point1(self):
        return self.point1

    def get_point2(self):
        return self.point2

    def get_point3(self):
        return self.point3

    def get_colour1(self):
        return self.colour1

    def get_colour2(self):
        return self.colour2

    def get_colour3(self):
        return self.colour3

    def get_centroid(self):
        return self.centroid

    def get_depth(self):
        return self.depth

    def __repr__(self):
        '''
        A function for printing this class (useful for development)
        :return: A string representing the contents of the class
        '''
        string = "<"
        string += self.point1.__repr__()
        string += "; "
        string += self.point2.__repr__()
        string += "; "
        string += self.point3.__repr__()
        string += ">"
        return string

    def get_aggregate_colour(self):
        '''
        Get the aggregate colour of the three points by averaging the RGB values
        This value is then multiplied by the lambertian co-efficient for the polygon
        :return: An RGB list representing a flat shaded, lambertian lit polygon
        '''
        co = self.compute_lambertian()
        r = (((float(self.colour1[0]) + float(self.colour2[0]) + float(self.colour3[0])) / 3) / 255) * co
        g = (((float(self.colour1[1]) + float(self.colour2[1]) + float(self.colour3[1])) / 3) / 255) * co
        b = (((float(self.colour1[2]) + float(self.colour2[2]) + float(self.colour3[2])) / 3) / 255) * co
        if r > 1:
            r = 1
        if g > 1:
            g = 1
        if b > 1:
            b = 1
        return [r, g, b]

    def depth(self):
        z_dis = self.centroid.get_z() - self.light_source.get_z()
        self.depth = z_dis
        
    def centroid(self):
        '''
        Computer the centroid (exact middle point) of a triangule
        '''
        x = (self.point1.get_x() + self.point2.get_x() + self.point3.get_x()) / 3
        y = (self.point1.get_y() + self.point2.get_y() + self.point3.get_y()) / 3
        z = (self.point1.get_z() + self.point2.get_z() + self.point3.get_z()) / 3
        self.centroid = point.Point(x, y, z)

    def compute_normal(self):
        '''
        Compute the normal of a triangle
        '''
        v1 = point.Point(self.point2.get_x() - self.get_point1().get_x(),
                         self.point2.get_y() - self.get_point1().get_y(),
                         self.point2.get_z() - self.get_point1().get_z())
        v2 = point.Point(self.point3.get_x() - self.get_point1().get_x(),
                         self.point3.get_y() - self.get_point1().get_y(),
                         self.point3.get_z() - self.get_point1().get_z())
        i = determinant(v1.get_y(), v1.get_z(), v2.get_y(), v2.get_z())
        j = determinant(v1.get_x(), v1.get_z(), v2.get_x(), v2.get_z())
        k = determinant(v1.get_x(), v1.get_y(), v2.get_x(), v2.get_y())
        normalisation = sqrt((i ** 2) + (j ** 2) + (k ** 2))
        self.normal = point.Point(i / normalisation, j / normalisation, k / normalisation)

    def compute_direction(self):
        '''
        Compute the vector going from the centroid of the polygon
        to the light source.
        '''
        x = self.light_source.get_x() - self.centroid.get_x()
        y = self.light_source.get_y() - self.centroid.get_y()
        z = self.light_source.get_z() - self.centroid.get_z()
        normalisation = sqrt((x ** 2) + (y ** 2) + (z ** 2))
        self.w = point.Point(x / normalisation, y / normalisation, z / normalisation)

    def compute_lambertian(self):
        '''
        Compute the lambertian reflectance co-efficient for this triangle
        @:return the intensity
        '''
        self.compute_normal()
        self.compute_direction()
        dot_product = self.w.get_x() * self.normal.get_x() + \
                      self.w.get_y() * self.normal.get_y() + \
                      self.w.get_z() * self.normal.get_z()
        intensity = dot_product * 2 * 0.6
        if intensity < 0:
            intensity = 0
        return intensity
