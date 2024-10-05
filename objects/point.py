from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type
from tools.clipping import Clipping

class Point(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.POINT, coord, color)
    
    def draw(self, window, painter, viewport):
        # Normalizar as coordenadas
        normalized_coords = self.normalizeCoords(window)

        # Determina se vai desenhar o ponto
        (draw, coords) = Clipping.pointClipping(normalized_coords, window)

        if draw:
            # Transforma para coordenadas da viewport
            coord_viewport = viewport.calcularCoordsViewport(coords)

            # Desenha o ponto
            pen = QPen(self.color, 2)
            painter.setPen(pen)
            painter.drawPoint(coord_viewport[0][0], coord_viewport[0][1])
