from PySide6.QtWidgets import QMessageBox

class ErrorMessages():
    @staticmethod
    def erro(text):
        message = QMessageBox()
        message.setWindowTitle("Erro")
        message.setText(text)
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setStandardButtons(QMessageBox.Ok)
        return message
    
    @staticmethod
    def warning(text):
        message = QMessageBox()
        message.setWindowTitle("Aviso")
        message.setText(text)
        message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        return message

    # Arquivo não tem a extensão correta
    @staticmethod
    def invalidExtension(extra, file, extension):
        text = f"O arquivo {extra}{file} não tem a extensão {extension}"
        return ErrorMessages.erro(text)
    
    # Arquilo de cores não informado
    @staticmethod
    def mtlNotInformed():
        text = f"O arquivo de cores (.mtl) não foi informado"
        return ErrorMessages.erro(text)
    
    # Arquivo não encontrado
    @staticmethod
    def fileNotFound(extra, file):
        text = f"O arquivo {extra}{file} não foi encontrado"
        return ErrorMessages.erro(text)
    
    # Arquivo de cores já existe -> será sobrescrito?
    @staticmethod
    def overwriteFile(file):
        text = f"O arquivo de cores {file} será sobrescrito"
        return ErrorMessages.warning(text)
