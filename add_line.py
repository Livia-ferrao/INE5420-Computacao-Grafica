from add_object import AddObject
from line import Line

class AddLine(AddObject):
    def __init__(self, list_names):
        self.n_coord = 2
        super().__init__(list_names)

    def setTitle(self):
        self.setWindowTitle("Adicionar Reta")
    
    def create(self):
        return Line(self.name_input.text(), self.get_list_coord())