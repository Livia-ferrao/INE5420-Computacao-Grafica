from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton, QSpinBox, QScrollArea, QWidget, QVBoxLayout, QMessageBox
from configurations import Configurations
from abc import abstractmethod

class AddObject(QDialog):
    def __init__(self, display_file, object_list):
        super().__init__()
        self.__display_file = display_file
        self.__object_list = object_list

        self.setFixedSize(400, 200)
        # Definindo área de scrool e layout
        self.__main_layout = QVBoxLayout(self)
        self.__scroll_area = QScrollArea()
        self.__scroll_area.setWidgetResizable(True)
        self.__scroll_content = QWidget()
        self.__scroll_area.setWidget(self.__scroll_content)
        self.__layout = QGridLayout(self.__scroll_content)
        self.__scroll_content.setLayout(self.__layout)
        self.__main_layout.addWidget(self.__scroll_area)

        # Label "Nome" e input para nome
        self.__name_label = QLabel("Nome:")
        self.__name_input = QLineEdit()
        self.__layout.addWidget(self.__name_label, 0, 0)
        self.__layout.addWidget(self.__name_input, 0, 1)

        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")

        self.__drawXYinputs()
        self.__drawButtons()
        self.setTitle()

    # Labels xi e yi e input para pontos xi e yi
    def __drawXYinputs(self):
        self.__x_inputs = []
        self.__y_inputs = []
        for i in range(self.n_coord):
            x_label = QLabel(f"x{i+1}")
            self.__x_inputs.append(QSpinBox())
            self.__x_inputs[i].setRange(Configurations.min_coord(), Configurations.max_coord())
            y_label = QLabel(f"y{i+1}")
            self.__y_inputs.append(QSpinBox())
            self.__y_inputs[i].setRange(Configurations.min_coord(), Configurations.max_coord())

            self.__layout.addWidget(x_label, 1+2*i, 0)
            self.__layout.addWidget(self.__x_inputs[i], 1+2*i, 1)
            self.__layout.addWidget(y_label, 2+2*i, 0)
            self.__layout.addWidget(self.__y_inputs[i], 2+2*i, 1)
    
    # Botôes ok e cancelar
    def __drawButtons(self):
        line = self.n_coord*2 + 1
        self.__ok_button = QPushButton("OK")
        self.__layout.addWidget(self.__ok_button, line, 1)
        self.__cancel_button = QPushButton("Cancelar")
        self.__layout.addWidget(self.__cancel_button, line, 0)

        self.__cancel_button.clicked.connect(self.reject)
        self.__ok_button.clicked.connect(self.ok)
    
    # Retorna lista das coordenadas inseridas
    def getListCoord(self):
        list_coord = []
        for i in range(self.n_coord):
            list_coord.append((self.__x_inputs[i].value(), self.__y_inputs[i].value()))
        return list_coord

    def ok(self):
        # Verifica se nome é repetido ou vazio
        name = self.__name_input.text().strip()
        if len(name) == 0:
            self.noName()
        elif name in self.__display_file.getNames():
            self.repeatedName()
        else:
            obj = self.create()
            self.__display_file.addObject(obj)
            self.__object_list.addItem(str(obj.name))
            super().accept() 

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def setTitle(self):
        pass

    # Aviso sem nome
    def noName(self):
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Dê um nome ao objeto")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()
    
    # Aviso nome repetido
    def repeatedName(self):
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText("Esse nome já existe")
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setFixedSize(400, 200)
        message.exec()
    
    @property
    def display_file(self):
        return self.__display_file
    
    @property
    def name_input(self):
        return self.__name_input
    
    @property
    def x_inputs(self):
        return self.__x_inputs
    
    @property
    def y_inputs(self):
        return self.__y_inputs