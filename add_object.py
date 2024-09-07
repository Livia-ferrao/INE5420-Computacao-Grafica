from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton, QSpinBox
from configurations import Configurations
from abc import abstractmethod

class AddObject(QDialog):
    def __init__(self):
        super().__init__()

        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.name_input, 0, 1)

        self.draw_x_y_inputs()
        self.draw_buttons()
        self.setTitle()

    def draw_x_y_inputs(self):
        self.x_inputs = []
        self.y_inputs = []
        for i in range(self.n_coord):
            x_label = QLabel(f"x{i+1}")
            self.x_inputs.append(QSpinBox())
            self.x_inputs[i].setRange(Configurations.min_coord(), Configurations.max_coord())
            y_label = QLabel(f"y{i+1}")
            self.y_inputs.append(QSpinBox())
            self.y_inputs[i].setRange(Configurations.min_coord(), Configurations.max_coord())

            self.layout.addWidget(x_label, 1+2*i, 0)
            self.layout.addWidget(self.x_inputs[i], 1+2*i, 1)
            self.layout.addWidget(y_label, 2+2*i, 0)
            self.layout.addWidget(self.y_inputs[i], 2+2*i, 1)
    
    def draw_buttons(self):
        line = self.n_coord*2 + 1
        self.cancel_button = QPushButton("Cancelar")
        self.layout.addWidget(self.cancel_button, line, 0)
        self.ok_button = QPushButton("OK")
        self.layout.addWidget(self.ok_button, line, 1)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
    
    def get_list_coord(self):
        list_coord = []
        for i in range(self.n_coord):
            list_coord.append((self.x_inputs[i].value(), self.y_inputs[i].value()))
    
    @abstractmethod
    def setTitle(self):
        pass

    @abstractmethod
    def create(self):
        pass