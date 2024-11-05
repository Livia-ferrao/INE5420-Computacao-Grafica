from enum import Enum

class Type(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3
    BERZIER_CURVE = 4
    B_SPLINE = 5
    OBJECT_3D = 6
    BERZIER_SURFACE = 7

class ClippingAlgorithm(Enum):
    COHEN = "Método de Cohen Sutherland"
    LIANG = "Método de Liang-Barsky"

class RotationAxis(Enum):
    X = "X"
    Y = "Y"
    Z = "Z"
    ARBRITRARY = "Arbitrário"

class Projection(Enum):
    PARALLEL = "Projeção Paralela"
    PERSPECTIVE = "Projeção em Perspectiva"