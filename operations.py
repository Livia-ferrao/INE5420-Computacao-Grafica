from PySide6.QtWidgets import QDialog
from PySide6 import QtWidgets

class Operations(QDialog):
    def __init__(self, name):
        super().__init__()

        self.setFixedSize(400, 100)
        self.setWindowTitle("Operações")
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")

        self.__label = QtWidgets.QLabel(f"Escolha uma operação para fazer com o objeto \"{name}\"")

        # Botões
        self.__edit_button = QtWidgets.QPushButton("Editar")
        self.__delete_button = QtWidgets.QPushButton("Deletar")
        self.__transformations_button = QtWidgets.QPushButton("Transformações")
        self.__cancel_button = QtWidgets.QPushButton("Cancelar")
        
        self.__cancel_button.clicked.connect(self.reject)
        self.__delete_button.clicked.connect(lambda: self.accept("delete"))
        self.__edit_button.clicked.connect(lambda: self.accept("edit"))
        self.__transformations_button.clicked.connect(lambda: self.accept("transformations"))

        # Layout
        self.__layout = QtWidgets.QGridLayout(self)
        self.__layout.addWidget(self.__label, 0, 0, 1, 4)
        self.__layout.addWidget(self.__cancel_button, 1, 0)
        self.__layout.addWidget(self.__delete_button, 1, 1)
        self.__layout.addWidget(self.__edit_button, 1, 2)
        self.__layout.addWidget(self.__transformations_button, 1, 3)

    def accept(self, button_name):
        self.__clicked_button = button_name
        super().accept()
    
    @property
    def clicked_button(self):
        return self.__clicked_button
