from abc import ABC, abstractmethod

class Object(ABC):
    def __init__(self, name, tipo, coord):
        self.name = name
        self.tipo = tipo
        self.coord = coord
    
    @abstractmethod
    def draw(self, painter):
        pass