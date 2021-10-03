import numpy as np
import point
import triangle
import csv


'''
A class to build the mesh
'''
class PolygonBuilder:
    x_max = 0
    y_max = 0
    z_max = 0
    points = [[], [], [], []]
    colours = [[], [], [], []]
    colour_weights = []
    shape_weights = []
    triangles = []

    def check_max(self, p: point.Point):
        '''
        Check if the ma values have been exceeded and if they have chnage them
        :param p: a new point
        '''
        if abs(float(p.get_x())) > self.x_max:
            self.x_max = abs(float(p.get_x()))
        if abs(float(p.get_y())) > self.y_max:
            self.y_max = abs(float(p.get_y()))
        if abs(float(p.get_z())) > self.z_max:
            self.z_max = abs(float(p.get_z()))

    def find_max(self):
        '''
        A method to find the max x, y and z values
        '''
        for each in self.triangles:
            self.check_max(each.get_point1())
            self.check_max(each.get_point2())
            self.check_max(each.get_point3())

    def get_shapes(self):
        '''
        Read in shape file and offsets
        '''
        files = ['sh_000.csv', 'sh_001.csv', 'sh_002.csv', 'sh_003.csv']
        for i in range(0, len(files)):
            with open(files[i], newline='') as csv_file:
                shape_reader = csv.reader(csv_file)
                for row in shape_reader:
                    p = point.Point(row[0], row[1], row[2])
                    self.points[i].append(p)

    def get_colours(self):
        '''
        Read in colour file and offsets
        '''
        files = ['tx_000.csv', 'tx_001.csv', 'tx_002.csv', 'tx_003.csv']
        for i in range(0, len(files)):
            with open(files[i], newline='') as csv_file:
                col_reader = csv.reader(csv_file)
                for row in col_reader:
                    self.colours[i].append([float(row[0]), float(row[1]), float(row[2])])

    def get_shape_weights(self):
        '''
        Read in shape weights
        '''
        with open("sh_ev.csv", newline='') as csv_file:
            sh_reader = csv.reader(csv_file)
            for row in sh_reader:
                self.shape_weights.append(float(row[0]))

    def get_colour_weights(self):
        '''
        Read in colour weights
        '''
        with open("tx_ev.csv", newline='') as csv_file:
            tx_reader = csv.reader(csv_file)
            for row in tx_reader:
                self.colour_weights.append(float(row[0]))

    def __init__(self):
        self.get_shapes()
        self.get_colours()
        self.get_shape_weights()
        self.get_colour_weights()

    def build_face(self, weight1, weight2, weight3):
        '''
        Read in mesh file and iteratively build triangles according to mesh
        :param weight1: weight of face 001
        :param weight2: weight of face 002
        :param weight3: weight of face 003
        '''
        with open('mesh.csv', newline='') as csv_file:
            mesh_reader = csv.reader(csv_file)
            for row in mesh_reader:
                t = self.create_triangle(row, weight1, weight2, weight3)
                self.triangles.append(t)
        self.find_max()

    def create_triangle(self, row, weight1, weight2, weight3):
        '''
        A method that takes the indices of three points and creates a triangle that
        averages the points across the three faces using the weights
        :param row: row from mesh
        :param weight1: weight of face 001
        :param weight2: weight of face 002
        :param weight3: weight of face 003
        :return:the resultant triangle
        '''
        p1 = self.create_point(int(row[0]) - 1, weight1, weight2, weight3)
        p2 = self.create_point(int(row[1]) - 1, weight1, weight2, weight3)
        p3 = self.create_point(int(row[2]) - 1, weight1, weight2, weight3)
        c1 = self.create_colour(int(row[0]) - 1, weight1, weight2, weight3)
        c2 = self.create_colour(int(row[1]) - 1, weight1, weight2, weight3)
        c3 = self.create_colour(int(row[2]) - 1, weight1, weight2, weight3)
        t = triangle.Triangle(p1, p2, p3)
        t.set_colors(c1, c2, c3)
        return t

    def create_point(self, index, w1, w2, w3):
        '''
        Create a single point that is the average of the three faces and the average face
        :param index: index of point
        :param w1: weight of face 001
        :param w2: weight of face 002
        :param w3: weight of face 003
        :return: averaged point
        '''
        x = self.points[0][index].get_x() + (self.points[1][index].get_x() * w1 * self.shape_weights[0]) + \
            (self.points[2][index].get_x() * w2 * self.shape_weights[1]) + \
            (self.points[3][index].get_x() * w3 * self.shape_weights[2])
        y = self.points[0][index].get_y() + (self.points[1][index].get_y() * w1 * self.shape_weights[0]) + \
            (self.points[2][index].get_y() * w2 * self.shape_weights[1]) + \
            (self.points[3][index].get_y() * w3 * self.shape_weights[2])
        z = self.points[0][index].get_z() + (self.points[1][index].get_z() * w1 * self.shape_weights[0]) + \
            (self.points[2][index].get_z() * w2 * self.shape_weights[1]) + \
            (self.points[3][index].get_z() * w3 * self.shape_weights[2])
        return point.Point(x, y, z)

    def create_colour(self, index, w1, w2, w3):
        '''
        Create a colour for each point that is the average colour for that point
        across the three faces and the average fae
        :param index: index of point
        :param w1: weight of face 001
        :param w2: weight of face 002
        :param w3: weigh of face 003
        :return: list of rgb values
        '''
        r = self.colours[0][index][0] + self.colours[1][index][0] * w1 * self.colour_weights[0] + \
            self.colours[2][index][0] * w2 * self.colour_weights[1] + \
            self.colours[3][index][0] * w3 * self.colour_weights[2]
        g = self.colours[0][index][1] + self.colours[1][index][1] * w1 * self.colour_weights[0] + \
            self.colours[2][index][1] * w2 * self.colour_weights[1] + \
            self.colours[3][index][1] * w3 * self.colour_weights[2]
        b = self.colours[0][index][2] + self.colours[1][index][2] * w1 * self.colour_weights[0] \
            + self.colours[2][index][2] * w2 * self.colour_weights[1] + \
            self.colours[3][index][2] * w3 * self.colour_weights[2]
        return [r, g, b]
