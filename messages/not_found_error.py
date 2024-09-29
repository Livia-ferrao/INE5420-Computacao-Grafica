from PySide6.QtWidgets import QMessageBox

class FileNotFound(QMessageBox):
    def __init__(self, nome_arquivo: str):
        super().__init__()
        self.setWindowTitle("Aviso!")
        self.setText(f"O arquivo {nome_arquivo} não foi encontrado")
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setStandardButtons(QMessageBox.Ok)
        botao_ok = self.button(QMessageBox.Ok)
        botao_ok.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setIcon(QMessageBox.Warning)
