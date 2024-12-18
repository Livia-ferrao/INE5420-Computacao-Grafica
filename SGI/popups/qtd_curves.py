from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox, QCheckBox

class QtdCurves(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar curva de Bérzier")

        # Labels e Inputs
        self.__curves_label = QLabel("Quantidade de curvas:")
        self.__curves_input = QSpinBox()
        self.__curves_input.setRange(1, 100000000)  # maximo de curvas com valor grande para representar o infinito
        
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
        self.__layout.addWidget(self.__curves_label, 0, 0)
        self.__layout.addWidget(self.__curves_input, 0, 1)
        self.__layout.addWidget(self.__ok_button, 1, 1)
        self.__layout.addWidget(self.__cancel_button, 1, 0)

    def qtdCurves(self):
        return self.__curves_input.value()
