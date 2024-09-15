from add_object import AddObject
from line import Line

class AddLine(AddObject):
    def __init__(self, display_file, object_list):
        self.__n_coord = 2
        super().__init__(display_file, object_list)

    def setTitle(self):
        self.setWindowTitle("Adicionar Reta")
    
    def create(self):
        return Line(self.name_input.text(), self.getListCoord(), self.color)

    @property
    def n_coord(self):
        return self.__n_coord