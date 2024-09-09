from PySide6.QtWidgets import QDialog, QLabel, QGridLayout, QPushButton, QSpinBox, QCheckBox

class QtdPoints(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Criar Polígono")

        self.qtd_label = QLabel("Quantidade de pontos do polígono")
        self.qtd_input = QSpinBox()
        self.qtd_input.setRange(3, 1000000)
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setFixedSize(400, 200)

        self.preencher = QCheckBox("Preencher polígono")
        self.ok_button = QPushButton("Ok")
        self.cancel_button = QPushButton("Cancelar")
        self.layout = QGridLayout(self)

        self.layout.addWidget(self.qtd_label, 0, 0)
        self.layout.addWidget(self.qtd_input, 0, 1)
        self.layout.addWidget(self.preencher, 1, 0, 1, 2)
        self.layout.addWidget(self.ok_button, 2, 1)
        self.layout.addWidget(self.cancel_button, 2, 0)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
