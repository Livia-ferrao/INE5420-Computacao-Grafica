from popups.add_object import AddObject
from objects.bspline import BSpline

class AddBSpline(AddObject):
    def __init__(self, display_file, object_list, n_coords, n_precision):
        self.__n_coord = n_coords
        self.__n_precision = n_precision
        super().__init__(display_file, object_list)
        
    def setTitle(self):
        self.setWindowTitle("Adicionar B-spline")
    
    def create(self):
        return BSpline(self.name_input.text(), self.getListCoord(), self.color, self.__n_precision)

    @property
    def n_coord(self):
        return self.__n_coord