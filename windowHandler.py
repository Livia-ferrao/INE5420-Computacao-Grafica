
from math import cos, sin
import numpy as np
from math import radians


class WindowHandler:    
    @staticmethod
    def create_translating_matrix(desvio_x, desvio_y):
        return np.array(
            [[1, 0, 0], 
             [0, 1, 0], 
             [desvio_x, desvio_y, 1]])

    @staticmethod
    def create_rotating_matrix(angulo):
        angulo = radians(-angulo)

        return np.array([[cos(angulo), -sin(angulo), 0],
                         [sin(angulo), cos(angulo), 0],
                         [0, 0, 1]])

    @staticmethod
    def create_scaling_matrix(Sx, Sy):
        return np.array([[Sx, 0, 0], 
                         [0, Sy, 0], 
                         [0, 0, 1]])