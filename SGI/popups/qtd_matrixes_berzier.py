from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox
from PySide6.QtCore import Qt

class QtdMatrixesBerzier(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Superfície de Bérzier")

        # Labels e Inputs     
        self.__qtd_label_matrixes = QLabel("Quantidade de matrizes de pontos de controle:")
        self.__qtd_label_matrixes.setAlignment(Qt.AlignCenter)
        self.__qtd_label_matrixes.setWordWrap(True)
        self.__qtd_input_matrixes = QSpinBox()
        self.__qtd_input_matrixes.setRange(1, 100000000)  # maximo de matrizes com valor grande para representar o infinito
        
        # Estilo
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setFixedSize(400, 120)

        # Botões
        self.__ok_button = QPushButton("Ok")
        self.__cancel_button = QPushButton("Cancelar")
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)

        # Layout
        self.__layout = QGridLayout(self)
        self.__layout.addWidget(self.__qtd_label_matrixes, 0, 0)
        self.__layout.addWidget(self.__qtd_input_matrixes, 0, 1)
        self.__layout.addWidget(self.__ok_button, 1, 1)
        self.__layout.addWidget(self.__cancel_button, 1, 0)
    
    def qtdMatrixes(self):
        return self.__qtd_input_matrixes.value()