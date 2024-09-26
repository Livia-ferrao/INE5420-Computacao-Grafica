from descritor_obj import DescritorOBJ
from point import Point
from line import Line
from wireframe import Wireframe
from PySide6.QtGui import QColor

class ReaderOBJ(DescritorOBJ):
    def __init__(self, nome_arquivo, display_file):
        self.objects = []
        pass

    def openFile(self, name_file, display_file):
        self.valid_name_file(name_file)
        edges, graphics_elements = self.readFileObj(name_file)

        for key, val in graphics_elements.items():
            
            # Precisa verificar se tem nome repetido?
            # i = 2
            # name = key.strip()
            # print(name)
            # while name in display_file.getNames():
            #     if i > 2:
            #         novo_nome = list(name)
            #         novo_nome[-1] = str(i)
            #         name = "".join(novo_nome)
            #     else:
            #         name = name + "_" + str(i)
            #     i += 1
                
            print(name)
            if val[0] == "Ponto":
                element = Point(name, self.obter_vertices(val[2], edges), val[1])

            elif val[0] == "Reta":
                element = Line(name, self.obter_vertices(val[2], edges), val[1])

            # else:
            #     element = Wireframe(name, val[1], self.obter_vertices(val[2], edges), val[3])

            self.objects.append(element)
        
        print('OBJECTS: ', self.objects)
        #  return objects

    def obter_vertices(self, indices, vertices):
        v = []
        for indice in indices:
            v.append(
                (
                    vertices[indice - 1][0],
                    vertices[indice - 1][1],
                )
            )
        return v

    def lerArquivoMTL(self, nome_arquivo: str) -> dict:
        cores = {}
        nome = ""
        rgb = ()

        with open(nome_arquivo, "r") as arquivo:
            for linha in arquivo:
                palavras = linha.split(" ")
                if palavras[0] == "Kd":
                    rgb = self.lerTupla(palavras)
                    cores[nome] = self.convertToQcolor(rgb)
                elif palavras[0] == "newmtl":
                    nome = palavras[1]
        return cores

    def convertToQcolor(self, rgb: tuple) -> QColor:
        """Converte tupla RGB (255.0, 0.0, 0.0) para QColor.fromRgbF"""
        r, g, b = (component / 255.0 for component in rgb)
        return QColor.fromRgbF(r, g, b, 1.0)
    
    def readFileObj(self, name_file: str) -> dict:
        name_file = "wavefront/" + name_file

        edges = []
        graphics_elements = {}
        nameObj = ""
        typeObj = ""
        colorObj = ""
        points = []
        colors = {}

        with open(name_file, "r") as file:
            line = file.readline()
            while line:
                word = line.split(" ")
                if word[0] == "v":
                    edges.append(self.lerTupla(word))
                elif word[0] == "o":
                    nameObj = word[1]
                    
                elif word[0] == "p":
                    typeObj = "Ponto"
                    points.append(int(word[1]))
                    graphics_elements[nameObj] = [typeObj, colorObj, points]
                
                elif word[0] == "l":
                    typeObj = self.decidirTipo(len(word))
                    points = self.lerLista(word[1:])
                    if typeObj == "Wireframe":
                        # False se refere ao preenchimento ou nao do polígono.
                        graphics_elements[nameObj] = [typeObj, colorObj, points, False]
                    else:
                        graphics_elements[nameObj] = [typeObj, colorObj, points]
                        
                elif word[0] == "f":
                    typeObj = "Wireframe"
                    points = self.lerLista(word[1:])
                    # Poligono preenchido (True)
                    graphics_elements[nameObj] =  [typeObj, colorObj, points, True]
                    
                elif word[0] == "mtllib":
                    name_mtl = "wavefront/" + word[1].strip()
                    colors = self.lerArquivoMTL(name_mtl)
                elif word[0] == "usemtl":
                    colorObj = colors[word[1]]
                    
                line = file.readline()
        
        print(graphics_elements)
        print(edges)
        return edges, graphics_elements

    def lerTupla(self, palavras: list) -> tuple:
        return (float(palavras[1]), float(palavras[2]), float(palavras[3]))

    def lerLista(self, palavras: list) -> list:
        pontos = []
        for ponto in palavras:
            pontos.append(int(ponto))
        return pontos

    def decidirTipo(self, tamanho: int) -> str:
        if tamanho == 3:
            return "Reta"
        return "Wireframe"
