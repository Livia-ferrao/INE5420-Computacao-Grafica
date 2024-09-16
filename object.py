from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, name, tipo, coord, color):
        self.__name = name
        self.__tipo = tipo
        self.__coord = coord
        self.__color = color

    @abstractmethod
    def draw(self, transformed_coord, painter):
        pass

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
    
    def get_center(self):
        coord_len = len(self.__coord)
        center_x = center_y = 0
        for x, y in self.__coord:
            center_x += x/coord_len
            center_y += y/coord_len
        return (center_x, center_y)