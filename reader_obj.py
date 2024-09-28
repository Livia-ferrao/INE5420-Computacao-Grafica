from descritor_obj import DescritorOBJ
from point import Point
from line import Line
from wireframe import Wireframe
from PySide6.QtGui import QColor

class ReaderOBJ(DescritorOBJ):
    def __init__(self):
        self.objects = []

    def openFile(self, name_file, display_file):
        # self.valid_name_file(name_file)
        edges, graphics_elements = self.readFileObj(name_file)

        for key, val in graphics_elements.items():
            
            # Precisa verificar se tem nome repetido?
            # i = 2
            name = key.strip()
            print(name)
            # while name in display_file.getNames():
            #     if i > 2:
            #         novo_nome = list(name)
            #         novo_nome[-1] = str(i)
            #         name = "".join(novo_nome)
            #     else:
            #         name = name + "_" + str(i)
            #     i += 1
                
            if val[0] == "Ponto":
                element = Point(name, self.getEdges(val[2], edges), val[1])
            elif val[0] == "Reta":
                element = Line(name, self.getEdges(val[2], edges), val[1])
            else:
                print("val[3]: ", val[3])
                element = Wireframe(name, self.getEdges(val[2], edges), val[1], val[3])

            self.objects.append(element)
        
        print('OBJECTS: ', self.objects)
        #  return objects

    def getEdges(self, index, edges):
        v = []
        for i in index:
            v.append(
                (
                    edges[i - 1][0],
                    edges[i - 1][1],
                )
            )
        return v

    def readMTLFile(self, name_file: str) -> dict:
        colors = {}
        name = ""
        rgb = ()

        with open(name_file, "r") as file:
            for line in file:
                words = line.split(" ")
                if words[0] == "Kd":
                    rgb = self.readTuple(words)
                    colors[name] = self.convertToQcolor(rgb)
                elif words[0] == "newmtl":
                    name = words[1]
        return colors

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
                    edges.append(self.readTuple(word))
                elif word[0] == "o":
                    nameObj = word[1]
                    
                elif word[0] == "p":
                    typeObj = "Ponto"
                    points.append(int(word[1]))
                    graphics_elements[nameObj] = [typeObj, colorObj, points]
                
                elif word[0] == "l":
                    typeObj = self.chooseType(len(word))
                    points = self.readList(word[1:])
                    if typeObj == "Wireframe":
                        # False se refere ao preenchimento ou nao do polígono.
                        graphics_elements[nameObj] = [typeObj, colorObj, points, False]
                    else:
                        graphics_elements[nameObj] = [typeObj, colorObj, points]
                        
                elif word[0] == "f":
                    typeObj = "Wireframe"
                    points = self.readList(word[1:])
                    # Poligono preenchido (True)
                    graphics_elements[nameObj] =  [typeObj, colorObj, points, True]
                    
                elif word[0] == "mtllib":
                    name_mtl = "wavefront/" + word[1].strip()
                    colors = self.readMTLFile(name_mtl)
                elif word[0] == "usemtl":
                    colorObj = colors[word[1]]
                    
                line = file.readline()
        
        print(graphics_elements)
        print(edges)
        return edges, graphics_elements

    def readTuple(self, words: list) -> tuple:
        return (float(words[1]), float(words[2]), float(words[3]))

    def readList(self, words: list) -> list:
        points = []
        for point in words:
            points.append(int(point))
        return points

    def chooseType(self, size: int) -> str:
        if size == 3:
            return "Reta"
        return "Wireframe"
