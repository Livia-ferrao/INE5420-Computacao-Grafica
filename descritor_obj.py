from os.path import exists, splitext
from PySide6.QtWidgets import QMessageBox
from messages.not_found_error import FileNotFound

class DescritorOBJ:
    def __init__(self):
        pass

    def verify_valid_read_file(self, name_file):
        # Verifica se algum arquivo foi selecionado
        if name_file.replace(" ", "") == "":
            return True
        
        # Verifica se o arquivo de cores (MTL) existe
        with open(name_file, "r") as file:
            line = file.readline()
            while line:
                words = line.split(" ")
                if words[0] == "mtllib":
                    name_mtl = words[1].strip()
                line = file.readline()

        name_mtl = "wavefront/" + name_mtl
        if not exists(name_mtl):
            not_found = FileNotFound(name_mtl)
            i = not_found.exec_()
            return True

        return False