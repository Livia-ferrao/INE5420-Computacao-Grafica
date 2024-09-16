from enum import Enum

class Type(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3
    
class RotationType(Enum):
    OBJECT_CENTER = "Centro do objeto"
    WORLD_CENTER = "Centro do mundo"
    ARBITRARY_POINT = "Ponto Arbitrário"
