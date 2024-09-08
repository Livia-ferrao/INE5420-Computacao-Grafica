from abc import ABC, abstractmethod
import numpy as np

class Object(ABC):
    def __init__(self, name, tipo, coord):
        self.name = name
        self.tipo = tipo
        self.coord = coord

    @abstractmethod
    def draw(self, transformed_coord, painter):
        pass