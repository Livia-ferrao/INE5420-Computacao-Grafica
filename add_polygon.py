from add_object import AddObject
from wireframe import Wireframe

class AddPolygon(AddObject):
    def __init__(self, n_coord):
        self.n_coord = n_coord
        super().__init__()

    def setTitle(self):
        self.setWindowTitle("Adicionar Polígono")
    
    def create(self):
        return Wireframe(self.name_input.text(), self.get_list_coord())