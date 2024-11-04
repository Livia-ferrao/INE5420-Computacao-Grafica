from popups.add_object import AddObject
from objects.berzier_surface import BerzierSurface
from PySide6.QtWidgets import QLabel, QHBoxLayout, QDoubleSpinBox
from main_interface.configurations import Configurations

class AddBerzierSurface(AddObject):
    def __init__(self, display_file, object_list, n_matrixes):
        # n_coord passado com esse valor apenas para determinar posições do layout corretamente
        self.__n_coord = n_matrixes * 16 + n_matrixes
        self.n_matrixes = n_matrixes
        super().__init__(display_file, object_list)
        # atualizando n_coord com valor correto
        self.__n_coord = n_matrixes * 16 
    
    # Labels xi, yi e zi e input para pontos xi, yi e zi
    def drawXYZinputs(self):
        self.x_inputs = []
        self.y_inputs = []
        self.z_inputs = []
        for n in range(self.n_matrixes):
            label = QLabel(f"{n+1}ª matriz de pontos de controle")
            self.layout.addWidget(label, n*16+n+1, 0, 1, 2)
            for i in range(16):
                x_label = QLabel(f"x{i//4 + 1}{i%4 + 1}")
                self.x_inputs.append(QDoubleSpinBox())
                self.x_inputs[n*16+i].setRange(Configurations.min_coord(), Configurations.max_coord())
                self.x_inputs[n*16+i].setFixedWidth(90)
                y_label = QLabel(f"y{i//4 + 1}{i%4 + 1}")
                self.y_inputs.append(QDoubleSpinBox())
                self.y_inputs[n*16+i].setRange(Configurations.min_coord(), Configurations.max_coord())
                self.y_inputs[n*16+i].setFixedWidth(90)
                z_label = QLabel(f"z{i//4 + 1}{i%4 + 1}")
                self.z_inputs.append(QDoubleSpinBox())
                self.z_inputs[n*16+i].setRange(Configurations.min_coord(), Configurations.max_coord())
                self.z_inputs[n*16+i].setFixedWidth(90)

                point_layout = QHBoxLayout()
                point_layout.addWidget(x_label)
                point_layout.addWidget(self.x_inputs[n*16+i])
                point_layout.addWidget(y_label)
                point_layout.addWidget(self.y_inputs[n*16+i])
                point_layout.addWidget(z_label)
                point_layout.addWidget(self.z_inputs[n*16+i])
                self.layout.addLayout(point_layout, n*16+n+2+i, 0, 1, 2)
        
    def setTitle(self):
        self.setWindowTitle("Adicionar Superfície de Bérzier")
    
    def create(self):
        return BerzierSurface(self.name_input.text(), self.getListCoord(), self.color)

    @property
    def n_coord(self):
        return self.__n_coord