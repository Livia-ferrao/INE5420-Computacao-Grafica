from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import Qt

from popups.edit_object import EditObject
from main_interface.configurations import Configurations
from main_interface.window import Window
from main_interface.viewport import Viewport
from popups.qtd_points import QtdPoints
from popups.qtd_points_obj_3d import QtdPointsObj3D
from popups.add_point import AddPoint
from popups.add_line import AddLine
from popups.add_wireframe import AddWireframe
from popups.add_berzier_curve import AddBerzierCurve
from popups.add_bspline import AddBSpline
from popups.add_object_3d import AddObject3D
from main_interface.display_file import DisplayFile
from popups.operations import Operations
from popups.transformations_dialog import TransformationsDialog
from import_export.generate_obj import GenerateOBJ
from import_export.reader_obj import ReaderOBJ
from tools.type import ClippingAlgorithm
from main_interface.canvas import Canvas
from popups.qtd_curves import QtdCurves
from popups.qtd_points_bspline import QtdPointsBSpline
from objects.line import Line
from objects.wireframe import Wireframe
from objects.object3D import Object3D

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.setFixedSize(Configurations.window_X(), Configurations.window_Y())
        self.setWindowTitle('Sistema gráfico')
        self.setStyleSheet("background-color: rgb(212,208,200);")
        self.__drawElements()

    # Contrução de frames
    def __buildFrame(self, parent, x, y, w, h):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(x, y, w, h)
        frame.setStyleSheet("QFrame { border: 2px solid black; }")
        return frame

    # Construção de labels (textos/titulos)
    def __buildLabel(self, text, parent, x, y, w, h):
        label = QtWidgets.QLabel(text, parent)
        label.setGeometry(x, y, w, h)
        label.setStyleSheet("background-color: rgb(212,208,200); color: black; border: none;")
        return label
    
    # Construção dos botões de controle da window (movimentação e zoom)
    def __createControlFrameButton(self, path_icon, function, text):
        button = QtWidgets.QPushButton(self.__control_frame)
        button.setIcon(QtGui.QIcon(path_icon))
        button.setToolTip(text)
        button.clicked.connect(function)
        #button.setStyleSheet("background-color: rgb(212,208,200);")
        button.setStyleSheet("""
            QPushButton {
                background-color: rgb(212,208,200)
            }
            QPushButton:disabled {
                background-color: rgb(180, 175, 170)
            }
        """)
        return button
    
    # Construção dos botões do frame de objetos e arquivos
    def __createNameButton(self, name, function, frame):
        button = QtWidgets.QPushButton(name, frame)
        button.clicked.connect(function)
        button.setStyleSheet("background-color: rgb(212,208,200); color: black")
        return button
    
    # Desenha principais elementos da tela
    def __drawElements(self):
        # Frame de ferramentas (lateral esquerda)
        self.__tools_frame = self.__buildFrame(self, Configurations.tool_frame()[0],
                                         Configurations.tool_frame()[1],
                                         Configurations.tool_frame()[2],
                                         Configurations.tool_frame()[3])
   
        # Frame de visualização (direita)
        self.__view_frame = self.__buildFrame(self, Configurations.view_frame()[0],
                                         Configurations.view_frame()[1],
                                         Configurations.view_frame()[2],
                                         Configurations.view_frame()[3])

        # Viewport
        self.__viewport = Viewport(self.__window)

        # Área de desenho
        self.__canvas = Canvas(self.__view_frame, self.__viewport)

        # Frame de objetos
        self.__objects_frame = self.__buildFrame(self.__tools_frame, Configurations.objects_frame()[0],
                                         Configurations.objects_frame()[1],
                                         Configurations.objects_frame()[2],
                                         Configurations.objects_frame()[3])
        self.__objects_frame.setStyleSheet("background-color: rgb(165,165,165);")

        # Label do frame de objetos
        self.__objects_label = self.__buildLabel("Gerenciar objetos", self.__tools_frame,
                                           80, Configurations.objects_frame()[1] - 20, 140, 20)

        # Frame de controle da window
        self.__control_frame = self.__buildFrame(self.__tools_frame, Configurations.control_frame()[0],
                                         Configurations.control_frame()[1],
                                         Configurations.control_frame()[2],
                                         Configurations.control_frame()[3])
        self.__control_frame.setStyleSheet("background-color: rgb(165,165,165);")
        
        # Label do frame de controle da window
        self.__control_label = self.__buildLabel("Controle da window", self.__tools_frame,
                                           80, Configurations.control_frame()[1] - 20, 140, 20)
        
        # Frame de gerenciar arquivos
        self.__files_frame = self.__buildFrame(self.__tools_frame, *Configurations.files_frame())
        self.__files_frame.setStyleSheet("background-color: rgb(165,165,165);")
        
        # Label do frame de gerencia de arquivos
        self.___files_label = self.__buildLabel("Gerência de arquivos", self.__tools_frame,
                                           80, Configurations.files_frame()[1] - 20, 140, 20)

        # Frame de escolha de clipping
        self.__clipping_frame = self.__buildFrame(self.__tools_frame, *Configurations.clipping_frame())
        self.__clipping_frame.setStyleSheet("background-color: rgb(165,165,165);")

        self.__clipping_label = self.__buildLabel("Clipagem de segmentos de reta", self.__tools_frame,
                                                  40, Configurations.clipping_frame()[1] - 20, 215, 20)

        # Botões de controle da window
        self.__button_up = self.__createControlFrameButton("icons/up-arrow.png", self.__moveUp, "Mover window para cima")
        self.__button_down = self.__createControlFrameButton("icons/down-arrow.png", self.__moveDown, "Mover window para baixo")
        self.__button_left = self.__createControlFrameButton("icons/left-arrow.png", self.__moveLeft, "Mover window para esquerda")
        self.__button_right = self.__createControlFrameButton("icons/right-arrow.png", self.__moveRight, "Mover window para direita")
        self.__button_zoom_in = self.__createControlFrameButton("icons/zoom-in.png", self.__zoomIn, "Zoom in")
        self.__button_zoom_out = self.__createControlFrameButton("icons/zoom-out.png", self.__zoomOut, "Zoom out")
        self.__button_rotate_right = self.__createControlFrameButton("icons/rotate-right", self.__rotateRight, "Rotacionar window para direita no eixo z")
        self.__button_rotate_left = self.__createControlFrameButton("icons/rotate-left.png", self.__rotateLeft, "Rotacionar window para esquerda no eixo z")
        self.__button_front = self.__createControlFrameButton("icons/arrow-upper-right.png", self.__moveFront, "Mover window para frente")
        self.__button_back = self.__createControlFrameButton("icons/down-left-arrow.png", self.__moveBack, "Mover window para trás")
        self.__button_front.setEnabled(False)
        self.__button_back.setEnabled(False)

        # Spin box da porcentagem de movimentação/zoom
        self.__control_scale = QtWidgets.QDoubleSpinBox()
        self.__control_scale.setValue(10.00)
        self.__control_scale.setMinimum(0.01)
        self.__control_scale.setMaximum(99.99)
        self.__control_scale.setSingleStep(1)
        self.__control_scale.setStyleSheet("background-color: rgb(212,208,200); color: black;")

        # Label indicativo do lado da spin box da porcentagem de movimentação/zoom
        self.__scale_label = QtWidgets.QLabel("Passo de navegação")
        self.__scale_label.setStyleSheet("color: black; border: none;")

        # Label "%" do lado da spin box da porcentagem de movimentação/zoom
        self.__scale_label_percentage = QtWidgets.QLabel("%")
        self.__scale_label_percentage.setStyleSheet("color: black; border: none;")
        
        # Label indicativo do lado do spin box do ângulo de rotação
        self.__rotation_label = QtWidgets.QLabel("Ângulo de rotação")
        self.__rotation_label.setStyleSheet("color: black; border: none;")
        self.__rotation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Spin box do ângulo para rotação
        self.__angle_spin = QtWidgets.QSpinBox()
        self.__angle_spin.setValue(15)
        self.__angle_spin.setMinimum(0)
        self.__angle_spin.setMaximum(360)
        self.__angle_spin.setSingleStep(1)
        self.__angle_spin.setStyleSheet("background-color: rgb(212,208,200); color: black;")

        # Label "°" do lado da spin box do angulo de rotação
        self.__degrees_label = QtWidgets.QLabel("°")
        self.__degrees_label.setStyleSheet("color: black; border: none;")

        # 2D x 3D botão
        self.__dimensions_button = self.__createNameButton("2D", self.__changeDimension, self.__control_frame)
        
        # Layout do frame de controle
        self.__layout_control = QtWidgets.QGridLayout(self.__control_frame)
        self.__layout_control.addWidget(self.__button_up, 0, 2, 1, 2)
        self.__layout_control.addWidget(self.__button_left, 1, 1)
        self.__layout_control.addWidget(self.__button_right, 1, 4)
        self.__layout_control.addWidget(self.__button_down, 2, 2, 1, 2)
        self.__layout_control.addWidget(self.__button_zoom_in, 0, 0)
        self.__layout_control.addWidget(self.__button_zoom_out, 1, 0)
        self.__layout_control.addWidget(self.__button_rotate_right, 0, 1)
        self.__layout_control.addWidget(self.__button_rotate_left, 0, 4)
        self.__layout_control.addWidget(self.__dimensions_button, 2, 0)
        self.__layout_control.addWidget(self.__button_front, 1, 3)
        self.__layout_control.addWidget(self.__button_back, 1, 2)
        scale_hbox = QtWidgets.QHBoxLayout()
        scale_hbox.addWidget(self.__scale_label)
        scale_hbox.addWidget(self.__control_scale)
        scale_hbox.addWidget(self.__scale_label_percentage)
        angle_hbox = QtWidgets.QHBoxLayout()
        angle_hbox.addWidget(self.__rotation_label)
        angle_hbox.addWidget(self.__angle_spin)
        angle_hbox.addWidget(self.__degrees_label)
        self.__layout_control.addLayout(scale_hbox, 3, 0, 1, 5)
        self.__layout_control.addLayout(angle_hbox, 4, 0, 1, 5)

        # Combo box para escolher entre ponto, reta e polígono
        self.__combo_box = QtWidgets.QComboBox(self.__objects_frame)
        self.__combo_box.addItems(["Ponto", "Reta", "Polígono", "Curva de Bérzier", "B-Spline", "Objeto 3D"])
        self.__combo_box.setStyleSheet("background-color: rgb(212,208,200); color: black")
        
        # Botões no frame de objetos
        self.__add_button = self.__createNameButton('Adicionar', self.__addObject, self.__objects_frame)
        self.__operations_button = self.__createNameButton('Operações', self.__chooseOperation, self.__objects_frame)

        # Lista de objetos
        self.__object_list = QtWidgets.QListWidget(self.__objects_frame)
        self.__object_list.setStyleSheet("background-color: rgb(240,240,240); color: black; border: 1px solid black")
        
        # Label "Lista de objetos"
        self.__obj_list_label = QtWidgets.QLabel("Lista de objetos")
        self.__obj_list_label.setFixedHeight(13)
        self.__obj_list_label.setStyleSheet("color: black; border: none; font-size: 13px")
        
        # Layout do frame de objetos
        self.__layout_objects = QtWidgets.QGridLayout(self.__objects_frame)
        self.__layout_objects.addWidget(self.__combo_box, 1, 1)
        self.__layout_objects.addWidget(self.__add_button, 2, 1)
        self.__layout_objects.addWidget(self.__operations_button, 3, 1)
        self.__layout_objects.addWidget(self.__object_list, 1, 0, 3, 1)
        self.__layout_objects.addWidget(self.__obj_list_label, 0, 0)
        
        # Botões no frame de arquivos
        self.__read_file_button = self.__createNameButton('Importar arquivo', self.__readFile, self.__files_frame)
        self.__save_file_button = self.__createNameButton('Exportar arquivo', self.__saveFile, self.__files_frame)
        
        # Layout do frame de arquivos
        self.__layout_files = QtWidgets.QGridLayout(self.__files_frame)
        self.__layout_files.addWidget(self.__read_file_button, 0, 0)
        self.__layout_files.addWidget(self.__save_file_button, 0, 1)

        # Radio buttons do frame de clipping
        self.__radio = [QtWidgets.QRadioButton(ClippingAlgorithm.COHEN.value), QtWidgets.QRadioButton(ClippingAlgorithm.LIANG.value)]
        self.__radio[0].setChecked(True)
        self.__clipping_algorithm = ClippingAlgorithm.COHEN

        # Layout do frame de clipping
        self.__layout_clipping = QtWidgets.QVBoxLayout(self.__clipping_frame)
        for radio in self.__radio:
            radio.toggled.connect(self.__changeClipping)
            radio.setStyleSheet("color: black;")
            self.__layout_clipping.addWidget(radio)

        # Adicionando objetos para teste
        obj1 = Line("linha1", [(200, 0, 0), (400, 0, 0)], QtGui.QColor(0,0,0))
        self.__display_file.addObject(obj1)
        self.__object_list.addItem(str(obj1.name))
        obj2 = Wireframe("wireframe1", [(300, -200, 0), (-300, -200, 0), (0, 200, 0)], QtGui.QColor(255,0,0), True)
        self.__display_file.addObject(obj2)
        self.__object_list.addItem(str(obj2.name))
        obj3 = Object3D("cubo", [(-800, -800, 0), (-800, -400, 0), (-800, -400, 0), (-400, -400, 0), (-400, -400, 0), (-400, -800, 0), (-400, -800, 0), (-800, -800, 0), (-800, -800, -400), (-800, -400, -400), (-800, -400, -400), (-400, -400, -400), (-400, -400, -400), (-400, -800, -400), (-400, -800, -400), (-800, -800, -400), (-800, -800, 0), (-800, -800, -400), (-800, -400, 0), (-800, -400, -400), (-400, -800, 0), (-400, -800, -400), (-400, -400, 0), (-400, -400, -400)], QtGui.QColor(0,255,0))
        self.__display_file.addObject(obj3)
        self.__object_list.addItem(str(obj3.name))
        
        self.__updateViewframe()

    # Redesenha objetos
    def __updateViewframe(self):
        self.__canvas.drawObjects(self.__display_file.objects_list, self.__clipping_algorithm, self.__window)
    
    # Ler arquivo .obj
    def __readFile(self):
        filepath = QFileDialog.getOpenFileName(caption="Open Image", filter="Wavefront files (*.obj)")
        reader =  ReaderOBJ(filepath[0])
        if reader.files_exist:
            reader.createObjects()
            for obj in reader.objects:
                self.__display_file.addObject(obj)
                self.__object_list.addItem(str(obj.name))
            self.__updateViewframe()
    
    # Salvar arquivo .obj
    def __saveFile(self):
        filename = QFileDialog.getSaveFileName(caption="File to export", filter="Wavefront files (*.obj)")
        generator = GenerateOBJ(filename[0], self.__display_file.objects_list)
        if generator.file_creation_success:
            generator.generateFiles()
    
    # Trocar algoritmo de clipping de linhas
    def __changeClipping(self):
        if self.__radio[0].isChecked():
            self.__clipping_algorithm = ClippingAlgorithm.COHEN
        else:
            self.__clipping_algorithm = ClippingAlgorithm.LIANG
        self.__updateViewframe()
    
    # Ação do botão de adicionar objeto
    def __addObject(self):
        add_dialog = None
        selected_option = self.__combo_box.currentText()
        if selected_option == "Ponto":
            add_dialog = AddPoint(self.__display_file, self.__object_list)
        elif selected_option == "Reta":
            add_dialog = AddLine(self.__display_file, self.__object_list)
        elif selected_option == "Polígono":
            qtd_dialog = QtdPoints() # Tela para indicar a quantidade de pontos do polígono
            if qtd_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                add_dialog = AddWireframe(self.__display_file, self.__object_list, qtd_dialog.qtdPoints(),  qtd_dialog.isFilled())
        elif selected_option == "Curva de Bérzier":
            qtd_dialog = QtdCurves()
            if qtd_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                add_dialog = AddBerzierCurve(self.__display_file, self.__object_list, qtd_dialog.qtdCurves())
        elif selected_option == "B-Spline":
            qtd_dialog = QtdPointsBSpline()
            if qtd_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                add_dialog = AddBSpline(self.__display_file, self.__object_list, qtd_dialog.qtdPointsControl())
        elif selected_option == "Objeto 3D":
            qtd_dialog = QtdPointsObj3D()
            if qtd_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                add_dialog = AddObject3D(self.__display_file, self.__object_list, qtd_dialog.qtdPoints())
        
        if add_dialog:
            if add_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                self.__updateViewframe()

    # Ação do botão de operações para um objeto selecionado da lista
    def __chooseOperation(self):
        index_selected_obj = self.__object_list.currentRow()
        if index_selected_obj != -1:
            operations = Operations(self.__object_list.item(index_selected_obj).text())
            if operations.exec()== QtWidgets.QDialog.DialogCode.Accepted:
                if operations.clicked_button == "delete":
                    self.__deleteObject(index_selected_obj)
                elif operations.clicked_button == "edit":
                    self.__editObject(index_selected_obj)
                elif operations.clicked_button == "transformations":
                    self.__transformObject(index_selected_obj)
        else:
            # Mensagem aparece se nenhum objeto for selecionado
            message = QMessageBox()
            message.setWindowTitle("Aviso")
            message.setText("Selecione um objeto na lista de objetos para realizar uma operação")
            message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
            message.setFixedSize(400, 200)
            message.exec()
    
    # Deletar objeto
    def __deleteObject(self, index_selected_obj):
        self.__object_list.takeItem(index_selected_obj)
        self.__display_file.removeObject(index_selected_obj)
        self.__updateViewframe()

    # Editar objeto
    def __editObject(self, index_selected_obj):
        selected_item = self.__object_list.item(index_selected_obj)
        if selected_item:
            selected_object = self.__display_file.getObject(selected_item.text())
            if selected_object:
                edit_window = EditObject(selected_object, self.__display_file, self.__object_list)               
                if edit_window.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                    updated_object = edit_window.existing_object
                    selected_item.setText(updated_object.name) 
                    self.__display_file.updateObject(index_selected_obj, updated_object)
                    self.__updateViewframe()
    
    # Criar e executar transformações em um objeto
    def __transformObject(self, index_selected_obj):
        selected_obj = self.__display_file.objects_list[index_selected_obj]
        transform_window = TransformationsDialog(selected_obj, self.__window)
        if transform_window.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.__updateViewframe()

    # Rotacionar para esquerda
    def __rotateLeft(self):
        self.__window.rotate_z_axis(-self.__angle_spin.value())
        self.__updateViewframe() 

    # Rotacionar para direita
    def __rotateRight(self):
        self.__window.rotate_z_axis(self.__angle_spin.value())
        self.__updateViewframe()      

   # Botão movimentação para esquerda
    def __moveLeft(self):
        if self.__dimensions_button.text() == "2D":
            self.__window.moveLeft(self.__control_scale.value())
        else:
            self.__window.rotate_y_axis(-self.__angle_spin.value())
        self.__updateViewframe()
    
    # Botão movimentação para direita
    def __moveRight(self):
        if self.__dimensions_button.text() == "2D":
            self.__window.moveRight(self.__control_scale.value())
        else:
            self.__window.rotate_y_axis(self.__angle_spin.value())
        self.__updateViewframe()

    # Botão movimentação para cima
    def __moveUp(self):
        if self.__dimensions_button.text() == "2D":
            self.__window.moveUp(self.__control_scale.value())
        else:
            self.__window.rotate_x_axis(self.__angle_spin.value())
        self.__updateViewframe()
    
    # Botão movimentação para baixo
    def __moveDown(self):
        if self.__dimensions_button.text() == "2D":
            self.__window.moveDown(self.__control_scale.value())
        else:
            self.__window.rotate_x_axis(-self.__angle_spin.value())
        self.__updateViewframe()
    
    # Botão movimentação para frente
    def __moveFront(self):
        self.__window.moveFront(self.__control_scale.value())
        self.__updateViewframe()

    # Botão movimentação para trás
    def __moveBack(self):
        self.__window.moveBack(self.__control_scale.value())
        self.__updateViewframe()

    # Zoom in
    def __zoomIn(self):
        self.__window.zoomIn(self.__control_scale.value())
        self.__updateViewframe()
    
    # Zoom out
    def __zoomOut(self):
        self.__window.zoomOut(self.__control_scale.value())
        self.__updateViewframe()

    # Muda forma de "movimentação" entre 2D e 3D:
    # Em 2D movimenta nos eixos x e y
    # Em 3D rotaciona pelos eixos x e y e movimenta no eixo z
    def __changeDimension(self):
        if self.__dimensions_button.text() == "2D":
            self.__dimensions_button.setText("3D")
            self.__button_back.setEnabled(True)
            self.__button_front.setEnabled(True)
            self.__button_left.setToolTip("Rotacionar para esquerda no eixo y")
            self.__button_right.setToolTip("Rotacionar para direita no eixo y")
            self.__button_up.setToolTip("Rotationar para cima no eixo x")
            self.__button_down.setToolTip("Rotacionar para baixo no eixo x")
        else:
            self.__dimensions_button.setText("2D")
            self.__button_back.setEnabled(False)
            self.__button_front.setEnabled(False)
            self.__button_left.setToolTip("Mover window para esquerda")
            self.__button_right.setToolTip("Mover window para direita")
            self.__button_up.setToolTip("Mover window para cima")
            self.__button_down.setToolTip("Mover window para baixo")