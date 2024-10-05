from enum import Enum

class Type(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3
    BERZIER_CURVE = 4
    
class RotationType(Enum):
    OBJECT_CENTER = "Centro do objeto"
    WORLD_CENTER = "Centro do mundo"
    ARBITRARY_POINT = "Ponto Arbitrário"

class ClippingAlgorithm(Enum):
    COHEN = "Método de Cohen Sutherland"
    LIANG = "Método de Liang-Barsky"