from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping

class Line(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.LINE, coord, color)
    
    def draw(self, window, painter, viewport, clipping_algorithm, projection_matrix, normalize_matrix, projection):
        # Projeta e normaliza
        normalized_coords = self.projectAndNormalize(self.coord, projection_matrix, normalize_matrix, projection)

        # Se len(normalized_coords) for 0 é porque tem algum z <= 0, então não desenha
        if len(normalized_coords) != 0:
            if clipping_algorithm ==  ClippingAlgorithm.COHEN:
                (draw, coords) = Clipping.cohenSutherland(normalized_coords, window)
            else:
                (draw, coords) = Clipping.liangBarsky(normalized_coords, window)

            if draw:
                # Transforma para coordenadas da viewport
                coord_viewport = viewport.calcularCoordsViewport(coords)

                # Desenha a linha
                pen = QPen(self.color, 2)
                painter.setPen(pen)
                painter.drawLine(
                    coord_viewport[0][0],
                    coord_viewport[0][1],
                    coord_viewport[1][0],
                    coord_viewport[1][1]
                )