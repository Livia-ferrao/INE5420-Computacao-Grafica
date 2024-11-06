from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
from numpy import arange

class BerzierCurve(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.BERZIER_CURVE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm, projection_matrix, normalize_matrix, projection):
        # Determina pontos da curva
        points = self.getDrawingPoints(self.coord)

        # Projeta e normaliza
        normalized_coords = self.projectAndNormalize(points, projection_matrix, normalize_matrix, projection)

        # Se len(normalized_coords) for 0 é porque tem algum z <= 0, então não desenha
        if len(normalized_coords) != 0:

            # Desenha linhas entre os pontos
            for i in range(len(normalized_coords)-1):
                line = [normalized_coords[i], normalized_coords[i+1]]
                # Determina se vai desenhar a linha/parte da linha
                if clipping_algorithm ==  ClippingAlgorithm.COHEN:
                    (draw, coords) = Clipping.cohenSutherland(line, window)
                else:
                    (draw, coords) = Clipping.liangBarsky(line, window)

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

    # Determinar os pontos da curva a serem desenhadas linhas entre eles
    def getDrawingPoints(self, coords):
        drawing_points = []

        # Loop para cada curva
        for i in range(0, len(coords)-1, 3):
            # Pontos da curva
            p1 = coords[i]
            p2 = coords[i+1]
            p3 = coords[i+2]
            p4 = coords[i+3]

            # Blending functions da curva
            x = self.__getBlendingFunctions(p1[0], p2[0], p3[0], p4[0])
            y = self.__getBlendingFunctions(p1[1], p2[1], p3[1], p4[1])
            z = self.__getBlendingFunctions(p1[2], p2[2], p3[2], p4[2])

            # Calcula os pontos da curva de acordo com o parametro t e um passo 0.02
            passo = 1/50
            for t in arange(0, 1.01, passo):
                drawing_points.append((x(t), y(t), z(t)))

        return drawing_points
    
    def __getBlendingFunctions(self, p1, p2, p3, p4):
        return lambda t: (p1*(-t**3 + 3*t**2 - 3*t + 1) + p2*(3*t**3 - 6*t**2 + 3*t)
                          + p3*(-3*t**3 + 3*t**2) + p4*t**3)
