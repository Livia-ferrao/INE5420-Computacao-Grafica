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

        # Ponto máximo e mínimo da altura e largura da window para controlar o escalonamento
        self.__w_min = Configurations.windowXmin()
        self.__w_max = Configurations.windowXmax()
        self.__h_min = Configurations.windowYmin()
        self.__h_max = Configurations.windowYmax()

        self.__center = (0, 0, 0)
        self.__x_angle = 0
        self.__y_angle = 0
        self.__z_angle = 0
        
        # Distância do observador para projeção em perspectiva
        self.__d = 5.0  # valor ajustável para efeito de profundidade

     # Ajuste do parâmetro de profundidade para projeção em perspectiva
    def setObserverDistance(self, distance):
        self.__d = distance
        
    # Movimentação para esquerda
    def moveLeft(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(-distance, 0, 0)

   # Movimentação para direita
    def moveRight(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(distance, 0, 0)

    # Movimentação para cima
    def moveUp(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, distance, 0)

    # Movimentação para baixo
    def moveDown(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, -distance, 0)

    # Movimentação para frente
    def moveFront(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, 0, distance)

    # Movimentação para trás
    def moveBack(self, scale):
        distance = (self.__w_max - self.__w_min) * (scale/100)
        self.__move(0, 0, -distance)

    # Função chamada por todas as movimentações para mover a window efetivamente
    def __move(self, dx, dy, dz):
        x = self.__center[0] + dx
        y = self.__center[1] + dy
        z = self.__center[2] + dz
        self.__center = (x, y, z)

    # Zoom in
    def zoomIn(self, scale):
        scale = scale / 100
        dw = ((self.__w_max - self.__w_min) * scale) / 2
        dh = ((self.__h_max - self.__h_min) * scale) / 2

        self.__w_min += dw
        self.__w_max -= dw
        self.__h_min += dh
        self.__h_max -= dh

    # Zoom out
    def zoomOut(self, scale):
        scale = scale / 100
        dw = ((self.__w_max - self.__w_min) * scale) / 2
        dh = ((self.__h_max - self.__h_min) * scale) / 2

        self.__w_min -= dw
        self.__w_max += dw
        self.__h_min -= dh
        self.__h_max += dh
    
    # Rotaciona a window no eixo z
    def rotate_z_axis(self, theta):
        self.__z_angle += theta
    
    # Rotaciona no eixo x
    def rotate_x_axis(self, theta):
        self.__x_angle += theta

    # Rotaciona no eixo y
    def rotate_y_axis(self, theta):
        self.__y_angle += theta
    
    # Retorna a matriz de transformação para normalizar os objetos
    def windowNormalize(self):
        (Wxc, Wyc, _) = self.__center

        Sx = 2 / (self.__w_max - self.__w_min)
        Sy = 2 / (self.__h_max - self.__h_min)

        # Translação já é feita na projeção paralela
        translating_matrix = MatrixGenerator.generateTranslationMatrix(-Wxc, -Wyc)
        rotating_matrix = MatrixGenerator.generateRotationMatrix(-self.__z_angle)
        scaling_matrix = MatrixGenerator.generateScalingMatrix(Sx, Sy)
        result = np.matmul(np.matmul(translating_matrix, rotating_matrix), scaling_matrix)
        # result = np.matmul(rotating_matrix, scaling_matrix)
        return result.tolist()

    # Retorna a matriz de projeção paralela ortogonal para projetar os objetos no espaço 3D
    def getParallelProjectionMatrix(self):
        vpr = self.__center
        translating_vpr = MatrixGenerator.generateTranslationMatrix3D(-vpr[0], -vpr[1], -vpr[2])
        rotating_x = MatrixGenerator.generateRotationMatrix3D_X(-self.__x_angle)
        rotating_y = MatrixGenerator.generateRotationMatrix3D_Y(-self.__y_angle)
        result = np.matmul(np.matmul(translating_vpr, rotating_x), rotating_y)
        return result

    def getPerspectiveProjectionMatrix(self):
        d = 800
        perspective_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, -1/d, 1]
        ])
        
        vpr = self.__center
        # translating_vpr = MatrixGenerator.generateTranslationMatrix3D(-vpr[0], -vpr[1], -vpr[2])
        rotating_x = MatrixGenerator.generateRotationMatrix3D_X(-self.__x_angle)
        rotating_y = MatrixGenerator.generateRotationMatrix3D_Y(-self.__y_angle)

        # Combina translação, rotação e projeção em perspectiva
        # result = np.matmul(np.matmul(np.matmul(translating_vpr, rotating_x), rotating_y), perspective_matrix)
        result = np.matmul(np.matmul(rotating_x, rotating_y), perspective_matrix)

        return result
    
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
    def x_angle(self):
        return self.__x_angle
    
    @property
    def y_angle(self):
        return self.__y_angle
    
    @property
    def z_angle(self):
        return self.__z_angle
