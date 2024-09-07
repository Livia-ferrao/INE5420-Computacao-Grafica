from add_object import AddObject
from point import Point

class AddPoint(AddObject):
    def __init__(self):
        self.n_coord = 1
        super().__init__()

    def setTitle(self):
        self.setWindowTitle("Adicionar Ponto")
    
    def create(self):
        return Point(self.name_input.text(), self.get_list_coord())
    