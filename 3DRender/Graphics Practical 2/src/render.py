import point
import triangle
import mpl_toolkits.mplot3d as a3
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pylab as pl
import numpy as np
import polygon_builder


def median_pivot(triangles: list, low, high):
    '''
    Find the median pivot using median of three
    :param triangles: List of triangles from mehs
    :param low: start of current partition
    :param high: end of current partition
    :return pivot index
    '''
    val1 = triangles[low]
    val2 = triangles[int((low + high) / 2)]
    val3 = triangles[high]
    med = np.median([val1.get_depth(), val2.get_depth(), val3.get_depth()])
    if med == val1.get_depth():
        return low
    if med == val2.get_depth():
        return int((low + high) / 2)
    if med == val3.get_depth():
        return high


def partition(triangles: list, low, high):
    '''
    Using a pivot value, sort values either side

    :param triangles: list of triangles from mesh
    :param low: Start of current partition
    :param high: End of current partition
    :return partition value
    '''
    i = (low - 1)
    p_val = median_pivot(triangles, low, high)
    pivot = triangles[p_val]

    for j in range(low, high):
        if triangles[j].get_depth() >= pivot.get_depth():
            i += 1
            triangles[i], triangles[j] = triangles[j], triangles[i]
    triangles[i + 1], triangles[p_val] = triangles[p_val], triangles[i + 1]
    return i + 1


def quick_sort(triangles: list, low, high):
    '''
    Recursive quicksort function
    :param triangles: list of triangles from a mesh
    :param low: the start of current partition
    :param high: the end of current partition
    :return: sorted partition
    '''
    if len(triangles) == 1:
        return triangles
    if low < high:
        part = partition(triangles, low, high)
        quick_sort(triangles, part + 1, high)
        quick_sort(triangles, low, part - 1)


def create_vertex(triangle: triangle.Triangle, x, y, z):
    '''
    Create a vertex list (np array) for matplotlib
    :param triangle: a triangle from mesh
    :param x: normalisation value for x
    :param y: normalisation value for y
    :param z: normalisation value for z
    :return: the vertex
    '''
    vtx = np.array(
        [[triangle.get_point1().get_x() / x, triangle.get_point1().get_y() / y, triangle.get_point1().get_z() / z],
         [triangle.get_point2().get_x() / x, triangle.get_point2().get_y() / y, triangle.get_point2().get_z() / z],
         [triangle.get_point3().get_x() / x, triangle.get_point3().get_y() / y, triangle.get_point3().get_z() / z]])
    return vtx


def render_face(w1, w2, w3):
    '''
    This method orchestrates the necessary functions
    for rendering of a face using the other scripts
    :param w1: weight of face 1
    :param w2: weight of face 2
    :param w3: weight of face 3
    :return:
    '''
    print('Reading in data')
    pol = polygon_builder.PolygonBuilder()
    print('Building triangle mesh')
    pol.build_face(w1, w2, w3)
    triangles = pol.triangles
    print('Sorting for painters algorithm')
    quick_sort(triangles, 0, len(triangles) - 1)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_ylim(-1, 1)
    ax.set_xlim(-1, 1)
    ax.set_zlim(-1, 1)
    print('Adding triangle mesh to a figure')
    for each in triangles:
        vtx = create_vertex(each, pol.x_max, pol.y_max, pol.z_max)
        tri = a3.art3d.Poly3DCollection([vtx])
        rgb = each.get_aggregate_colour()
        tri.set_color(colors.rgb2hex(rgb))
        tri.set_edgecolor(colors.rgb2hex(rgb))
        ax.add_collection3d(tri)
    print('Rendering figure')
    ax.set_xlabel('$X$')
    ax.set_ylabel('$Y$')
    ax.set_xlabel('$Z$')
    ax.view_init(elev=90., azim=-90)
    pl.savefig('face.png')
