from objects.point import Point
from objects.line import Line
from objects.wireframe import Wireframe
from objects.object3D import Object3D
from PySide6.QtGui import QColor
from os.path import exists, dirname, splitext
from import_export.error_messages import ErrorMessages
from tools.type import Type

class ReaderOBJ():
    def __init__(self, file_name):  
        self.__obj_file = file_name

        # Verifica se arquivos realmente existem    
        self.__files_exist = self.__filesExist()

        self.__objects = [] # Objetos criados
        self.__colors = {}  # Cores
        self.__points = []  # Vertices
        self.__objs_description = []  # Descrições dos objetos lidos

    def __filesExist(self):
        # Verifica se algum arquivo foi selecionado
        if self.__obj_file.replace(" ", "") == "":
            return False

        # Verifica se a extensão do arquivo é .obj
        _, extension = splitext(self.__obj_file)
        if extension != ".obj":
            erro = ErrorMessages.invalidExtension("", self.__obj_file, ".obj")
            erro.exec()
            return False
        
        # Verifica se o arquivo .obj existe
        if not exists(self.__obj_file):
            erro = ErrorMessages.fileNotFound("", self.__obj_file)
            erro.exec()
            return False
        
        name_mtl = ""  
        # Procura o nome do arquivo de cores (MTL)
        with open(self.__obj_file, "r") as file:
            for line in file:
                words = line.split(" ")
                if words[0] == "mtllib":
                    name_mtl = words[1].strip()

        # Arquivo de cores não informado
        if name_mtl == "":
            erro = ErrorMessages.mtlNotInformed()
            erro.exec()
            return False
        
        # Verifica se a extensão do arquivo é .mtl
        _, extension2 = splitext(name_mtl)
        if extension2 != ".mtl":
            erro = ErrorMessages.invalidExtension("de cores informado ", name_mtl, ".mtl")
            erro.exec()
            return False
        
        # Verifica se o arquivo de cores existe
        self.__mtl_file = f'{dirname(self.__obj_file)}/{name_mtl}'
        if not exists(self.__mtl_file):
            erro = ErrorMessages.fileNotFound("de cores informado ", self.__mtl_file)
            erro.exec_()
            return False

        return True

    # Cria os objetos
    def createObjects(self, existing_names):
        self.__readMTLFile()
        self.__readOBJFile()
        
        for description in self.__objs_description:
            i = 1
            # Para nao existir objetos com o mesmo nome
            if description[1] in existing_names:
                description[1] += "_1"
            while description[1] in existing_names:
                i += 1
                description[1] = description[1][:-1] + f"{i}"
            existing_names.append(description[1])

            if description[0] == Type.POINT:
                obj = Point(description[1], description[2], description[3])
            elif description[0] == Type.LINE:
                obj = Line(description[1], description[2], description[3])
            elif description[0] == Type.WIREFRAME:
                obj = Wireframe(description[1], description[2], description[3], description[4])
            elif description[0] == Type.OBJECT_3D:
                obj = Object3D(description[1], description[2], description[3])

            self.__objects.append(obj)
        
    # Le arquivo de cores .mtl
    def __readMTLFile(self):
        # Salva as cores em self.__colors
        name = ""
        with open(self.__mtl_file, "r") as file:
            for line in file:
                words = line.split(" ")
                words = [w.strip() for w in words]
                if words[0] == "newmtl":
                    name = words[1]
                if words[0] == "Kd":
                    self.__colors[name] = self.__convertToQcolor(float(words[1]), float(words[2]), float(words[3]))

    # Converte rgb normalizada para QColor
    def __convertToQcolor(self, r, g, b):
        r_int = int(round(r * 255))
        g_int = int(round(g * 255))
        b_int = int(round(b * 255))
        return QColor(r_int, g_int, b_int)
    
    # Le o arquivo dos objetos .obj
    def __readOBJFile(self):
        # Salva os vertices em self.__points
        # Salva as descricoes dos objetos em self.__objs_description
        # descricao = [tipo, nome, coordenadas, cor, filled (para polígonos)]
        with open(self.__obj_file, "r") as file:
            lines = file.readlines()
            i = 0
            while True:
                word = lines[i].split(" ")
                word = [w.strip() for w in word]
                if word[0] == "usemtl":
                    colorObj = self.__colors[word[1]]

                elif word[0] == "v":
                    self.__points.append([float(word[1]), float(word[2]), float(word[3])])
                    
                elif word[0] == "o":
                    nameObj = " ".join(word[1:])
                    
                elif word[0] == "p":
                    typeObj = Type.POINT
                    self.__objs_description.append([typeObj, nameObj, self.__getPoints([int(word[1])]), colorObj])
                
                elif word[0] == "l":
                    typeObj = Type.LINE if len(word) == 3 else Type.WIREFRAME
                    points = [int(x) for x in word[1:]]

                    linhas_restantes = lines[i+1:]
                    for next in linhas_restantes:
                        word = next.split(" ")
                        word = [w.strip() for w in word]
                        if word[0] == "l":
                            typeObj = Type.OBJECT_3D
                            points.extend(int(x) for x in word[1:])
                        elif word[0] == "o" or word[0] == "v":
                            break
                        i += 1
                    
                    if typeObj == Type.WIREFRAME:
                        self.__objs_description.append([typeObj, nameObj, self.__getPoints(points), colorObj, False])
                    else:
                        self.__objs_description.append([typeObj, nameObj, self.__getPoints(points), colorObj])
                        
                elif word[0] == "f":
                    typeObj = Type.WIREFRAME
                    points = [int(x) for x in word[1:]]
                    self.__objs_description.append([typeObj, nameObj, self.__getPoints(points), colorObj, True])

                i += 1
                if i >= len(lines):
                    break
    
    # Retorna as coordenadas dos vértices 
    def __getPoints(self, indexes):
        coords = []
        for i in indexes:
            coords.append((self.__points[i - 1][0], self.__points[i - 1][1], self.__points[i - 1][2]))
        return coords
    
    @property
    def files_exist(self):
        return self.__files_exist
    
    @property
    def objects(self):
        return self.__objects