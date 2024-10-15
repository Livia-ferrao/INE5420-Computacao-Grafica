from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox, QCheckBox

class QtdPointsBSpline(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar B-Spline")

        # Labels e Inputs     
        self.__qtd_label_control = QLabel("Quantidade de pontos de controle:")
        self.__qtd_input_control = QSpinBox()
        self.__qtd_input_control.setRange(4, 100000000)  # maximo de pontos com valor grande para representar o infinito
        
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
        self.__layout.addWidget(self.__qtd_label_control, 0, 0)
        self.__layout.addWidget(self.__qtd_input_control, 0, 1)
        self.__layout.addWidget(self.__ok_button, 1, 1)
        self.__layout.addWidget(self.__cancel_button, 1, 0)
    
    def qtdPointsControl(self):
        return self.__qtd_input_control.value()