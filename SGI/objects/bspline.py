from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
from numpy import arange
import numpy as np
from tools.math_utils import MathUtils

class BSpline(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.B_SPLINE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm, projection_matrix, normalize_matrix, projection):
        # Calcula os pontos da B-Spline
        points = self.getDrawingPoints(self.coord)

        # Desenha linhas entre os pontos
        for i in range(len(points)-1):
            line = [points[i], points[i+1]]

            line = self.projectAndNormalize(line, projection_matrix, normalize_matrix, projection)

            # Se len(line) =! 0, ou seja, se z > 0 nos 2 pontos da linha
            if len(line) != 0:
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
    def getDrawingPoints(self, points_control):
        drawing_points = []
        precision = 51
        # Itera sobre os pontos de controle em blocos de 4
        for i in range(3, len(points_control)):
            # Seleciona o segmento de 4 pontos de controle
            segment = points_control[i-3:i+1]
            
            # Calcula as diferenças iniciais para o bloco de pontos de controle
            x_f, x_df, x_d2f, x_d3f, y_f, y_df, y_d2f, y_d3f, z_f, z_df, z_d2f, z_d3f = self.__getInitialConditions(segment, (1/(precision-1)))
            
            drawing_points.extend(MathUtils.forwardDifferences(precision,
                                                            x_f, x_df, x_d2f, x_d3f,
                                                            y_f, y_df, y_d2f, y_d3f,
                                                            z_f, z_df, z_d2f, z_d3f))
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
        z_Gbs = [point[2] for point in segment]

        # Coeficientes para calcular as condições iniciais
        ax, bx, cx, dx = (np.dot(Mbs, x_Gbs)).tolist()
        ay, by, cy, dy = (np.dot(Mbs, y_Gbs)).tolist()
        az, bz, cz, dz = (np.dot(Mbs, z_Gbs)).tolist()

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
        z_f0 = dz
        z_df0 = az*passo3 + bz*passo2 + cz*passo
        z_d2f0 = 6*az*passo3 + 2*bz*passo2
        z_d3f0 = 6*az*passo3
        
        return x_f0, x_df0, x_d2f0, x_d3f0, y_f0, y_df0, y_d2f0, y_d3f0, z_f0, z_df0, z_d2f0, z_d3f0
