from tools.type import Type
from os.path import exists, splitext
from import_export.error_messages import ErrorMessages
from PySide6.QtWidgets import QMessageBox

class GenerateOBJ():
    def __init__(self, file_name, objects):
        self.__obj_file = file_name
        self.__objects = objects

        # Verifica se nome do arquivo é válido
        self.__file_creation_success = self.__validateFileName()

    def __validateFileName(self):
        # Verifica se algum arquivo foi criado
        if self.__obj_file.replace(" ", "") == "":
            return False
        
        # Verifica se a extensão está correta
        base, extension = splitext(self.__obj_file)
        if extension != ".obj":
            erro = ErrorMessages.invalidExtension("", self.__obj_file, ".obj")
            erro.exec()
            return False
        
        # Arquivo .mtl tem o mesmo nome (porém com a extensão .mtl) e diretório que o .obj
        # Verifica se já existe um arquivo .mtl com esse nome, se sim pergunta se quer sobrescreve-lo
        self.__mtl_file = f'{base}.mtl'
        if exists(self.__mtl_file):
            erro = ErrorMessages.overwriteFile(self.__mtl_file)
            if erro.exec() == QMessageBox.Cancel:
                return False
        
        return True

    def generateFiles(self):
        self.__generateMTLFile()
        self.__generateOBJFile()
    
    # Cria o arquivo .obj
    def __generateOBJFile(self):
        objects = []
        points = []
        # Passa por todos os objetos do display file salvando suas informações
        # description = [nome, tipo, coordenadas]
        for obj in self.__objects:
            description = [obj.name]
            if obj.tipo == Type.POINT:
                description.append("p")
            elif obj.tipo == Type.WIREFRAME and obj.filled:
                description.append("f")
            elif (obj.tipo == Type.LINE) or (obj.tipo == Type.WIREFRAME and not obj.filled):
                description.append("l")

            # Salva os vertices de pontos, linhas e wireframes
            if len(description) == 2:
                obj_points = []
                for coord in obj.coord:
                    # Coordenada não está na lista de pontos
                    if coord not in points:
                        points.append(coord)
                        obj_points.append(len(points))
                    # Coordenada já está na lista de pontos
                    else:
                        obj_points.append(points.index(coord) + 1)

                description.append(obj_points)

                objects.append(description)
            
            # Salva os vertices de objetos 3d
            elif obj.tipo == Type.OBJECT_3D:
                for i in range(len(obj.coord)//2):
                    obj_points = []
                    for j in range(2):
                        coord = obj.coord[i*2+j]
                        # Coordenada não está na lista de pontos
                        if coord not in points:
                            points.append(coord)
                            obj_points.append(len(points))
                        # Coordenada já está na lista de pontos
                        else:
                            obj_points.append(points.index(coord) + 1)
                    description.append("l")
                    description.append(obj_points)
                objects.append(description)
                
        # Escreve no arquivo .obj
        with open(self.__obj_file, "w") as file:
            # Escreve os vertices
            for x, y, z in points:
                file.write(f"v {x} {y} {z}\n")

            # Escreve o nome do arquivo .mtl
            file.write("\n")
            mtl_name = self.__mtl_file.split("/")[-1]
            file.write(f"mtllib {mtl_name}\n\n")

            # Escreve as informações dos objetos
            for i, description in enumerate(objects):
                # Pontos, linhas e wireframes
                if len(description) == 3:
                    file.write(f"o {description[0]}\n")
                    file.write(f"usemtl {self.__objects_mtl_color[i]}\n")
                    coords = " ".join(map(str, description[2]))
                    file.write(f"{description[1]} {coords}\n")
                # Objeto 3d (é diferente pois tem que colocar cada aresta)
                else:
                    file.write(f"o {description[0]}\n")
                    file.write(f"usemtl {self.__objects_mtl_color[i]}\n")
                    for i in range(len(description[1:])//2):
                        coords = " ".join(map(str, description[i*2 + 2]))
                        file.write(f"{description[i*2 + 1]} {coords}\n")

    # Cria o arquivo .mtl
    def __generateMTLFile(self):
        colors = []
        self.__objects_mtl_color = []  # Contém o nome das cores de cada objeto para depois escrever no .obj

        with open(self.__mtl_file, "w") as file:
            for obj in self.__objects:
                if obj.tipo == Type.POINT or obj.tipo == Type.LINE or obj.tipo == Type.WIREFRAME or obj.tipo == Type.OBJECT_3D:
                    # Cor nova (não está na lista de colors)
                    if obj.color not in colors:
                        color_name = f"cor{len(colors)}"
                        file.write(f"newmtl {color_name}\n")

                        colors.append(obj.color)
                        r, g, b, _ = obj.color.getRgb()
                        file.write(f"Kd {r/255.0} {g/255.0} {b/255.0}\n")
                    # Cor já está na lista de colors
                    else:
                        color_name = f"cor{colors.index(obj.color)}"
                    self.__objects_mtl_color.append(color_name)
    
    @property
    def file_creation_success(self):
        return self.__file_creation_success