from popups.add_object import AddObject
from objects.bspline import BSpline

class AddObject3D(AddObject):
    def __init__(self, display_file, object_list, n_coords):
        self.__n_coord = n_coords * 2
        super().__init__(display_file, object_list)
        
    def setTitle(self):
        self.setWindowTitle("Adicionar Objeto 3D")
    
    def create(self):
        return BSpline(self.name_input.text(), self.getListCoord(), self.color)

    @property
    def n_coord(self):
        return self.__n_coord