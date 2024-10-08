from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton, QScrollArea, QWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QDoubleSpinBox
from PySide6.QtGui import QColor
from main_interface.configurations import Configurations
from abc import abstractmethod
from popups.color_picker import ColorPicker

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
        self.__drawColorInput()
        self.__drawButtons()
        self.setTitle()

    # Labels xi e yi e input para pontos xi e yi
    def __drawXYinputs(self):
        self.__x_inputs = []
        self.__y_inputs = []
        for i in range(self.n_coord):
            x_label = QLabel(f"x{i+1}")
            self.__x_inputs.append(QDoubleSpinBox())
            self.__x_inputs[i].setRange(Configurations.min_coord(), Configurations.max_coord())
            y_label = QLabel(f"y{i+1}")
            self.__y_inputs.append(QDoubleSpinBox())
            self.__y_inputs[i].setRange(Configurations.min_coord(), Configurations.max_coord())

            self.__layout.addWidget(x_label, 1+2*i, 0)
            self.__layout.addWidget(self.__x_inputs[i], 1+2*i, 1)
            self.__layout.addWidget(y_label, 2+2*i, 0)
            self.__layout.addWidget(self.__y_inputs[i], 2+2*i, 1)
    
    # Botões ok e cancelar
    def __drawButtons(self):
        line = self.n_coord*2 + 2
        self.__ok_button = QPushButton("OK")
        self.__layout.addWidget(self.__ok_button, line, 1)
        self.__cancel_button = QPushButton("Cancelar")
        self.__layout.addWidget(self.__cancel_button, line, 0)

        self.__cancel_button.clicked.connect(self.reject)
        self.__ok_button.clicked.connect(self.ok)
        self.__ok_button.setFocus()
    
    # Seleção de cor
    def __drawColorInput(self):
        line = self.n_coord*2 + 1
        
        color_label = QLabel("Cor")
        self.__layout.addWidget(color_label, line, 0)

        line_layout = QHBoxLayout()
        # Retângulo da cor selecionada
        self.__color_display = QLabel()
        self.__color_display.setFixedSize(80, 20)
        line_layout.addWidget(self.__color_display)

        # Label do código da cor selecionada
        self.__color_code_label = QLabel()
        line_layout.addWidget(self.__color_code_label)
        
        # Cor inicial: preto
        self.__updateColor(QColor(0, 0, 0))

        # Botão para selecionar outra cor
        self.__select_color_button = QPushButton("Trocar cor")
        self.__select_color_button.clicked.connect(self.__drawColorPicker)
        line_layout.addWidget(self.__select_color_button)

        self.__layout.addLayout(line_layout, line, 1)
        
    # Desenha um QDialog (ColorPicker) para selecionar a cor
    def __drawColorPicker(self):
        self.__color_picker = ColorPicker(self.__color)
        if self.__color_picker.exec() == QDialog.DialogCode.Accepted:
            self.__updateColor(self.__color_picker.selected_color)
    
    # Atualiza a cor
    def __updateColor(self, color):
        self.__color = color
        self.__color_display.setStyleSheet(f"background-color: {self.__color.name()};")
        self.__color_code_label.setText(self.__color.name())

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
    
    @property
    def color(self):
        return self.__color