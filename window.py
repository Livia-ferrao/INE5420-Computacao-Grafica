import numpy as np
from configurations import Configurations

class Window:
    def __init__(self):
        self.__translating_matrix = self.__createTranslatingMatrix(0, 0)
        self.__scaling_matrix = self.__createScalingMatrix(1, 1)
        self.__transformMatrix()

        # X e Y max e min da window inicial
        self.__xw_min = Configurations.windowXmin()
        self.__xw_max = Configurations.windowXmax()
        self.__yw_min = Configurations.windowYmin()
        self.__yw_max = Configurations.windowYmax()

        # Centro da window (meio que dá de ver na viewport)
        self.__x_center = 0
        self.__y_center = 0
        # X e Y max e min da window atual (que dá de ver na viewport)
        self.__x_min = self.__xw_min
        self.__x_max = self.__xw_max
        self.__y_min = self.__yw_min
        self.__y_max = self.__yw_max
    
    # Matriz de translação
    def __createTranslatingMatrix(self, dx, dy):
        return [[1, 0, 0],
                [0, 1, 0],
                [dx, dy, 1]]
    
    # Matriz de escalonamento
    def __createScalingMatrix(self, sx, sy):
        return [[sx, 0, 0],
                [0, sy, 0],
                [0, 0, 1]]
    
    def __transformMatrix(self):
        t_np = np.array(self.__translating_matrix)
        s_np = np.array(self.__scaling_matrix)
        result = np.matmul(t_np, s_np)
        self.__transforming_matrix = result.tolist()

    # Movimentação para esquerda
    def moveLeft(self, scale):
        d = (self.__x_max - self.__x_min) * (scale/100)
        self.__x_center += d
        self.__translating_matrix = self.__createTranslatingMatrix(self.__x_center, self.__y_center)
        self.__transformMatrix()
    
    # Movimentação para direita
    def moveRight(self, scale):
        d = (self.__x_max - self.__x_min) * (scale/100)
        self.__x_center -= d
        self.__translating_matrix = self.__createTranslatingMatrix(self.__x_center, self.__y_center)
        self.__transformMatrix()
    
    # Movimentação para cima
    def moveUp(self, scale):
        d = (self.__y_max - self.__y_min) * (scale/100)
        self.__y_center -= d
        self.__translating_matrix = self.__createTranslatingMatrix(self.__x_center, self.__y_center)
        self.__transformMatrix()
    
    # Movimentação para baixo
    def moveDown(self, scale):
        d = (self.__y_max - self.__y_min) * (scale/100)
        self.__y_center += d
        self.__translating_matrix = self.__createTranslatingMatrix(self.__x_center, self.__y_center)
        self.__transformMatrix()
    
    # Zoom in
    def zoomIn(self, scale):
        scale = scale/100
        x = ((self.__x_max - self.__x_min) * scale)/2
        y = ((self.__y_max - self.__y_min) * scale)/2

        self.__x_min += x
        self.__x_max -= x
        self.__y_min += y
        self.__y_max -= y

        sx = 2000/(self.__x_max-self.__x_min)
        sy = 2000/(self.__y_max-self.__y_min)
        self.__scaling_matrix = self.__createScalingMatrix(sx, sy)
        self.__transformMatrix()

    # Zoom out
    def zoomOut(self, scale):
        scale = scale/100
        x = ((self.__x_max - self.__x_min) * scale)/2
        y = ((self.__y_max - self.__y_min) * scale)/2

        self.__x_min -= x
        self.__x_max += x
        self.__y_min -= y
        self.__y_max += y

        sx = 2000/(self.__x_max-self.__x_min)
        sy = 2000/(self.__y_max-self.__y_min)
        self.__scaling_matrix = self.__createScalingMatrix(sx, sy)
        self.__transformMatrix()

    @property
    def transforming_matrix(self):
        return self.__transforming_matrix
    
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