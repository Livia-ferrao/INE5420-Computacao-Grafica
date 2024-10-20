from abc import ABC, abstractmethod
import numpy as np

class Object(ABC):
    def __init__(self, name, tipo, coord, color):
        self.__name = name
        self.__tipo = tipo
        self.__coord = coord
        self.__color = color

    @abstractmethod
    def draw(*args, **kwargs):
        pass

     # Normaliza as coordenadas no espaço 3D
    def normalizeCoords(self, window):
        transforming_matrix = window.windowNormalize3D()

        normalized_coords = []
        for x, y, z in self.coord:
            transformed_coord = (np.dot(np.array([x, y, z, 1]), np.array(transforming_matrix))).tolist()
            normalized_coords.append(transformed_coord[:3])  # Mantém apenas as coordenadas 3D normalizadas
        return normalized_coords
    
    def project(self, window):
        projection_matrix = window.getParallelProjectionMatrix()
        projected_coords = []
        for x, y, z in self.coord:
            transformed_coord = (np.dot(np.array([x, y, z, 1]), np.array(projection_matrix))).tolist()
            projected_coords.append(transformed_coord[:3])  # Mantém apenas as coordenadas 3D normalizadas
        return projected_coords
    
    def projectAndNormalizeCoords(self, window):
        projection_matrix = window.getParallelProjectionMatrix()
        normalizing_matrix = window.windowNormalize3D()
        transforming_matrix = np.matmul(projection_matrix, normalizing_matrix)
        resulting_coords = []
        for x, y, z in self.coord:
            transformed_coord = (np.dot(np.array([x, y, z, 1]), np.array(transforming_matrix))).tolist()
            resulting_coords.append(transformed_coord[:3])  # Mantém apenas as coordenadas 3D normalizadas
        return resulting_coords
    
    @property
    def name(self):
        return self.__name
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def coord(self):
        return self.__coord
    
    @property
    def color(self):
        return self.__color
    
    @name.setter
    def name(self, new_name):
        self.__name = new_name
    
    @coord.setter
    def coord(self, new_coord):
        self.__coord = new_coord

    @color.setter
    def color(self, new_color):
        self.__color = new_color
    
    # Calcula o centro do objeto 3D
    def getCenter(self):
        coord_len = len(self.__coord)
        center_x = center_y = center_z = 0
        for x, y, z in self.__coord:
            center_x += x / coord_len
            center_y += y / coord_len
            center_z += z / coord_len
        return (center_x, center_y, center_z)
