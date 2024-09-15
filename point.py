from object import Object
from PySide6.QtGui import QColor, QPen
from type import Type

class Point(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.POINT, coord, color)
    
    def draw(self, coord_viewport, painter):
        pen = QPen(self.color, 3)
        painter.setPen(pen)
        painter.drawPoint(coord_viewport[0][0], coord_viewport[0][1])
