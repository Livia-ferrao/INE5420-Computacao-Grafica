from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox
from PySide6.QtCore import Qt

class MatrixDimensionBSpline(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Superfície B-Spline")

        # Labels e Inputs     
        self.__lines_label = QLabel("Quantidade de linhas da matriz de pontos de controle:")
        self.__columns_label = QLabel("Quantidade de colunas da matriz de pontos de controle:")
        self.__lines_input = QSpinBox()
        self.__lines_input.setRange(4, 20)
        self.__columns_input = QSpinBox()
        self.__columns_input.setRange(4, 20)
        
        # Estilo
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setFixedSize(500, 120)

        # Botões
        self.__ok_button = QPushButton("Ok")
        self.__cancel_button = QPushButton("Cancelar")
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)

        # Layout
        self.__layout = QGridLayout(self)
        self.__layout.addWidget(self.__lines_label, 0, 0)
        self.__layout.addWidget(self.__lines_input, 0, 1)
        self.__layout.addWidget(self.__columns_label, 1, 0)
        self.__layout.addWidget(self.__columns_input, 1, 1)
        self.__layout.addWidget(self.__ok_button, 2, 1)
        self.__layout.addWidget(self.__cancel_button, 2, 0)
    
    def qtdLines(self):
        return self.__lines_input.value()
    
    def qtdColumns(self):
        return self.__columns_input.value()