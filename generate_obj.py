from descritor_obj import DescritorOBJ
from type import Type
from PySide6.QtGui import QColor

class GenerateOBJ(DescritorOBJ):
    def __init__(self, display_file):
        objects, edges = self.generateEdges(display_file)

        self.objects = objects
        self.edges = edges
        self.colors = []

    def generateFileObj(self, name_file):
        # self.verificar_nome_escrita(self.nome_arquivo)
        name_file = "wavefront/" + name_file
        
        with open("wavefront/cores.mtl", "w") as file:
            file.write("")

        with open(name_file, "w") as file:
            for i in range(len(self.edges)):
                saida = (
                    "v "
                    + str(self.edges[i][0])
                    + " "
                    + str(self.edges[i][1])
                    + "\n"
                )
                file.write(saida)
            file.write("mtllib cores.mtl\n\n")
            for key, val in self.objects.items():
                name = "o " + key + "\n"
                file.write(name)
                color = self.generateMTLFile(val[2])
                file.write(color)
                coords = (
                    val[0]
                    + " "
                    + str(val[1]).replace("[", "").replace("]", "").replace(",", "")
                    + "\n"
                )
                file.write(coords)

    # Converte o QColor para valores RGB
    def generateMTLFile(self, qcolor):
        r, g, b, _ = qcolor.getRgbF()
        
        rgb = (r, g, b)
        new_color = False
        if rgb not in self.colors:
            new_color = True
            self.colors.append(rgb)
        
        name = "Cor_" + str(self.colors.index(rgb) + 1) + "\n"
        
        if new_color:
            with open("wavefront/cores.mtl", "a") as file:
                file.write("newmtl " + name)
                color = "Kd {:.6f} {:.6f} {:.6f}\n\n".format(r, g, b)
                file.write(color)
        
        return "usemtl " + name

    def generateEdges(self, display_file):
        objects = {}
        edges = []
        for obj in display_file.objects_list:
            objects[obj.name] = ["", [], ()]
            for coord in obj.coord:
                if coord not in edges:
                    edges.append(coord)
                    
                if obj.tipo == Type.POINT:
                    objects[obj.name][0] = "p"
                elif obj.tipo == Type.WIREFRAME and obj.filled:
                    objects[obj.name][0] = "f"
                else:
                    objects[obj.name][0] = "l"
                    
                objects[obj.name][1].append(edges.index(coord) + 1)
                objects[obj.name][2] = obj.color
                
        print("objects: ", objects)
        print()
        print("edges: ", edges)
        return objects, edges
