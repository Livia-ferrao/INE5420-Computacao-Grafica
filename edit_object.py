from add_object import AddObject

class EditObject(AddObject):
    def __init__(self, existing_object, display_file, object_list):
        self.__n_coord = len(existing_object.coord)
        self.__existing_object = existing_object
        super().__init__(display_file, object_list)
        self.__populateFields()

    # Coloca o nome e coordenadas do objeto como valores iniciais da tela de edição
    def __populateFields(self):
        self.name_input.setText(self.__existing_object.name)
        for i, (x, y) in enumerate(self.__existing_object.coord):
            self.x_inputs[i].setValue(x)
            self.y_inputs[i].setValue(y)
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