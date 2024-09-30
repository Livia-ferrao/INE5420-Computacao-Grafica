from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type

class Line(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.LINE, coord, color)
    
    def draw(self, coord_viewport, painter):
        pen = QPen(self.color, 2)
        painter.setPen(pen)
        painter.drawLine(
            coord_viewport[0][0],
            coord_viewport[0][1],
            coord_viewport[1][0],
            coord_viewport[1][1]
        )