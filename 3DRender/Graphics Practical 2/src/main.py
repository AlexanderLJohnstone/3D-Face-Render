from math import sqrt
from tkinter import *

from PIL import ImageTk, Image

import render

# Positions for triangle vertices
vertex_1 = [200, 100]
vertex_2 = [100, 273.2]
vertex_3 = [300, 273.2]


def distance(x, y, x2, y2):
    '''
    Find the distance between two points
    :param x: input x
    :param y: input y
    :param x2: vertex x
    :param y2: vertex y
    :return:
    '''
    return sqrt((x2 - x) ** 2 + (y2 - y) ** 2)


def calculate_weights(x, y, ver_1, ver_2, ver_3):
    '''
    Calculate the weights of each face for interpolation using distance from each vertex.
    The weights are standardised so that they sum to 1.
    :param x: input x
    :param y: input y
    :param ver_1: vertex 1
    :param ver_2: vertex 2
    :param ver_3: vertex 3
    :return: a weight for each vertex
    '''
    w1 = 1 - (distance(x, y, ver_1[0], ver_1[1]) / 200)
    w2 = 1 - (distance(x, y, ver_2[0], ver_2[1]) / 200)
    w3 = 1 - (distance(x, y, ver_3[0], ver_3[1]) / 200)
    total = w1 + w2 + w3
    w1, w2, w3 = w1 / total, w2 / total, w3 / total
    return w1, w2, w3


def callback(event):
    '''
    This method determines if a click is within a triangle and if it is initiates rendering using weights
    :param event: Input from user
    :return: None
    '''
    if inside_triangle(event.x, event.y, vertex_1, vertex_2, vertex_3):
        print("Input Received!")
        w1, w2, w3 = calculate_weights(event.x, event.y, vertex_1, vertex_2, vertex_3)
        print("Weights: ", w1, w2, w3)
        render.render_face(w1, w2, w3)
        # Output face in a new window
        root = Tk()
        canvas = Canvas(root, width=1200, height=1200)
        canvas.pack()
        img = ImageTk.PhotoImage(image=Image.open("face.png"), master=canvas)
        canvas.create_image(640, 480, image=img)
        root.mainloop()
    else:
        print('Click outside of triangle')


def compute_z(x1, y1, x2, y2):
    '''
    Compute the Z value of a cross product
    :param x1: vector 1 x
    :param y1: vector 1 y
    :param x2: vector 2 x
    :param y2: vector 2 y
    :return:
    '''
    z_comp = determinant(x1, y1, x2, y2)
    if z_comp < 0:
        return True
    return False


def determinant(a, b, c, d):
    '''
    Find the determinant of a 2X2 matrix
    :return: determinant
    '''
    return a * d - b * c


def inside_triangle(x: int, y: int, ver_1: list, ver_2: list, ver_3: list):
    '''
    Determine if a user click was within the triangle on the canvas
    :param x: Input x
    :param y: Input y
    :param ver_1: Vertex 1 in triangle
    :param ver_2: Vertex 2 in triangle
    :param ver_3: Vertex 3 in triangle
    :return:
    '''
    bool_1 = further_left(ver_2[0], ver_2[1], x, y, ver_1[0], ver_1[1])
    bool_2 = further_left(ver_1[0], ver_1[1], x, y, ver_3[0], ver_3[1])
    bool_3 = further_left(ver_3[0], ver_3[1], x, y, ver_2[0], ver_2[1])
    if not (bool_1 or bool_2 or bool_3):
        return True
    else:
        return False


def further_left(ref_x, ref_y, inp_x, inp_y, vert_x, vert_y):
    '''
    A method to determine which of two vectors are further left
    :param ref_x: Reference x value
    :param ref_y: Reference y value
    :param inp_x: Input x
    :param inp_y: Input y
    :param vert_x: Next vertex x
    :param vert_y: Next vertex y
    :return:
    '''
    tri_x = ref_x - vert_x
    tri_y = ref_y - vert_y
    inp_x = ref_x - inp_x
    inp_y = ref_y - inp_y
    return compute_z(tri_x, tri_y, inp_x, inp_y)


# Open a TKinter menu with text and interactive triangle
window = Tk()
window.title("Face Rendering")
w = Label(window, text="3D Face Render!", font=('Courier', 36))
w.pack()
w = Label(window, text="Click on the triangle to render a face.", font=('Courier', 12))
w.pack()
can = Canvas(window, width=400, height=400)
can.bind("<Button-1>", callback)
can.pack()
points = [vertex_1[0], vertex_1[1], vertex_2[0], vertex_2[1], vertex_3[0], vertex_3[1]]
can.create_polygon(points, fill='black')
window.mainloop()
