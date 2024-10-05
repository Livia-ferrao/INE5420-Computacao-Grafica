from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox, QCheckBox

class QtdCurves(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar curva de Bérzier")

        # Labels e Inputs
        self.__curves_label = QLabel("Quantidade de curvas:")
        self.__curves_input = QSpinBox()
        self.__curves_input.setRange(1, 1000000)

        self.__points_label = QLabel("Quantidade de pontos para continuidade:")
        self.__points_input = QSpinBox()
        self.__points_input.setRange(4, 1000000)
        self.__points_input.setValue(10)
        
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
        self.__layout.addWidget(self.__points_label, 1, 0)
        self.__layout.addWidget(self.__points_input, 1, 1)
        self.__layout.addWidget(self.__ok_button, 2, 1)
        self.__layout.addWidget(self.__cancel_button, 2, 0)

    def qtdPoints(self):
        return self.__points_input.value()

    def qtdCurves(self):
        return self.__curves_input.value()
