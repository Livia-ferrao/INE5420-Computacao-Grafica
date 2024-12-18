from popups.add_object import AddObject
from objects.point import Point

class AddPoint(AddObject):
    def __init__(self, display_file, object_list):
        self.__n_coord = 1
        super().__init__(display_file, object_list)
        self.setFixedSize(430, 180)

    def setTitle(self):
        self.setWindowTitle("Adicionar Ponto")
    
    def create(self):
        return Point(self.name_input.text(), self.getListCoord(), self.color)
    
    @property
    def n_coord(self):
        return self.__n_coord