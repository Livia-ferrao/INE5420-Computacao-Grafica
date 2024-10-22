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
    
    def projectAndNormalize(self, project, normalize):
        project_coords = []
        for x, y, z in self.coord:
            transformed_coord = (np.dot(np.array([x, y, z, 1]), np.array(project))).tolist()
            project_coords.append(transformed_coord[:2])
        normalize_coords = []
        for x, y in project_coords:
            transformed_coord = (np.dot(np.array([x, y, 1]), np.array(normalize))).tolist()
            normalize_coords.append(transformed_coord[:2])
        return normalize_coords
    
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
