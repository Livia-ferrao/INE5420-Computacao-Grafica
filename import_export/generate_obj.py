from import_export.descritor_obj import DescritorOBJ
from tools.type import Type

class GenerateOBJ(DescritorOBJ):
    def __init__(self, display_file):
        objects, edges = self.generateEdges(display_file)

        self.objects = objects
        self.edges = edges
        self.colors = []

    # Cria arquivo com os objetos da viewport
    def generateFileObj(self, name_file):        
        with open("wavefront/cores.mtl", "w") as file:
            file.write("")

        with open(name_file, "w") as file:
            for i in range(len(self.edges)):
                saida = (
                    "v "
                    + "{:.1f}".format(self.edges[i][0]) + " "
                    + "{:.1f}".format(self.edges[i][1]) + " "
                    + "0.0\n"
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

    # Converte o QColor para valores RGB normais
    def generateMTLFile(self, qcolor):
        r, g, b, _ = qcolor.getRgbF()

        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        rgb = (r, g, b)
        new_color = False
        if rgb not in self.colors:
            new_color = True
            self.colors.append(rgb)
        
        name = "Cor_" + str(self.colors.index(rgb) + 1) + "\n"
        
        if new_color:
            with open("wavefront/cores.mtl", "a") as file:
                file.write("newmtl " + name)
                color = "Kd {} {} {}\n\n".format(r, g, b)
                file.write(color)
        
        return "usemtl " + name

    # Cria os vértices
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
                
        return objects, edges