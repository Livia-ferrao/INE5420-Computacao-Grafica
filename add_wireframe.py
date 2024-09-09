from add_object import AddObject
from wireframe import Wireframe

class AddWireframe(AddObject):
    def __init__(self, list_names, n_coord, filled):
        self.n_coord = n_coord
        self.fill = filled
        super().__init__(list_names)

    def setTitle(self):
        self.setWindowTitle("Adicionar Polígono")
    
    def create(self):
        return Wireframe(self.name_input.text(), self.get_list_coord(), self.fill)