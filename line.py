from object import Object
from PySide6.QtGui import QColor, QPen
from type import Type

class Line(Object):
    def __init__(self, name, coord):
        super().__init__(name, Type.LINE, coord)
    
    def draw(self, coord_viewport, painter):
        pen = QPen(QColor('black'), 3)
        painter.setPen(pen)
        painter.drawLine(
            coord_viewport[0][0],
            coord_viewport[0][1],
            coord_viewport[1][0],
            coord_viewport[1][1]
        )