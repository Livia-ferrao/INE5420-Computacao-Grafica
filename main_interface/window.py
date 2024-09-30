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

        # X e Y max e min da window para controlar o escalonamento
        self.__xw_min = Configurations.windowXmin()
        self.__xw_max = Configurations.windowXmax()
        self.__yw_min = Configurations.windowYmin()
        self.__yw_max = Configurations.windowYmax()

        # Cantos da window
        self.__edges = [(self.__xw_min, self.__yw_min),
                         (self.__xw_max, self.__yw_min),
                         (self.__xw_min, self.__yw_max),
                         (self.__xw_max, self.__yw_max)]

        # View up vector aponta inicialmente para cima
        self.__view_up_vector = [0, 1]

    # Retorna o centro da window
    def __getCenter(self):
        x_cont = y_cont = 0
        for x, y in self.__edges:
            x_cont += x
            y_cont += y
        return (x_cont/4, y_cont/4)
    
    # Movimentação para esquerda
    def moveLeft(self, scale):
        distance = (self.__xw_max - self.__xw_min) * (scale/100)
        (x_viewup, y_viewup) = self.__view_up_vector
        vector = self.__rotatePoint([x_viewup, y_viewup], -90)
        (dx, dy) = (distance*np.array(vector)).tolist()
        self.__move(dx, dy)

    # Movimentação para direita
    def moveRight(self, scale):
        distance = (self.__xw_max - self.__xw_min) * (scale/100)
        (x_viewup, y_viewup) = self.__view_up_vector
        vector = self.__rotatePoint([x_viewup, y_viewup], 90)
        (dx, dy) = (distance*np.array(vector)).tolist()
        self.__move(dx, dy)

    # Movimentação para cima
    def moveUp(self, scale):
        distance = (self.__yw_max - self.__yw_min) * (scale/100)
        (dx, dy) = (distance*np.array(self.__view_up_vector)).tolist()
        self.__move(dx, dy)

    # Movimentação para baixo
    def moveDown(self, scale):
        distance = (self.__yw_max - self.__yw_min) * (scale/100)
        (dx, dy) = (distance*np.array(self.__view_up_vector)*-1).tolist()
        self.__move(dx, dy)

    # Função chamada por todas as movimentações para fazer a movimentação efetiva da window
    def __move(self, dx, dy):
        translation_matrix = MatrixGenerator.generateTranslationMatrix(dx, dy)
        new_edges = []
        for x, y in self.__edges:
            new_edge = np.matmul(np.array([x, y, 1]), translation_matrix)
            new_edges.append((new_edge[0], new_edge[1]))
        self.__edges = new_edges
    
    # Zoom in
    def zoomIn(self, scale):
        scale = scale/100
        dx = ((self.__xw_max - self.__xw_min) * scale)/2
        dy = ((self.__yw_max - self.__yw_min) * scale)/2

        self.__xw_min += dx
        self.__xw_max -= dx
        self.__yw_min += dy
        self.__yw_max -= dy

    # Zoom out
    def zoomOut(self, scale):
        scale = scale/100
        dx = ((self.__xw_max - self.__xw_min) * scale)/2
        dy = ((self.__yw_max - self.__yw_min) * scale)/2

        self.__xw_min -= dx
        self.__xw_max += dx
        self.__yw_min -= dy
        self.__yw_max += dy
    
    # Rotação da window
    def rotate(self, theta):
        self.__view_up_vector = self.__rotatePoint(self.__view_up_vector, theta)
        self.__updateEdges(theta)
    
    # Rotaciona um ponto por um ângulo
    def __rotatePoint(self, point, angle):
        rotation_matrix = MatrixGenerator.generateRotationMatrix(angle)
        result = np.matmul(np.array([point[0], point[1], 1]), rotation_matrix).tolist()[0:2]
        return result
    
    # Atualiza os cantos da window quando uma rotação acontece
    def __updateEdges(self, theta):
        (dx, dy) = self.__getCenter()
        translation_matrix1 = MatrixGenerator.generateTranslationMatrix(-dx, -dy)
        rotation_matrix = MatrixGenerator.generateRotationMatrix(theta)
        translation_matrix2 = MatrixGenerator.generateTranslationMatrix(dx, dy)
        transforming_matrix = np.matmul(translation_matrix1, np.matmul(rotation_matrix, translation_matrix2))

        new_edges = []
        for x, y in self.__edges:
            new_edge = np.matmul(np.array([x, y, 1]), transforming_matrix).tolist()[0:2]
            new_edges.append(new_edge)
        self.__edges = new_edges
    
    # Retorna a matriz de transformação para normalizar os objetos
    def windowNormalize(self):
        # Deslocamento (centro da window) da matriz de translação
        (Wxc, Wyc) = self.__getCenter()

        # Escala da matriz de escalonamento
        Sx = 2/(self.__xw_max - self.__xw_min)
        Sy = 2/(self.__yw_max - self.__yw_min)

        # Ângulo (do view up vector comparado ao vetor para cima [0, 1]) da matriz de rotação
        np_viewup = np.array(self.__view_up_vector)
        angle = np.degrees(np.arctan2(np_viewup[0], np_viewup[1]))

        translating_matrix = MatrixGenerator.generateTranslationMatrix(-Wxc, -Wyc)
        rotating_matrix = MatrixGenerator.generateRotationMatrix(-angle)
        scaling_matrix = MatrixGenerator.generateScalingMatrix(Sx, Sy)
        result = np.matmul(np.matmul(translating_matrix, rotating_matrix), scaling_matrix)
        return result.tolist()

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