'''
A class for storing a single point in three-dimensional space
'''
class Point:

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def __repr__(self):
        '''
        A function for printing this class (useful for development)
        :return: A string representing the contents of the class
        '''
        string = "{"
        string += str(self.x)
        string += ", "
        string += str(self.y)
        string += ", "
        string += str(self.z)
        string+= "}"
        return string
