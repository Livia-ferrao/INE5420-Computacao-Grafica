from objects.object import Object
from tools.type import Type, ClippingAlgorithm
from PySide6.QtGui import QPen
from tools.clipping import Clipping

class Object3D(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.OBJECT_3D, coord, color)
    
    def draw(self, window, painter, viewport, clipping_algorithm, projection_matrix, normalize_matrix, projection):
        # Projeta e normaliza
        normalized_coords = self.projectAndNormalize(self.coord, projection_matrix, normalize_matrix, projection)

        # Se len(normalized_coords) for 0 é porque tem algum z <= 0, então não desenha
        if len(normalized_coords) != 0:

            # Criar arestas (linhas) ligando os pontos consecutivos
            edges = [((normalized_coords[i]), (normalized_coords[i + 1])) for i in range(0, len(normalized_coords) - 1, 2)]
            
            # Desenhar cada uma das arestas como retas 2D normalizadas
            for i in edges:
                line = [i[0], i[1]]

                # Determina se vai desenhar a aresta ou parte da aresta
                if clipping_algorithm == ClippingAlgorithm.COHEN:
                    draw, coords = Clipping.cohenSutherland(line, window)
                else:
                    draw, coords = Clipping.liangBarsky(line, window)

                if draw:
                    # Transforma para coordenadas da viewport
                    coord_viewport = viewport.calcularCoordsViewport(coords)

                    # Desenha a aresta
                    pen = QPen(self.color, 2)
                    painter.setPen(pen)
                    painter.drawLine(
                        coord_viewport[0][0],
                        coord_viewport[0][1],
                        coord_viewport[1][0],
                        coord_viewport[1][1]
                    )
