from descritor_obj import DescritorOBJ
from point import Point
from line import Line
from wireframe import Wireframe
from PySide6.QtGui import QColor
from os.path import exists

class ReaderOBJ(DescritorOBJ):
    def __init__(self, name_file):  
        # Verifica possíveis erros     
        self.erro = self.verify_valid_read_file(name_file)
        if self.erro:
            return
        self.objects = []

    # Abrir arquivo
    def openFile(self, name_file, display_file):
        edges, graphics_elements = self.readFileObj(name_file)

        for key, val in graphics_elements.items():

            name = key.strip()
            if val[0] == "Ponto":
                element = Point(name, self.getEdges(val[2], edges), val[1])
            elif val[0] == "Reta":
                element = Line(name, self.getEdges(val[2], edges), val[1])
            else:
                element = Wireframe(name, self.getEdges(val[2], edges), val[1], val[3])

            self.objects.append(element)
    
    # Retorna os vértices
    def getEdges(self, index, edges):
        v = []
        for i in index:
            v.append((edges[i - 1][0], edges[i - 1][1]))
        return v

    # Le arquivo de cores (MTL)
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

    # Converte tupla RGB (255.0, 0.0, 0.0) para QColor.fromRgbF
    def convertToQcolor(self, rgb: tuple) -> QColor:
        r, g, b = (component / 255.0 for component in rgb)
        return QColor.fromRgbF(r, g, b, 1.0)
    
    # Le o arquivo dos objetos
    def readFileObj(self, name_file: str) -> dict:
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
                if word[0] == "mtllib":
                    name_mtl = "wavefront/" + word[1].strip()
                    colors = self.readMTLFile(name_mtl)
                            
                elif word[0] == "usemtl":
                    colorObj = colors[word[1]]
                    
                elif word[0] == "v":
                    edges.append(self.readTuple(word))
                    
                elif word[0] == "o":
                    nameObj = word[1]
                    
                elif word[0] == "p":
                    typeObj = "Ponto"
                    points.append(int(word[1]))
                    graphics_elements[nameObj] = [typeObj, colorObj, points]
                
                elif word[0] == "l":
                    typeObj = "Reta" if len(word) == 3 else "Wireframe"
                    points = self.readList(word[1:])
                    if typeObj == "Wireframe":
                        graphics_elements[nameObj] = [typeObj, colorObj, points, False]
                    else:
                        graphics_elements[nameObj] = [typeObj, colorObj, points]
                        
                elif word[0] == "f":
                    typeObj = "Wireframe"
                    points = self.readList(word[1:])
                    graphics_elements[nameObj] =  [typeObj, colorObj, points, True]
                
                line = file.readline()
        
        return edges, graphics_elements

    # Leitura de tupla
    def readTuple(self, words: list) -> tuple:
        return (float(words[1]), float(words[2]), float(words[3]))

    # Leitura de lista
    def readList(self, words: list) -> list:
        points = []
        for point in words:
            points.append(int(point))
        return points