from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
import numpy as np
from tools.math_utils import MathUtils

class BSplineSurface(Object):
    def __init__(self, name, coord, color, n_lines, n_columns):
        super().__init__(name, Type.BSPLINE_SURFACE, coord, color)
        self.__n_lines = n_lines
        self.__n_columns = n_columns

    def draw(self, window, painter, viewport, clipping_algorithm, projection_matrix, normalize_matrix, projection):
        # Calcula os pontos da B-Spline
        points = self.getDrawingPoints(self.coord)

        for curv in points:
            # Desenha linhas entre os pontos
            for i in range(len(curv)-1):
                line = [curv[i], curv[i+1]]
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
    
    # Determinar os pontos da curva a serem desenhadas linhas entre eles
    def getDrawingPoints(self, points_control):
        drawing_points = []
        n = 21
        delta = 1/(n-1)
        Es, Et_t = self.__createDeltaMatrices(delta)

        # Submatrizes 4x4 da matriz de pontos de controle dada
        submatrices = self.__getSubmatrices(points_control)

        for G in submatrices:
            # DD(s,t)
            DDx, DDy, DDz = self.__getInitialConditionsMatrices(G, Es, Et_t)
            
            # DD(s,t) transposta
            DDx_t = DDx.T.copy()
            DDy_t = DDy.T.copy()
            DDz_t = DDz.T.copy()

            # Gera os pontos das curvas em t ao longo de s
            drawing_points = self.__calculateSurface(DDx, DDy, DDz, n, drawing_points)
            # Gera os pontos das curvas em s ao longo de t
            drawing_points = self.__calculateSurface(DDx_t, DDy_t, DDz_t, n, drawing_points)   
        return drawing_points
    
    def __calculateSurface(self, DDx, DDy, DDz, n, drawing_points):
        for i in range(n):
            # Calcula os pontos da curva com forward differences
            drawing_points.append(MathUtils.forwardDifferences(n,
                                                    DDx[0][0], DDx[0][1], DDx[0][2], DDx[0][3],
                                                    DDy[0][0], DDy[0][1], DDy[0][2], DDy[0][3],
                                                    DDz[0][0], DDz[0][1], DDz[0][2], DDz[0][3]))
            # Atualiza DD(s,t)
            DDx, DDy, DDz = self.__updateDDMatrices(DDx, DDy, DDz)
        return drawing_points

    # Atualizar DD(s,t) em x, y e z
    def __updateDDMatrices(self, DDx, DDy, DDz):
        DDx[0] = DDx[0] + DDx[1]
        DDx[1] = DDx[1] + DDx[2]
        DDx[2] = DDx[2] + DDx[3]
        DDy[0] = DDy[0] + DDy[1]
        DDy[1] = DDy[1] + DDy[2]
        DDy[2] = DDy[2] + DDy[3]
        DDz[0] = DDz[0] + DDz[1]
        DDz[1] = DDz[1] + DDz[2]
        DDz[2] = DDz[2] + DDz[3]
        return DDx, DDy, DDz
    
    # Determinar matriz das condições iniciais DD(s,t)
    def __getInitialConditionsMatrices(self, G, Es, Et_t):
            Bbs = np.array([[-1/6, 3/6, -3/6, 1/6],
                        [3/6, -1, 3/6, 0],
                        [-3/6, 0, 3/6, 0],
                        [1/6, 4/6, 1/6, 0]])
            Bbs_t = Bbs.T.copy()

            Gx = np.array([[p[0] for p in line] for line in G])
            Gy = np.array([[p[1] for p in line] for line in G])
            Gz = np.array([[p[2] for p in line] for line in G])

            Cx = np.matmul(np.matmul(Bbs, Gx), Bbs_t)
            Cy = np.matmul(np.matmul(Bbs, Gy), Bbs_t)
            Cz = np.matmul(np.matmul(Bbs, Gz), Bbs_t)
            
            DDx = np.matmul(np.matmul(Es, Cx), Et_t)
            DDy = np.matmul(np.matmul(Es, Cy), Et_t)
            DDz = np.matmul(np.matmul(Es, Cz), Et_t)
            return DDx, DDy, DDz

    # Cria as matrizes E(delta_s) e E(delta_t) transposta
    def __createDeltaMatrices(self,delta):
        delta2 = delta ** 2
        delta3 = delta ** 3
        E = np.array([[0, 0, 0, 1],
                      [delta3, delta2, delta, 0],
                      [6*delta3, 2*delta2, 0, 0],
                      [6*delta3, 0, 0, 0]])

        return E, E.T.copy()
    
    # Percorrer a matriz de pontos de controle e pegar as submatrizes 4x4
    def __getSubmatrices(self, matrix):
        submatrices = []
        for line in range(self.__n_lines - 3):
            for column in range(self.__n_columns - 3):
                submatrix = []
                for i in range(4):
                    inicio = (line + i) * self.__n_columns + column
                    submatrix.append(matrix[inicio:inicio+4])
                submatrices.append(np.array(submatrix))
        return submatrices
    
    @property
    def n_lines(self):
        return self.__n_lines
    
    @property
    def n_columns(self):
        return self.__n_columns