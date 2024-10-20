import numpy as np
from main_interface.configurations import Configurations
from tools.matrix_generator import MatrixGenerator

class Window:
    def __init__(self):
        # X e Y max e min normalizados
        self.__xmin_scn = -1
        self.__xmax_scn = 1
        self.__ymin_scn = -1
        self.__ymax_scn = 1
        self.__zmin_scn = -1
        self.__zmax_scn = 1

        # X e Y max e min da window para controlar o escalonamento
        self.__xw_min = Configurations.windowXmin()
        self.__xw_max = Configurations.windowXmax()
        self.__yw_min = Configurations.windowYmin()
        self.__yw_max = Configurations.windowYmax()
        self.__zw_min = Configurations.windowZmin()
        self.__zw_max = Configurations.windowZmax()

        # Cantos da window 3D (4 cantos da base + 4 cantos do topo)
        self.__edges = [(self.__xw_min, self.__yw_min, self.__zw_min),
                         (self.__xw_max, self.__yw_min, self.__zw_min),
                         (self.__xw_min, self.__yw_max, self.__zw_min),
                         (self.__xw_max, self.__yw_max, self.__zw_min),
                         (self.__xw_min, self.__yw_min, self.__zw_max),
                         (self.__xw_max, self.__yw_min, self.__zw_max),
                         (self.__xw_min, self.__yw_max, self.__zw_max),
                         (self.__xw_max, self.__yw_max, self.__zw_max)]

        # View up vector aponta inicialmente para cima
        self.__view_up_vector = [0, 1, 0]

    # Retorna o centro da window
    def __getCenter(self):
        x_cont = y_cont = z_cont = 0
        for x, y, z in self.__edges:
            x_cont += x
            y_cont += y
            z_cont += z
        return (x_cont/8, y_cont/8, z_cont/8)
    
    # Movimentação para esquerda
    def moveLeft(self, scale):
        distance = (self.__xw_max - self.__xw_min) * (scale/100)
        vector = self.__rotatePoint([self.__view_up_vector[0], self.__view_up_vector[1], 0], -90)
        (dx, dy, dz) = (distance * np.array(vector)).tolist()
        self.__move(dx, dy, dz)

   # Movimentação para direita
    def moveRight(self, scale):
        distance = (self.__xw_max - self.__xw_min) * (scale/100)
        vector = self.__rotatePoint([self.__view_up_vector[0], self.__view_up_vector[1], 0], 90)
        (dx, dy, dz) = (distance * np.array(vector)).tolist()
        self.__move(dx, dy, dz)

    # Movimentação para cima
    def moveUp(self, scale):
        distance = (self.__yw_max - self.__yw_min) * (scale/100)
        (dx, dy, dz) = (distance * np.array(self.__view_up_vector)).tolist()
        self.__move(dx, dy, dz)

    # Movimentação para baixo
    def moveDown(self, scale):
        distance = (self.__yw_max - self.__yw_min) * (scale/100)
        (dx, dy, dz) = (distance * np.array(self.__view_up_vector) * -1).tolist()
        self.__move(dx, dy, dz)

    # Função chamada por todas as movimentações para mover a window efetivamente
    def __move(self, dx, dy, dz):
        translation_matrix = MatrixGenerator.generateTranslationMatrix3D(dx, dy, dz)
        new_edges = []
        for x, y, z in self.__edges:
            new_edge = np.matmul(np.array([x, y, z, 1]), translation_matrix)
            new_edges.append((new_edge[0], new_edge[1], new_edge[2]))
        self.__edges = new_edges

    # Zoom in
    def zoomIn(self, scale):
        scale = scale / 100
        dx = ((self.__xw_max - self.__xw_min) * scale) / 2
        dy = ((self.__yw_max - self.__yw_min) * scale) / 2
        dz = ((self.__zw_max - self.__zw_min) * scale) / 2

        self.__xw_min += dx
        self.__xw_max -= dx
        self.__yw_min += dy
        self.__yw_max -= dy
        self.__zw_min += dz
        self.__zw_max -= dz

    # Zoom out
    def zoomOut(self, scale):
        scale = scale / 100
        dx = ((self.__xw_max - self.__xw_min) * scale) / 2
        dy = ((self.__yw_max - self.__yw_min) * scale) / 2
        dz = ((self.__zw_max - self.__zw_min) * scale) / 2

        self.__xw_min -= dx
        self.__xw_max += dx
        self.__yw_min -= dy
        self.__yw_max += dy
        self.__zw_min -= dz
        self.__zw_max += dz
    
    # Rotação da window
    def rotate(self, theta):
        self.__view_up_vector = self.__rotatePoint(self.__view_up_vector, theta)
        self.__updateEdges(theta)
    
    # Rotaciona um ponto 3D por um ângulo em torno de um eixo
    def __rotatePoint(self, point, angle, axis='z'):
        rotation_matrix = MatrixGenerator.generateRotationMatrix3D(angle, axis)
        result = np.matmul(np.array([point[0], point[1], point[2], 1]), rotation_matrix).tolist()[:3]
        return result
    
    # Atualiza os cantos da window quando uma rotação acontece
    def __updateEdges(self, theta, axis='z'):
        (dx, dy, dz) = self.__getCenter()
        translation_matrix1 = MatrixGenerator.generateTranslationMatrix3D(-dx, -dy, -dz)
        rotation_matrix = MatrixGenerator.generateRotationMatrix3D(theta, axis)
        translation_matrix2 = MatrixGenerator.generateTranslationMatrix3D(dx, dy, dz)
        transforming_matrix = np.matmul(translation_matrix1, np.matmul(rotation_matrix, translation_matrix2))

        new_edges = []
        for x, y, z in self.__edges:
            new_edge = np.matmul(np.array([x, y, z, 1]), transforming_matrix).tolist()[:3]
            new_edges.append(new_edge)
        self.__edges = new_edges
    
     # Retorna a matriz de transformação para normalizar os objetos no espaço 3D
    def windowNormalize3D(self):
        (Wxc, Wyc, Wzc) = self.__getCenter()

        Sx = 2 / (self.__xw_max - self.__xw_min)
        Sy = 2 / (self.__yw_max - self.__yw_min)
        Sz = 2 / (self.__zw_max - self.__zw_min)

        np_viewup = np.array(self.__view_up_vector)
        angle = np.degrees(np.arctan2(np_viewup[0], np_viewup[1]))

        translating_matrix = MatrixGenerator.generateTranslationMatrix3D(-Wxc, -Wyc, -Wzc)
        rotating_matrix = MatrixGenerator.generateRotationMatrix3D(-angle, axis='z')
        scaling_matrix = MatrixGenerator.generateScalingMatrix3D(Sx, Sy, Sz)
        result = np.matmul(np.matmul(translating_matrix, rotating_matrix), scaling_matrix)
        return result.tolist()

    def getParallelProjectionMatrix(self):
        vpr = self.__getCenter()
        translating_vpr = MatrixGenerator.generateTranslationMatrix3D(-vpr[0], -vpr[1], -vpr[2])
        np_viewup = np.array(self.__view_up_vector)
        theta_x = np.degrees(np.arctan2(np_viewup[1], np_viewup[2]))
        theta_y = np.degrees(np.arctan2(np_viewup[0], np_viewup[1]))
        rotating_x = MatrixGenerator.generateRotationMatrix3D(-theta_x, axis='x')
        rotating_y = MatrixGenerator.generateRotationMatrix3D(-theta_y, axis='y')
        result = np.matmul(np.matmul(translating_vpr, rotating_x), rotating_y)
        return result

    @property
    def xw_min(self):
        return self.__xw_min
    
    @property
    def xw_max(self):
        return self.__xw_max
    
    @property
    def yw_min(self):
        return self.__yw_min
    
    @property
    def yw_max(self):
        return self.__yw_max

    @property
    def zw_min(self):
        return self.__zw_min
    
    @property
    def zw_max(self):
        return self.__zw_max
    
    @property
    def view_up_vector(self):
        return self.__view_up_vector
    
    @property
    def xmin_scn(self):
        return self.__xmin_scn

    @property
    def xmax_scn(self):
        return self.__xmax_scn
    
    @property
    def ymin_scn(self):
        return self.__ymin_scn
    
    @property
    def ymax_scn(self):
        return self.__ymax_scn

    @property
    def zmin_scn(self):
        return self.__zmin_scn
    
    @property
    def zmax_scn(self):
        return self.__zmax_scn