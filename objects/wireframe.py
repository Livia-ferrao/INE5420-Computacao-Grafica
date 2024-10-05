from objects.object import Object
from PySide6.QtGui import QPen, QBrush, QColor, QPainterPath
from PySide6.QtCore import Qt
from tools.type import Type
from tools.clipping import Clipping

class Wireframe(Object):
    def __init__(self, name, coord, color, filled):
        super().__init__(name, Type.WIREFRAME, coord, color)
        self.__filled = filled

    def draw(self, window, painter, viewport):
        # Normalizar as coordenadas
        normalized_coords = self.normalizeCoords(window)

        # Determina se vai desenhar o wireframe/parte do wireframe
        (draw, coords) = Clipping.sutherlandHodgeman(normalized_coords, window)

        if draw:
            # Transforma para coordenadas da viewport
            coord_viewport = viewport.calcularCoordsViewport(coords)

            pen = QPen(self.color, 2)
            painter.setPen(pen)

            # Desenhar as linhas do polígono
            for i, (x, y) in enumerate(coord_viewport):
                if i == len(coord_viewport)-1:
                    painter.drawLine(x, y, coord_viewport[0][0], coord_viewport[0][1])
                else:
                    painter.drawLine(x, y, coord_viewport[i+1][0], coord_viewport[i+1][1])

            # Preencher o polígono se estiver configurado
            if self.__filled:
                painter.setBrush(QBrush(self.color, Qt.SolidPattern))
                
                path = QPainterPath()
                path.moveTo(coord_viewport[0][0], coord_viewport[0][1])
                
                for x, y in coord_viewport[1:]:
                    path.lineTo(x, y)
                
                path.lineTo(coord_viewport[0][0], coord_viewport[0][1])
                painter.fillPath(path, QColor(self.color))

    @property
    def filled(self):
        return self.__filled