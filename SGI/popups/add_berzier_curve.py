from popups.add_object import AddObject
from objects.berzier_curve import BerzierCurve

class AddBerzierCurve(AddObject):
    def __init__(self, display_file, object_list, n_curves):
        self.__n_coord = n_curves*4 - (n_curves-1)
        super().__init__(display_file, object_list)
        
    def setTitle(self):
        self.setWindowTitle("Adicionar Curva de Bérzier")
    
    def create(self):
        return BerzierCurve(self.name_input.text(), self.getListCoord(), self.color)

    @property
    def n_coord(self):
        return self.__n_coord