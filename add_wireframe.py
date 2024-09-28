from add_object import AddObject
from wireframe import Wireframe
from PySide6.QtWidgets import QCheckBox

class AddWireframe(AddObject):
    def __init__(self, display_file, object_list, n_coord, filled=False):
        self.__n_coord = n_coord
        self.__filled = filled
        super().__init__(display_file, object_list)
        
    def setTitle(self):
        self.setWindowTitle("Adicionar Polígono")
    
    def create(self):
        return Wireframe(self.name_input.text(), self.getListCoord(), self.color, self.__filled)
    
    @property
    def n_coord(self):
        return self.__n_coord