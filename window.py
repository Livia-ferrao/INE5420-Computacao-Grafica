import numpy as np
from math import cos, sin
from configurations import Configurations
from windowHandler import WindowHandler
from math import radians

class Window:
    def __init__(self):
        # X e Y max e min da window
        self.__xw_min = Configurations.windowXmin()
        self.__xw_max = Configurations.windowXmax()
        self.__yw_min = Configurations.windowYmin()
        self.__yw_max = Configurations.windowYmax()
        # Vetor aponta inicialmente para cima
        self.__view_up_vector = np.array([0, 1])
        # Ângulo de rotação da window
        self.__angle = 0 
        self.__angle_variation = 0 
        
        # Matrizes
        self.translating_matrix = WindowHandler.create_translating_matrix(1, 1)
        self.scaling_matrix = WindowHandler.create_scaling_matrix(1, 1)
        self.rotating_matrix = WindowHandler.create_rotating_matrix(0)
        self.transforming_matrix = np.identity(3).tolist()

    def atualizaCoordenadaAposRotacao(self):
        if self.__angle_variation != 0:  # Ou seja, houve uma rotacao
            dx, dy = self.get_center()
            matriz_translacao1 = np.array([[1, 0, 0], [0, 1, 0], [-dx, -dy, 1]])
            matriz_rotacao = np.array(
                [
                    [cos(self.__angle_variation), -sin(self.__angle_variation), 0],
                    [sin(self.__angle_variation), cos(self.__angle_variation), 0],
                    [0, 0, 1],
                ]
            )
            matriz_translacao2 = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
            matriz_resultante = np.dot(
                matriz_translacao1, np.dot(matriz_rotacao, matriz_translacao2)
            )
            
            coordenadas = [
                (self.__xw_min, self.__yw_min, 0),
                (self.__xw_max, self.__yw_min, 0),
                (self.__xw_min, self.__yw_max, 0),
                (self.__xw_max, self.__yw_max, 0),
            ]
            
            novos_pontos_lista = []
            for x, y, z in coordenadas:
                pontos = np.array([[x, y, 1]])
                novos_pontos = np.dot(pontos, matriz_resultante)
                novos_pontos = novos_pontos.tolist()[0][0:2]
                novos_pontos.append(z)
                novos_pontos_lista.append(novos_pontos)

            self.__xw_min = novos_pontos_lista[0][0]
            self.__yw_min = novos_pontos_lista[0][1]
            self.__xw_max = novos_pontos_lista[3][0]
            self.__yw_max = novos_pontos_lista[3][1]
            print("NOVOS PONTOS DA LISTA: ", novos_pontos_lista)
            coordenadas = novos_pontos_lista
            
            self.__angle_variation = (
                0  # Coordenadas foram atualizadas, logo reseta o buffer
            )
        
    def rotate_view_up_vector(self, coords, angulo):
        dx, dy = 0, 0
        angulo_rad = np.radians(angulo)

        matriz_translacao1 = WindowHandler.create_translating_matrix(-dx, -dy)
        matriz_rotacao = WindowHandler.create_rotating_matrix(angulo_rad)
        matriz_translacao2 = WindowHandler.create_translating_matrix(dx, dy)
        matriz_resultante = np.dot(matriz_translacao1, np.dot(matriz_rotacao, matriz_translacao2))

        novos_pontos = []
        for i, j in coords:
            pontos = np.array([[i, j, 1]])
            pontos_atualizados = np.dot(pontos, matriz_resultante)
            novos_pontos.append((pontos_atualizados[0][0], pontos_atualizados[0][1]))

        return novos_pontos
        
    def transform_matrix(self):
        t_np = np.array(self.translating_matrix)
        s_np = np.array(self.scaling_matrix)
        r_np = np.array(self.rotating_matrix)
        result = np.matmul(t_np, np.matmul(s_np, r_np))
        self.transforming_matrix = result.tolist()
        
    def get_center(self):
        center_x = (self.__xw_max + self.__xw_min) / 2
        center_y = (self.__yw_max + self.__yw_min) / 2
        return np.array([center_x, center_y])
        
    def rotateLeft(self, theta):
        self.__angle += theta
        self.__angle_variation += theta
        print("Angulo: ", self.__angle_variation)
        
        # FUNÇÃO self.updateViewUpVector()
        # rotaciona o vetor
        n = self.__view_up_vector[0]
        m = self.__view_up_vector[1]
        pontos = self.rotate_view_up_vector([(n, m)], radians(-self.__angle))
        print(pontos)
        n = pontos[0][0]
        m = pontos[0][1]
        self.__view_up_vector = np.array([n, m])
        print("__view_up_vector: ", self.__view_up_vector)
        self.windowNormalize()
        
    def windowNormalize(self):        
        # FUNÇÃO self.windowNormalize()
        # CHAMAR PRA Normalizar
        (Wxc, Wyc) = self.get_center()
        print("center: ", Wxc, Wyc)
        Sx = 1 / (0.5 * ((self.__xw_max - self.__xw_min)/10))
        Sy = 1 / (0.5 * ((self.__yw_max - self.__yw_min)/10))
        print("S: ", Sx, Sy)
        self.translating_matrix = WindowHandler.create_translating_matrix(-Wxc, -Wyc)
        print("translating_matrix: \n", self.translating_matrix)
        self.rotating_matrix = WindowHandler.create_rotating_matrix(-self.__angle)
        print("rotating_matrix: \n ", self.rotating_matrix)
        self.scaling_matrix = WindowHandler.create_scaling_matrix(Sx, Sy)
        print("scaling_matrix: \n", self.scaling_matrix)
        self.transform_matrix()
        
    # def normalizing_coords(self, theta_degrees):
    #     center = self.get_center()
    #     translating_back = MatrixGenerator.generateTranslationMatrix(-center_coord[0], -center_coord[1])
    #     self.__transform(translating_back)
        
    #     TransformHandler.rotate_vector(self.__vup, theta_degrees)
    #     angle_with_y = np.degrees(np.arctan2(*self.__vup[:2]))
    #     TransformHandler.into_ncs(angle_with_y)
   
    #     stranslating_forword = MatrixGenerator.generateTranslationMatrix(-center_coord[0], -center_coord[1])
    #     self.__transform(stranslating_forword)


    # Movimentação para esquerda
    def moveLeft(self, scale):
        d = (self.__xw_max - self.__xw_min) * (scale/100)
        self.__xw_max -= d
        self.__xw_min -= d

    # Movimentação para direita
    def moveRight(self, scale):
        d = (self.__xw_max - self.__xw_min) * (scale/100)
        self.__xw_max += d
        self.__xw_min += d

    # Movimentação para cima
    def moveUp(self, scale):
        d = (self.__yw_max - self.__yw_min) * (scale/100)
        self.__yw_max += d
        self.__yw_min += d

    # Movimentação para baixo
    def moveDown(self, scale):
        d = (self.__yw_max - self.__yw_min) * (scale/100)
        self.__yw_max -= d
        self.__yw_min -= d

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