from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton, QSpinBox, QScrollArea, QWidget, QVBoxLayout, QMessageBox
from configurations import Configurations
from abc import abstractmethod

class AddObject(QDialog):
    def __init__(self, list_names):
        super().__init__()
        self.names = list_names
        self.main_layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.layout = QGridLayout(self.scroll_content)
        self.scroll_content.setLayout(self.layout)
        self.setFixedSize(400, 200)
        self.main_layout.addWidget(self.scroll_area)
        self.name_label = QLabel("Nome:")
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_label, 0, 0)
        self.layout.addWidget(self.name_input, 0, 1)
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")

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
        return list_coord
    
    @abstractmethod
    def setTitle(self):
        pass

    def accept(self):
        name = self.name_input.text().strip()
        if len(name) == 0:
            self.no_name()
        elif name in self.names:
            self.repeated_name()
        else:
            super().accept() 

    @abstractmethod
    def create(self):
        pass

    def no_name(self):
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Dê um nome ao objeto")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()
    
    def repeated_name(self):
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Esse nome já existe")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()
    