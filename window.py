import numpy as np
from math import cos, sin
from configurations import Configurations
from windowHandler import WindowHandler
from math import radians
from matrix_generator import MatrixGenerator

class Window:
    def __init__(self):
        # X e Y max e min da window
        self.__xw_min = Configurations.windowXmin()
        self.__xw_max = Configurations.windowXmax()
        self.__yw_min = Configurations.windowYmin()
        self.__yw_max = Configurations.windowYmax()
        self.__edges = [(self.__xw_min, self.__yw_min),
                         (self.__xw_max, self.__yw_min),
                         (self.__xw_min, self.__yw_max),
                         (self.__xw_max, self.__yw_max)]
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

    def atualizaCoordenadaAposRotacao(self, theta):
        (dx, dy) = self.get_center()
        matriz_translacao1 = np.array([[1, 0, 0], [0, 1, 0], [-dx, -dy, 1]])
        matriz_rotacao = np.array(
            [
                [cos(theta), -sin(theta), 0],
                [sin(theta), cos(theta), 0],
                [0, 0, 1],
            ]
        )
        matriz_translacao2 = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        matriz_resultante = np.dot(
            matriz_translacao1, np.dot(matriz_rotacao, matriz_translacao2)
        )
        novos_pontos_lista = []
        for x, y in self.__edges:
            pontos = np.array([[x, y, 1]])
            novos_pontos = np.dot(pontos, matriz_resultante)
            novos_pontos = novos_pontos.tolist()[0][0:2]
            novos_pontos_lista.append(novos_pontos)
        self.__edges = novos_pontos_lista
        
    def rotate_view_up_vector(self, angulo):
        x = self.__view_up_vector[0]
        y = self.__view_up_vector[1]
        coord = self.rotatePoint([(x, y)], angulo)
        self.__view_up_vector = np.array([coord[0][0], coord[0][1]])
    
    def rotatePoint(self, coords, angle):
        rotation_matrix = MatrixGenerator.generateRotationMatrix(angle)
        new_coords = []
        print("ROTACAO MATRIZ", rotation_matrix)
        for i, j in coords:
            print("COORDS", i, j)
            result = np.dot(np.array([[i, j, 1]]), rotation_matrix)
            new_coords.append((result[0][0], result[0][1]))
        print("RESULTADO", new_coords)
        return new_coords
    
    def transform_matrix(self):
        t_np = np.array(self.translating_matrix)
        s_np = np.array(self.scaling_matrix)
        r_np = np.array(self.rotating_matrix)
        result = np.matmul(t_np, np.matmul(s_np, r_np))
        self.transforming_matrix = result.tolist()
        
    def get_center(self):
        x = y = 0
        for i, j in self.__edges:
            x += i
            y += j
        return (x/4, y/4)
        
    def rotateLeft(self, theta):
        self.__angle += theta
        self.__angle_variation += theta
        #print("Angulo: ", self.__angle_variation)

        self.rotate_view_up_vector(-theta)
        self.atualizaCoordenadaAposRotacao(theta)
        #self.windowNormalize()
        
    def windowNormalize(self):        
        # FUNÇÃO self.windowNormalize()
        # CHAMAR PRA Normalizar
        (Wxc, Wyc) = self.get_center()
        #print("centro", Wxc, Wyc)
        #print("Wxc, Wyc", Wxc, Wyc)
        #print("center: ", Wxc, Wyc)
        Sx = 1 / (0.5 * ((self.__xw_max - self.__xw_min)))
        Sy = 1 / (0.5 * ((self.__yw_max - self.__yw_min)))
        #print("S: ", Sx, Sy)
        self.translating_matrix = WindowHandler.create_translating_matrix(-Wxc, -Wyc)
        #print("translating_matrix: \n", self.translating_matrix)
        self.rotating_matrix = WindowHandler.create_rotating_matrix(-self.__angle)
        #print("rotating_matrix: \n ", self.rotating_matrix)
        self.scaling_matrix = WindowHandler.create_scaling_matrix(Sx, Sy)
        #print("scaling_matrix: \n", self.scaling_matrix)
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
        x_viewup = self.__view_up_vector[0]
        y_viewup = self.__view_up_vector[1]
        vector = self.rotatePoint([(x_viewup, y_viewup)], -90)
        vector = np.array([vector[0][0], vector[0][1]])
        #print("VETOR", vector)
        d = d*vector
        translation_matrix = MatrixGenerator.generateTranslationMatrix(d[0], d[1])
        #print("TRANSLATING", translation_matrix)
        new_edges = []
        for x, y in self.__edges:
            new_edge = np.dot(np.array([x, y, 1]), translation_matrix)
            new_edges.append((new_edge[0], new_edge[1]))
            #print("NOVA COORD", new_edges)
        #print("ANTES", self.__edges)
        
        self.__edges = new_edges
        #print("DEPOIS", self.__edges)

    # Movimentação para direita
    def moveRight(self, scale):
        d = (self.__xw_max - self.__xw_min) * (scale/100)
        x_viewup = self.__view_up_vector[0]
        y_viewup = self.__view_up_vector[1]
        vector = self.rotatePoint([(x_viewup, y_viewup)], 90)
        vector = np.array([vector[0][0], vector[0][1]])
        d = d*vector
        translation_matrix = MatrixGenerator.generateTranslationMatrix(d[0], d[1])
        new_edges = []
        for x, y in self.__edges:
            new_edge = np.dot(np.array([x, y, 1]), translation_matrix)
            new_edges.append((new_edge[0], new_edge[1]))
        #print("ANTES", self.__edges)
        
        self.__edges = new_edges
        #print("DEPOIS", self.__edges)

    # Movimentação para cima
    def moveUp(self, scale):
        d = (self.__xw_max - self.__xw_min) * (scale/100)
        d = d*self.__view_up_vector*-1
        translation_matrix = MatrixGenerator.generateTranslationMatrix(d[0], d[1])
        new_edges = []
        for x, y in self.__edges:
            new_edge = np.dot(np.array([x, y, 1]), translation_matrix)
            new_edges.append((new_edge[0], new_edge[1]))
        self.__edges = new_edges

    # Movimentação para baixo
    def moveDown(self, scale):
        d = (self.__xw_max - self.__xw_min) * (scale/100)
        d = d*self.__view_up_vector
        translation_matrix = MatrixGenerator.generateTranslationMatrix(d[0], d[1])
        new_edges = []
        for x, y in self.__edges:
            new_edge = np.dot(np.array([x, y, 1]), translation_matrix)
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
    def angle(self):
        return self.__angle