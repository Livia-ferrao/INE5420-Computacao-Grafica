from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox

from edit_object import EditObject
from configurations import Configurations
from window import Window
from viewport import Viewport
from qtd_points import QtdPoints
from add_point import AddPoint
from add_line import AddLine
from add_wireframe import AddWireframe
from display_file import DisplayFile
from operations import Operations

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.setFixedSize(Configurations.window_X(), Configurations.window_Y())
        self.setWindowTitle('Window')
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
    def __createControlFrameButton(self, path_icon, function):
        button = QtWidgets.QPushButton(self.__control_frame)
        button.setIcon(QtGui.QIcon(path_icon))
        button.clicked.connect(function)
        button.setStyleSheet("background-color: rgb(212,208,200);")
        return button
    
    # Construção dos botões do frame de objetos
    def __createObjectFrameButton(self, name, function):
        button = QtWidgets.QPushButton(name, self.__objects_frame)
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
        self.__viewport = Viewport(self.__view_frame, self.__window)

        # Label da viewport
        self.__viewport_label = self.__buildLabel("Viewport", self.__view_frame, 
                                            250, Configurations.viewport()[1] - 20, 140, 20)

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


        # Botões de controle da window
        self.__button_up = self.__createControlFrameButton("icons/up-arrow.png", self.__moveUp)
        self.__button_down = self.__createControlFrameButton("icons/down-arrow.png", self.__moveDown)
        self.__button_left = self.__createControlFrameButton("icons/left-arrow.png", self.__moveLeft)
        self.__button_right = self.__createControlFrameButton("icons/right-arrow.png", self.__moveRight)
        self.__button_zoom_in = self.__createControlFrameButton("icons/zoom-in.png", self.__zoomIn)
        self.__button_zoom_out = self.__createControlFrameButton("icons/zoom-out.png", self.__zoomOut)

        # Spin box da porcentagem de movimentação/zoom
        self.__control_scale = QtWidgets.QDoubleSpinBox()
        self.__control_scale.setValue(10.00)
        self.__control_scale.setMinimum(0.01)
        self.__control_scale.setMaximum(99.99)
        self.__control_scale.setSingleStep(1)
        self.__control_scale.setStyleSheet("background-color: rgb(212,208,200); color: black;")

        # Label "%" do lado da spin box da porcentagem de movimentação/zoom
        self.__scale_label = QtWidgets.QLabel("%")
        self.__scale_label.setStyleSheet("color: black; border: none;")

        # Layout do frame de controle
        self.__layout_control = QtWidgets.QGridLayout(self.__control_frame)
        self.__layout_control.addWidget(self.__control_scale, 0, 0)
        self.__layout_control.addWidget(self.__scale_label, 0, 1)
        self.__layout_control.addWidget(self.__button_up, 1, 2)
        self.__layout_control.addWidget(self.__button_left, 2, 1)
        self.__layout_control.addWidget(self.__button_right, 2, 3)
        self.__layout_control.addWidget(self.__button_down, 3, 2)
        self.__layout_control.addWidget(self.__button_zoom_in, 1, 0)
        self.__layout_control.addWidget(self.__button_zoom_out, 3, 0)

        # Combo box para escolher entre ponto, reta e polígono
        self.__combo_box = QtWidgets.QComboBox(self.__objects_frame)
        self.__combo_box.addItems(["Ponto", "Reta", "Polígono"])
        self.__combo_box.setStyleSheet("background-color: rgb(212,208,200); color: black")
        
        # Botões no frame de objetos
        self.__add_button = self.__createObjectFrameButton('Adicionar', self.__addObject)
        self.__operations_button = self.__createObjectFrameButton('Operações', self.__chooseOperation)

        # Lista de objetos
        self.__object_list = QtWidgets.QListWidget(self.__objects_frame)
        self.__object_list.setStyleSheet("background-color: rgb(240,240,240); color: black; border: 1px solid black")

        # Layout do frame de objetos
        self.__layout_objects = QtWidgets.QGridLayout(self.__objects_frame)
        self.__layout_objects.addWidget(self.__combo_box, 0, 1)
        self.__layout_objects.addWidget(self.__add_button, 1, 1)
        self.__layout_objects.addWidget(self.__operations_button, 2, 1)
        self.__layout_objects.addWidget(self.__object_list, 0, 0, 3, 1)

    # Ação do botão de adicionar objeto
    def __addObject(self):
        selected_option = self.__combo_box.currentText()
        if selected_option == "Ponto":
            add_dialog = AddPoint(self.__display_file, self.__object_list)
        elif selected_option == "Reta":
            add_dialog = AddLine(self.__display_file, self.__object_list)
        elif selected_option == "Polígono":
            qtd_dialog = QtdPoints() # Tela para indicar a quantidade de pontos do polígono
            if qtd_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                add_dialog = AddWireframe(self.__display_file, self.__object_list, qtd_dialog.qtdPoints())
            else:
                add_dialog = None
        if add_dialog:
            if add_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                # Se um objeto for adicionado, desenha objetos da window na viewport
                self.__viewport.drawObjects(self.__display_file.objects_list)

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
        else:
            # Mensagem aparece se nenhum objeto for selecionado
            message = QMessageBox()
            message.setWindowTitle("Aviso")
            message.setText("Selecione um objeto para realizar uma operação")
            message.setStyleSheet("background-color: rgb(212,208,200); color: black;")
            message.setFixedSize(400, 200)
            message.exec()
    
    # Deletar objeto
    def __deleteObject(self, index_selected_obj):
        self.__object_list.takeItem(index_selected_obj)
        self.__display_file.removeObject(index_selected_obj)
        self.__viewport.drawObjects(self.__display_file.objects_list)

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
                    self.__viewport.drawObjects(self.__display_file.objects_list)

    # Movimentação para esquerda
    def __moveLeft(self):
        self.__window.moveLeft(self.__control_scale.value())
        self.__viewport.drawObjects(self.__display_file.objects_list)
    
    # Movimentação para direita
    def __moveRight(self):
        self.__window.moveRight(self.__control_scale.value())
        self.__viewport.drawObjects(self.__display_file.objects_list)

    # Movimentação para cima
    def __moveUp(self):
        self.__window.moveUp(self.__control_scale.value())
        self.__viewport.drawObjects(self.__display_file.objects_list)
    
    # Movimentação para baixo
    def __moveDown(self):
        self.__window.moveDown(self.__control_scale.value())
        self.__viewport.drawObjects(self.__display_file.objects_list)
    
    # Zoom in
    def __zoomIn(self):
        self.__window.zoomIn(self.__control_scale.value())
        self.__viewport.drawObjects(self.__display_file.objects_list)
    
    # Zoom out
    def __zoomOut(self):
        self.__window.zoomOut(self.__control_scale.value())
        self.__viewport.drawObjects(self.__display_file.objects_list)