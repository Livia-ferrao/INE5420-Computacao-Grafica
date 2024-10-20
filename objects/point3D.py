# from objects.object import Object3D
# from PySide6.QtGui import QPen
# from tools.type import Type
# from tools.clipping import Clipping
# from tools.matrix_generator import MatrixGenerator
# import numpy as np

# class Ponto3D(Object3D):
#     def __init__(self, name, coord, color):
#         super().__init__(name, Type.POINT_3D, coord, color)
    
#     def draw(self, window, painter, viewport):
#         # Normalizar as coordenadas
#         normalized_coords = self.normalizeCoords(window)

#         # Determina se vai desenhar o ponto
#         (draw, coords) = Clipping.pointClipping(normalized_coords, window)

#         if draw:
#             # Transforma para coordenadas da viewport
#             coord_viewport = viewport.calcularCoordsViewport(coords)

#             # Desenha o ponto
#             pen = QPen(self.color, 2)
#             painter.setPen(pen)
#             # Desenhar apenas a projeção 2D (ignorar o eixo Z)
#             painter.drawPoint(coord_viewport[0][0], coord_viewport[0][1])

#     # Faz a translação do ponto 3D
#     def translate(self, dx, dy, dz):
#         translation_matrix = MatrixGenerator.generateTranslationMatrix3D(dx, dy, dz)
#         self.__applyTransformation(translation_matrix)

#     # Faz o escalonamento do ponto 3D
#     def scale(self, sx, sy, sz):
#         center_coord = self.getCenter()

#         translating = MatrixGenerator.generateTranslationMatrix3D(-center_coord[0], -center_coord[1], -center_coord[2])
#         scaling = MatrixGenerator.generateScalingMatrix3D(sx, sy, sz)
#         translating_back = MatrixGenerator.generateTranslationMatrix3D(center_coord[0], center_coord[1], center_coord[2])

#         scaling_matrix = np.matmul(np.matmul(translating, scaling), translating_back)
#         self.__applyTransformation(scaling_matrix)

#     # Faz a rotação do ponto 3D em torno do eixo X
#     def rotateX(self, theta):
#         center_coord = self.getCenter()
#         translating = MatrixGenerator.generateTranslationMatrix3D(-center_coord[0], -center_coord[1], -center_coord[2])
#         rotation = MatrixGenerator.generateRotationMatrix3D_X(theta)
#         translating_back = MatrixGenerator.generateTranslationMatrix3D(center_coord[0], center_coord[1], center_coord[2])

#         rotation_matrix = np.matmul(np.matmul(translating, rotation), translating_back)
#         self.__applyTransformation(rotation_matrix)

#     # Faz a rotação do ponto 3D em torno do eixo Y
#     def rotateY(self, theta):
#         center_coord = self.getCenter()
#         translating = MatrixGenerator.generateTranslationMatrix3D(-center_coord[0], -center_coord[1], -center_coord[2])
#         rotation = MatrixGenerator.generateRotationMatrix3D_Y(theta)
#         translating_back = MatrixGenerator.generateTranslationMatrix3D(center_coord[0], center_coord[1], center_coord[2])

#         rotation_matrix = np.matmul(np.matmul(translating, rotation), translating_back)
#         self.__applyTransformation(rotation_matrix)

#     # Faz a rotação do ponto 3D em torno do eixo Z
#     def rotateZ(self, theta):
#         center_coord = self.getCenter()
#         translating = MatrixGenerator.generateTranslationMatrix3D(-center_coord[0], -center_coord[1], -center_coord[2])
#         rotation = MatrixGenerator.generateRotationMatrix3D_Z(theta)
#         translating_back = MatrixGenerator.generateTranslationMatrix3D(center_coord[0], center_coord[1], center_coord[2])

#         rotation_matrix = np.matmul(np.matmul(translating, rotation), translating_back)
#         self.__applyTransformation(rotation_matrix)

#     # Aplica uma matriz de transformação ao ponto 3D
#     def __applyTransformation(self, matrix):
#         new_coord = []
#         for x, y, z in self.coord:
#             new = np.matmul(np.array([x, y, z, 1]), matrix).tolist()
#             new_coord.append([new[0], new[1], new[2]])
#         self.coord = new_coord
