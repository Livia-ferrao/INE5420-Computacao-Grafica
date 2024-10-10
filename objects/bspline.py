from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
from numpy import arange
import numpy as np

class BSpline(Object):
    def __init__(self, name, coord, color, n_precision):
        self.n_precision = n_precision
        super().__init__(name, Type.BERZIER_CURVE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm):
        # Normalizar as coordenadas (pontos de controle)
        points_control = self.normalizeCoords(window)

        # Determina pontos da curva
        points_precision = self.n_precision
        
        # Calcula os pontos da B-Spline
        points = self.bspline(points_control, points_precision)
        
        print("points: ", points )

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
                
    def calculate_differences(self, delta, a, b, c, d):
        # Calcula as diferenças iniciais para os coeficientes de uma curva cúbica
        delta_2 = delta**2
        delta_3 = delta**3
        return [
            d,
            a * delta_3 + b * delta_2 + c * delta,
            6 * a * delta_3 + 2 * b * delta_2,
            6 * a * delta_3,
        ]

    def calculate_coefficients(self, points, delta):
        # Matriz de coeficientes para o cálculo da B-Spline
        MBS = np.array(
            [
                [(-1 / 6), (1 / 2), (-1 / 2), (1 / 6)],
                [(1 / 2), -1, (1 / 2), 0],
                [(-1 / 2), 0, (1 / 2), 0],
                [(1 / 6), (2 / 3), (1 / 6), 0],
            ]
        )

        # Vetores das coordenadas x e y dos pontos de controle
        GBS_x = []
        GBS_y = []
        for x, y in points:
            GBS_x.append(x)
            GBS_y.append(y)

        # Calcula as diferenças iniciais para x e y
        GBS_x = np.array([GBS_x]).T
        coeff_x = MBS.dot(GBS_x).T[0]
        dif_initial_x = self.calculate_differences(delta, *coeff_x)

        GBS_y = np.array([GBS_y]).T
        coeff_y = MBS.dot(GBS_y).T[0]
        dif_initial_y = self.calculate_differences(delta, *coeff_y)
        
        return dif_initial_x, dif_initial_y

    def bspline(self, points_control, points_precision):
        points_spline = []
        
        # Itera sobre os pontos de controle em blocos de 4
        for i in range(len(points_control)):
            upper_limit = i + 4

            if upper_limit > len(points_control):
                break
            
            # Seleciona o bloco de 4 pontos de controle
            points = points_control[i:upper_limit]
            
            # Calcula as diferenças iniciais para o bloco de pontos de controle
            delta_x, delta_y = self.calculate_coefficients(
                points, (1 / points_precision)
            )
            x = delta_x[0]
            y = delta_y[0]
            points_spline.append((x, y))
            
            # Calcula os demais pontos da curva usando diferenças sucessivas
            for k in range(points_precision):
                x += delta_x[1]
                delta_x[1] += delta_x[2]
                delta_x[2] += delta_x[3]

                y += delta_y[1]
                delta_y[1] += delta_y[2]
                delta_y[2] += delta_y[3]

                points_spline.append((x, y))
        return points_spline