from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox, QCheckBox

class QtdPoints(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Polígono")

        self.__qtd_label = QLabel("Quantidade de pontos do polígono")
        self.__qtd_input = QSpinBox()
        self.__qtd_input.setRange(3, 1000000)
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setFixedSize(400, 100)

        # Botões 
        self.__ok_button = QPushButton("Ok")
        self.__cancel_button = QPushButton("Cancelar")
        self.__ok_button.clicked.connect(self.accept)
        self.__cancel_button.clicked.connect(self.reject)

        # Layout
        self.__layout = QGridLayout(self)
        self.__layout.addWidget(self.__qtd_label, 0, 0)
        self.__layout.addWidget(self.__qtd_input, 0, 1)
        self.__layout.addWidget(self.__ok_button, 1, 1)
        self.__layout.addWidget(self.__cancel_button, 1, 0)
    
    def qtdPoints(self):
        return self.__qtd_input.value()

