from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6 import QtWidgets, QtGui

class OperationsMessage(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Operações")
        self.setText("Escolha a operação a ser realizada")
        self.setStyleSheet("background-color: rgb(165,165,165); color: black;")

        # Criando os botoes
        self.setStandardButtons(
            QtWidgets.QMessageBox.Open
            | QtWidgets.QMessageBox.Cancel
        )

        # Renomeando o botao de deletar objeto
        delete_button = self.button(QtWidgets.QMessageBox.Open)
        delete_button.setText("Deletar Objeto")
        delete_button.setFixedSize(150, 30)
        delete_button.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        
        delete_button.setIcon(QtGui.QIcon())

        # Renomeando o botao de cancelar
        cancel_button = self.button(QtWidgets.QMessageBox.Cancel)
        cancel_button.setText("Cancelar")
        cancel_button.setFixedSize(150, 30)
        cancel_button.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        cancel_button.setIcon(QtGui.QIcon())

        self.setDefaultButton(QtWidgets.QMessageBox.Cancel)
