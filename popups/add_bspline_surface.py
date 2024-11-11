from popups.add_object import AddObject
from objects.bspline_surface import BSplineSurface
from PySide6.QtWidgets import QLabel, QHBoxLayout, QDoubleSpinBox
from main_interface.configurations import Configurations

class AddBSplineSurface(AddObject):
    def __init__(self, display_file, object_list, lines, columns):
        self.__n_coord = lines * columns
        self.n_lines = lines
        self.n_columns = columns
        super().__init__(display_file, object_list)
    
    # Labels xi, yi e zi e input para pontos xi, yi e zi
    def drawXYZinputs(self):
        self.x_inputs = []
        self.y_inputs = []
        self.z_inputs = []
        for i in range(self.n_lines):
            for j in range(self.n_columns):
                x_label = QLabel(f"x{i+1},{j+1}")
                self.x_inputs.append(QDoubleSpinBox())
                self.x_inputs[i*self.n_columns + j].setRange(Configurations.min_coord(), Configurations.max_coord())
                self.x_inputs[i*self.n_columns + j].setFixedWidth(75)
                y_label = QLabel(f"y{i+1},{j+1}")
                self.y_inputs.append(QDoubleSpinBox())
                self.y_inputs[i*self.n_columns + j].setRange(Configurations.min_coord(), Configurations.max_coord())
                self.y_inputs[i*self.n_columns + j].setFixedWidth(75)
                z_label = QLabel(f"z{i+1},{j+1}")
                self.z_inputs.append(QDoubleSpinBox())
                self.z_inputs[i*self.n_columns + j].setRange(Configurations.min_coord(), Configurations.max_coord())
                self.z_inputs[i*self.n_columns + j].setFixedWidth(75)

                point_layout = QHBoxLayout()
                point_layout.addWidget(x_label)
                point_layout.addWidget(self.x_inputs[i*self.n_columns + j])
                point_layout.addWidget(y_label)
                point_layout.addWidget(self.y_inputs[i*self.n_columns + j])
                point_layout.addWidget(z_label)
                point_layout.addWidget(self.z_inputs[i*self.n_columns + j])
                self.layout.addLayout(point_layout, i*self.n_columns + j + 1, 0, 1, 2)
        
    def setTitle(self):
        self.setWindowTitle("Adicionar Superfície B-Spline")
    
    def create(self):
        return BSplineSurface(self.name_input.text(), self.getListCoord(), self.color, self.n_lines, self.n_columns)

    @property
    def n_coord(self):
        return self.__n_coord