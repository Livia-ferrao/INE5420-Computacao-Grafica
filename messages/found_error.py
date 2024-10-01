from PySide6.QtWidgets import QMessageBox

class FileFound(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atenção!")
        self.setText(f"O arquivo cores.mtl será sobrescrito")
        self.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        button_ok = self.button(QMessageBox.Ok)
        button_ok.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        button_cancel = self.button(QMessageBox.Cancel)
        button_cancel.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        self.setIcon(QMessageBox.Information)
