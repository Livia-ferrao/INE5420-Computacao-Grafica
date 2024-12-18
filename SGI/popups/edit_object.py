from popups.add_object import AddObject
from tools.type import Type
from popups.add_berzier_surface import AddBerzierSurface
from popups.add_bspline_surface import AddBSplineSurface

class EditObject(AddObject):
    def __init__(self, existing_object, display_file, object_list):
        self.__n_coord = len(existing_object.coord)
        self.__existing_object = existing_object
        super().__init__(display_file, object_list)
        if existing_object.tipo == Type.POINT:
            self.setFixedSize(430, 180)
        elif existing_object.tipo == Type.LINE:
            self.setFixedSize(430, 240)
        elif existing_object.tipo == Type.BERZIER_SURFACE:
            self.__n_coord = len(existing_object.coord)
        self.__populateFields()

    # Coloca o nome e coordenadas do objeto como valores iniciais da tela de edição
    def __populateFields(self):
        self.name_input.setText(self.__existing_object.name)
        for i, (x, y, z) in enumerate(self.__existing_object.coord):
            self.x_inputs[i].setValue(x)
            self.y_inputs[i].setValue(y)
            self.z_inputs[i].setValue(z)
        self._AddObject__updateColor(self.__existing_object.color)

    def setTitle(self):
        self.setWindowTitle(f"Editar objeto")

    def ok(self):
        # Verifica se nome é repetido ou vazio
        name = self.name_input.text().strip()
        existing_names = self.display_file.getNames()
        existing_names.remove(self.__existing_object.name)
        if len(name) == 0:
            self.noName()
        elif name in existing_names:
            self.repeatedName()
        else:
            self.__existing_object.name = self.name_input.text()
            self.__existing_object.coord = self.getListCoord()
            self.__existing_object.color = self.color
            super().accept()
    
    @property
    def existing_object(self):
        return self.__existing_object
    
    @property
    def n_coord(self):
        return self.__n_coord
    
    def drawXYZinputs(self):
        if self.__existing_object.tipo == Type.BERZIER_SURFACE:
            self.n_matrixes = int(self.__n_coord/16)
            self.__n_coord = self.__n_coord + self.n_matrixes
            AddBerzierSurface.drawXYZinputs(self)
        elif self.__existing_object.tipo == Type.BSPLINE_SURFACE:
            self.n_lines = self.__existing_object.n_lines
            self.n_columns = self.__existing_object.n_columns
            AddBSplineSurface.drawXYZinputs(self)
        else:
            super().drawXYZinputs()