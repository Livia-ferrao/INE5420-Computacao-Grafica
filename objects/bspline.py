from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
from numpy import arange

class BSpline(Object):
    def __init__(self, name, coord, color, n_precision):
        self.n_precision = n_precision
        super().__init__(name, Type.BERZIER_CURVE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm):
        print("entrou aqui")
        # Normalizar as coordenadas (pontos de controle)
        points_control = self.normalizeCoords(window)

        # Determina pontos da curva
        points_precision = self.n_precision
        
        points = self.bspline(points_control, points_precision)

        # # Desenha linhas entre os pontos
        # for i in range(len(points)-1):
        #     line = [points[i], points[i+1]]
        #     # Determina se vai desenhar a linha/parte da linha
        #     if clipping_algorithm ==  ClippingAlgorithm.COHEN:
        #         (draw, coords) = Clipping.cohenSutherland(line, window)
        #     else:
        #         (draw, coords) = Clipping.liangBarsky(line, window)

        #     if draw:
        #         # Transforma para coordenadas da viewport
        #         coord_viewport = viewport.calcularCoordsViewport(coords)

        #         # Desenha a linha
        #         pen = QPen(self.color, 2)
        #         painter.setPen(pen)
        #         painter.drawLine(
        #             coord_viewport[0][0],
        #             coord_viewport[0][1],
        #             coord_viewport[1][0],
        #             coord_viewport[1][1]
        #         )

    # def bspline(self, pontos_controle, precisao):
    #     pontos_spline = []

    #     for i in range(len(pontos_controle)):
    #         limite_superior = i + 4

    #         if limite_superior > len(pontos_controle):
    #             break
    #         pontos = pontos_controle[i:limite_superior]

    #         delta_x, delta_y = ObjectOperations.calcular_coeficientes(
    #             pontos, (1 / precisao)
    #         )
    #         x = delta_x[0]
    #         y = delta_y[0]
    #         pontos_spline.append((x, y))
    #         for k in range(precisao):
    #             x += delta_x[1]
    #             delta_x[1] += delta_x[2]
    #             delta_x[2] += delta_x[3]

    #             y += delta_y[1]
    #             delta_y[1] += delta_y[2]
    #             delta_y[2] += delta_y[3]

    #             pontos_spline.append((x, y))
    #     return pontos_spline