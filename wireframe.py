from object import Object
from PySide6.QtGui import QColor, QPen, QPolygonF, QBrush
from PySide6.QtCore import QPointF

class Wireframe(Object):
    def __init__(self, name, coord, fill):
        super().__init__(name, "wireframe", coord)
        self.fill = fill

    def draw(self, coord_viewport, painter):
        pen = QPen(QColor('black'), 3)
        painter.setPen(pen)

        polygon = QPolygonF([QPointF(x, y) for x, y in coord_viewport])
        if self.fill:
            brush = QBrush(QColor('black'))
            painter.setBrush(brush)
        painter.drawPolygon(polygon)
