from add_object import AddObject
from wireframe import Wireframe

class AddWireframe(AddObject):
    def __init__(self, display_file, object_list, n_coord):
        self.__n_coord = n_coord
        super().__init__(display_file, object_list)

    def setTitle(self):
        self.setWindowTitle("Adicionar Polígono")
    
    def create(self):
        return Wireframe(self.name_input.text(), self.getListCoord())
    
    @property
    def n_coord(self):
        return self.__n_coord