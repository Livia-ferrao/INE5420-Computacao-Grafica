from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox
from PySide6.QtCore import Qt 

class QtdPointsObj3D(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Objeto 3D")

        # Labels e Inputs
        self.__info_label = QLabel("As arestas começam nos pontos de índice ímpar e terminam nos de índice par\n\nEscolha as arestas na forma: (x1, y1, z1) -> (x2, y2, z2)")
        self.__info_label.setAlignment(Qt.AlignCenter)
        self.__info_label.setWordWrap(True)
        
        
        self.__qtd_label = QLabel("Quantidade de arestas do objeto:")
        self.__qtd_input = QSpinBox()
        self.__qtd_input.setRange(1, 1000000)
        
        # Estilo
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setFixedSize(400, 180)

        # Botões
        self.__ok_button = QPushButton("Ok")
        self.__cancel_button = QPushButton("Cancelar")
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)

        # Layout
        self.__layout = QGridLayout(self)
        self.__layout.addWidget(self.__info_label, 0, 0, 1, 2)
        self.__layout.addWidget(self.__qtd_label, 1, 0)
        self.__layout.addWidget(self.__qtd_input, 1, 1)
        self.__layout.addWidget(self.__ok_button, 2, 1)
        self.__layout.addWidget(self.__cancel_button, 2, 0)

    def qtdPoints(self):
        return self.__qtd_input.value()
