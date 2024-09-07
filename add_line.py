from add_object import AddObject
from line import Line

class AddLine(AddObject):
    def __init__(self):
        self.n_coord = 2
        super().__init__()

    def setTitle(self):
        self.setWindowTitle("Adicionar Linha")
    
    def create(self):
        return Line(self.name_input.text(), self.get_list_coord())