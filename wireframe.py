from object import Object
from PySide6.QtGui import QColor, QPen, QPolygonF, QBrush
from PySide6.QtCore import QPointF, Qt
from type import Type

class Wireframe(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.WIREFRAME, coord, color)

    def draw(self, coord_viewport, painter):
        pen = QPen(self.color, 3)
        painter.setPen(pen)

        # Desenhando linhas do polígono
        for i, (x, y) in enumerate(coord_viewport):
            if i == len(coord_viewport)-1:
                painter.drawLine(x, y, coord_viewport[0][0], coord_viewport[0][1])
            else:
                painter.drawLine(x, y, coord_viewport[i+1][0], coord_viewport[i+1][1])
        polygon = QPolygonF([QPointF(x, y) for x, y in coord_viewport])
