from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
from numpy import arange
import numpy as np

class BSpline(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.B_SPLINE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm):
        # Normalizar as coordenadas (pontos de controle)
        points_control = self.normalizeCoords(window)
        
        # Calcula os pontos da B-Spline
        points = self.__getDrawingPoints(points_control)

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
    
    # Determinar os pontos da bspline a serem desenhadas linhas entre eles
    def __getDrawingPoints(self, points_control):
        drawing_points = []
        precision = 50
        # Itera sobre os pontos de controle em blocos de 4
        for i in range(3, len(points_control)):
            # Seleciona o segmento de 4 pontos de controle
            segment = points_control[i-3:i+1]
            
            # Calcula as diferenças iniciais para o bloco de pontos de controle
            x_f, x_df, x_d2f, x_d3f, y_f, y_df, y_d2f, y_d3f = self.__getInitialConditions(segment, (1/precision))
            
            drawing_points.extend(self.__forwardDifferences(precision,
                                                            x_f, x_df, x_d2f, x_d3f,
                                                            y_f, y_df, y_d2f, y_d3f))
        return drawing_points
    
    # Determinar condições iniciais para as forward differences
    def __getInitialConditions(self, segment, passo):
        # Matriz B-Spline base
        Mbs = np.array([[-1/6, 3/6, -3/6, 1/6],
                        [3/6, -1, 3/6, 0],
                        [-3/6, 0, 3/6, 0],
                        [1/6, 4/6, 1/6, 0]])

        # Vetores de geometria x e y do segmento
        x_Gbs = [point[0] for point in segment]
        y_Gbs = [point[1] for point in segment]

        # Coeficientes para calcular as condições iniciais
        ax, bx, cx, dx = (np.dot(Mbs, x_Gbs)).tolist()
        ay, by, cy, dy = (np.dot(Mbs, y_Gbs)).tolist()

        passo2 = passo**2
        passo3 = passo**3

        x_f0 = dx
        x_df0 = ax*passo3 + bx*passo2 + cx*passo
        x_d2f0 = 6*ax*passo3 + 2*bx*passo2
        x_d3f0 = 6*ax*passo3
        y_f0 = dy
        y_df0 = ay*passo3 + by*passo2 + cy*passo
        y_d2f0 = 6*ay*passo3 + 2*by*passo2
        y_d3f0 = 6*ay*passo3
        
        return x_f0, x_df0, x_d2f0, x_d3f0, y_f0, y_df0, y_d2f0, y_d3f0
    
    # Calcula pontos de acordo com algoritmo de forward differences
    def __forwardDifferences(self, n, x, x_df, x_d2f, x_d3f, y, y_df, y_d2f, y_d3f):
            points = [(x, y)]
            
            for _ in range(n):
                x += x_df
                x_df += x_d2f
                x_d2f += x_d3f
                y += y_df
                y_df += y_d2f
                y_d2f += y_d3f
                points.append((x, y))
            return points