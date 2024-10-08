from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
from numpy import arange

class BerzierCurve(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.BERZIER_CURVE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm):
        # Normalizar as coordenadas
        normalized_coords = self.normalizeCoords(window)

        # Determina pontos da curva
        points = self.__getDrawingPoints(normalized_coords)

        # Desenha linhas entre os pontos
        for i in range(len(points)-1):
            line = [points[i], points[i+1]]
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
    def __getDrawingPoints(self, coords):
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

            # Calcula os pontos da curva de acordo com o parametro t e um passo 0.05
            passo = 1/20
            for t in arange(0, 1.01, passo):
                drawing_points.append((x(t), y(t)))

        return drawing_points
    
    def __getBlendingFunctions(self, p1, p2, p3, p4):
        return lambda t: (p1*(-t**3 + 3*t**2 - 3*t + 1) + p2*(3*t**3 - 6*t**2 + 3*t)
                          + p3*(-3*t**3 + 3*t**2) + p4*t**3)
