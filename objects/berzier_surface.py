from objects.object import Object
from PySide6.QtGui import QPen
from tools.type import Type, ClippingAlgorithm
from tools.clipping import Clipping
import numpy as np

class BerzierSurface(Object):
    def __init__(self, name, coord, color):
        super().__init__(name, Type.BERZIER_SURFACE, coord, color)

    def draw(self, window, painter, viewport, clipping_algorithm, projection_matrix, normalize_matrix, projection):
        # Determina pontos da curva
        points = self.getDrawingPoints(self.coord)

        curvs = []
        for curv in points:
            # Projeta e normaliza cada curva
            normalized_coords = self.projectAndNormalize(curv, projection_matrix, normalize_matrix, projection)

            # Se len(normalized_coords) for 0 é porque tem algum z <= 0, então não desenha
            if len(normalized_coords) == 0:
                return
            
            curvs.append(normalized_coords)

        # Se len(normalized_coords) =! 0 para todas as curvas, ou seja, se z > 0 em todos os pontos da superfície
        for curv in curvs:
            # Desenha linhas entre os pontos
            for i in range(len(curv)-1):
                line = [curv[i], curv[i+1]]
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

        # Loop para cada matriz
        for i in range(0, len(coords)-1, 16):
            p11 = coords[i]
            p12 = coords[i+1]
            p13 = coords[i+2]
            p14 = coords[i+3]
            p21 = coords[i+4]
            p22 = coords[i+5]
            p23 = coords[i+6]
            p24 = coords[i+7]
            p31 = coords[i+8]
            p32 = coords[i+9]
            p33 = coords[i+10]
            p34 = coords[i+11]
            p41 = coords[i+12]
            p42 = coords[i+13]
            p43 = coords[i+14]
            p44 = coords[i+15]

            # Mb x Gb x Mb_transposta para x, y e z
            Mb_Gbx_Mb = self.__getMbGbMb(p11[0], p12[0], p13[0], p14[0],
                                        p21[0], p22[0], p23[0], p24[0],
                                        p31[0], p32[0], p33[0], p34[0],
                                        p41[0], p42[0], p43[0], p44[0])
            Mb_Gby_Mb = self.__getMbGbMb(p11[1], p12[1], p13[1], p14[1],
                                        p21[1], p22[1], p23[1], p24[1],
                                        p31[1], p32[1], p33[1], p34[1],
                                        p41[1], p42[1], p43[1], p44[1])
            Mb_Gbz_Mb = self.__getMbGbMb(p11[2], p12[2], p13[2], p14[2],
                                        p21[2], p22[2], p23[2], p24[2],
                                        p31[2], p32[2], p33[2], p34[2],
                                        p41[2], p42[2], p43[2], p44[2])
            
            passo = 1/20
            # Curvas alterando o parametro s e mantendo o t
            curvs_vertical = [[] for _ in range(21)]

            # Itera pelos valores do parametro s
            for s in np.arange(0, 1.01, passo):
                S_Mb_Gbx_Mb = self.__applyS(s, Mb_Gbx_Mb)
                S_Mb_Gby_Mb = self.__applyS(s, Mb_Gby_Mb)
                S_Mb_Gbz_Mb = self.__applyS(s, Mb_Gbz_Mb)

                # Curvas alterando o parametro t e mantendo o s
                curv = []
                i = 0
                for t in np.arange(0, 1.01, passo):
                    x = self.__applyT(t, S_Mb_Gbx_Mb)
                    y = self.__applyT(t, S_Mb_Gby_Mb)
                    z = self.__applyT(t, S_Mb_Gbz_Mb)
                    curv.append((x, y, z))
                    curvs_vertical[i].append((x, y, z))
                    i += 1
                drawing_points.append(curv)
            for c in curvs_vertical:
                drawing_points.append(c)

        return drawing_points
    
    # Faz a multiplicação Mb x Gb x Mb_transposta
    def __getMbGbMb(self, p11, p12, p13, p14, p21, p22, p23, p24, p31, p32, p33, p34, p41, p42, p43, p44):
        Mb = np.array([[-1, 3, -3, 1],
                    [3, -6, 3, 0],
                    [-3, 3, 0, 0],
                    [1, 0, 0, 0]])
        Gb = np.array([[p11, p12, p13, p14],
                       [p21, p22, p23, p24],
                       [p31, p32, p33, p34],
                       [p41, p42, p43, p44]])
        return np.matmul(np.matmul(Mb, Gb), Mb)
    
    # Faz a multiplicação S x matrix (matrix será Mb x Gb x Mb_transposta)
    # Nessa multiplicação o parâmetro s já é substituído por um valor
    def __applyS(self, s, matrix):
        S = np.array([[s**3, s**2, s, 1]])
        return np.matmul(S, matrix)
    
    # Faz a multiplicação matrix x T_transposta (matrix será S x Mb x Gb x Mb_transposta)
    # Nessa multiplicação o parâmetro t já é substituído por um valor
    def __applyT(self, t, matrix):
        T = np.array([[t**3], [t**2], [t], [1]])
        result = np.matmul(matrix, T)
        return result[0][0]

