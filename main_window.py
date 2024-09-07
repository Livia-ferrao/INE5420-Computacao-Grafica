from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtWidgets import QMessageBox

from configurations import Configurations
from window import Window
from viewport import Viewport
from qtd_points import QtdPoints
from add_point import AddPoint
from add_line import AddLine
from add_polygon import AddPolygon
from display_file import DisplayFile
from operationsMessage import OperationsMessage

class MainWindow(QtWidgets.QMainWindow):
    """
    This class inherits from PyQt5 and handles all configs to run the 
    main window of the application
    """
    def __init__(self):
        super().__init__()
        self.__display_file = DisplayFile()
        # self.__g_object_handler = GObjectHandler(self.__display_file)
        self.window = Window()
        self.setFixedSize(Configurations.window_X(), Configurations.window_Y())
        self.setWindowTitle('Window')
        self.setStyleSheet("background-color: rgb(212,208,200);")
        self.__draw_elements()

    def __build_frame(self, parent, x, y, w, h):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(x, y, w, h)
        frame.setStyleSheet("QFrame { border: 2px solid black; }")
    
        return frame

    def __draw_elements(self):
        # Frame de ferramentas (lateral esquerda)
        self.__tools_frame = self.__build_frame(self, Configurations.tool_frame()[0],
                                         Configurations.tool_frame()[1],
                                         Configurations.tool_frame()[2],
                                         Configurations.tool_frame()[3])
   
        # Frame de visualização (direita)
        self.__view_frame = self.__build_frame(self, Configurations.view_frame()[0],
                                         Configurations.view_frame()[1],
                                         Configurations.view_frame()[2],
                                         Configurations.view_frame()[3])
        self.__view_frame.setStyleSheet("QFrame { background-color: rgb(255, 255, 255); border: 2px solid black; }")

        # Frame da viewport
        self.__viewport = Viewport(parent=self.__view_frame)
        self.__viewport.setGeometry(Configurations.viewport()[0],
                                Configurations.viewport()[1],
                                Configurations.viewport()[2],
                                Configurations.viewport()[3])
        self.window.set_viewport(self.__viewport)

        # Label do frame de objetos
        self.__objects_label = QtWidgets.QLabel("Gerenciar objetos", self.__tools_frame)
        self.__objects_label.setGeometry(80, Configurations.objects_frame()[1] - 20, 140, 20)
        self.__objects_label.setStyleSheet("background-color: rgb(212,208,200); color: black; border: none;")

        # Frame de objetos
        self.__objects_frame = self.__build_frame(self.__tools_frame, Configurations.objects_frame()[0],
                                         Configurations.objects_frame()[1],
                                         Configurations.objects_frame()[2],
                                         Configurations.objects_frame()[3])
        self.__objects_frame.setStyleSheet("background-color: rgb(165,165,165);")

        # Label do frame de controle da window
        self.__objects_label = QtWidgets.QLabel("Controle da window", self.__tools_frame)
        self.__objects_label.setGeometry(80, Configurations.control_frame()[1] - 20, 140, 20)
        self.__objects_label.setStyleSheet("background-color: rgb(212,208,200); color: black; border: none;")

        # Frame de controle da window
        self.__control_frame = self.__build_frame(self.__tools_frame, Configurations.control_frame()[0],
                                         Configurations.control_frame()[1],
                                         Configurations.control_frame()[2],
                                         Configurations.control_frame()[3])
        self.__control_frame.setStyleSheet("background-color: rgb(165,165,165);")
        
        # Botões de controle da window
        layout = QtWidgets.QGridLayout(self.__control_frame)

        self.__btnUp = QtWidgets.QPushButton("", self.__control_frame)
        self.__btnDown = QtWidgets.QPushButton("", self.__control_frame)
        self.__btnLeft = QtWidgets.QPushButton("", self.__control_frame)
        self.__btnRight = QtWidgets.QPushButton("", self.__control_frame)
        self.__btnZoomIn = QtWidgets.QPushButton("", self.__control_frame)
        self.__btnZoomOut = QtWidgets.QPushButton("", self.__control_frame)

        self.__btnRight.setIcon(QtGui.QIcon("icons/right.png"))
        self.__btnDown.setIcon(QtGui.QIcon("icons/down.png"))
        self.__btnLeft.setIcon(QtGui.QIcon("icons/left.png"))
        self.__btnUp.setIcon(QtGui.QIcon("icons/up.png"))
        self.__btnZoomIn.setIcon(QtGui.QIcon("icons/zoomin.png"))
        self.__btnZoomOut.setIcon(QtGui.QIcon("icons/zoomout.png"))

        layout.addWidget(self.__btnZoomIn, 2, 0)
        layout.addWidget(self.__btnUp, 1, 1)
        layout.addWidget(self.__btnZoomOut, 2, 2)
        layout.addWidget(self.__btnLeft, 1, 0)
        layout.addWidget(self.__btnRight, 1, 2)
        layout.addWidget(self.__btnDown, 2, 1)
 
        # self.__btnZoomOut.clicked.connect(self.__zoom_out)
        # self.__btnZoomIn.clicked.connect(self.__zoom_in)
        # self.__btnUp.clicked.connect(self.__move_up)
        # self.__btnDown.clicked.connect(self.__move_down)
        # self.__btnLeft.clicked.connect(self.__move_left)
        # self.__btnRight.clicked.connect(self.__move_right)

        # Botões no frame de objetos
        self.__combo_box = QtWidgets.QComboBox(self.__objects_frame)
        self.__combo_box.setGeometry(165, 30, 100, 30)
        self.__combo_box.addItems(["Ponto", "Reta", "Polígono"])
        self.__combo_box.setStyleSheet("background-color: rgb(212,208,200); color: black")
        
        self.__add_button = QtWidgets.QPushButton('Adicionar', self.__objects_frame)
        self.__add_button.setGeometry(165, 80, 100, 30)
        self.__add_button.clicked.connect(self.add_object)
        self.__add_button.setStyleSheet("background-color: rgb(212,208,200); color: black")

        self.__add_button = QtWidgets.QPushButton('Operações', self.__objects_frame)
        self.__add_button.setGeometry(165, 120, 100, 30)
        self.__add_button.clicked.connect(self.choose_operation)
        self.__add_button.setStyleSheet("background-color: rgb(212,208,200); color: black")

        # Lista de objetos
        self.__object_list = QtWidgets.QListWidget(self.__objects_frame)
        self.__object_list.setGeometry(10, 10, 140, 145)
        self.__object_list.setStyleSheet("background-color: rgb(240,240,240); color: black; border: 1px solid black")
        
        
        # self.__edit_button = QtWidgets.QPushButton('Editar', self.__objects_frame)
        # self.__remove_button = QtWidgets.QPushButton('Remover', self.__objects_frame)
        # self.__create_button = QtWidgets.QPushButton('Criar', self.__objects_frame)
        # layout_objects = QtWidgets.QGridLayout(self.__objects_frame)

        # layout_objects.addWidget(self.__edit_button, 0, 1)
        # layout_objects.addWidget(self.__remove_button, 1, 1)
        # layout_objects.addWidget(self.__create_button, 2, 1)
        
#         # Padding around the buttons
#         layout.setContentsMargins(10, 10, 10, 10)

    def add_object(self):
        selected_option = self.__combo_box.currentText()
        if selected_option == "Ponto":
            add_dialog = AddPoint()
        elif selected_option == "Reta":
            add_dialog = AddLine()
        elif selected_option == "Polígono":
            qtd_dialog = QtdPoints()
            if qtd_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                add_dialog = AddPolygon(qtd_dialog.qtd_input.value())
        if add_dialog:
            if add_dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                obj = add_dialog.create()
                print(obj)
                self.__display_file.add_object(obj)
                self.__object_list.addItem(str(obj.name))
                #self.__viewport.draw_objects(self.__display_file.objects_list)

    def choose_operation(self):
        operations_message = OperationsMessage()
        op = operations_message.exec()
        
        if op == QtWidgets.QMessageBox.Open:
            self.delete_object()
        else:
            pass
    
    def delete_object(self):
        selected_index = self.__object_list.currentRow()
        print(selected_index)
        
        if selected_index != -1:
            self.__object_list.takeItem(selected_index)
            self.__display_file.remove_object(selected_index)
            # TODO: redesenhar desenhos na tela
            # self.resetar_desenhos()
        else:
            print("No item selected for deletion.")
                
        
#     @property
#     def g_object_handler(self):
#         return self.__g_object_handler
    
#     @property
#     def objects_list(self):
#         return self.__objects_list
    
#     def write_feedback(self, text: str) -> None:
#         self.__feedback_label.setText(text)

#     def __zoom_in(self) -> None:
#         in_scale = 1 - self.__scale_spin.value()/100
#         self.__proceed_window_zoom(in_scale)

#     def __zoom_out(self) -> None:
#         out_scale = 1 + self.__scale_spin.value()/100
#         self.__proceed_window_zoom(out_scale)

#     def __proceed_window_zoom(self, scale: float) -> None:
#         self.world_window.zoom(scale, scale)
#         self.viewport.update()

    # def __move_up(self):
    #     up_delta = self.viewport.height()/100
    #     self.__procced_move_y(up_delta)

#     def __move_down(self):
#         up_delta = - self.viewport.height() * self.__scale_spin.value()/100
#         self.__procced_move_y(up_delta)

#     def __move_left(self):
#         left_delta = - self.viewport.width() * self.__scale_spin.value()/100
#         self.__proceed_move_x(left_delta)

#     def __move_right(self):
#         right_delta = self.viewport.width() * self.__scale_spin.value()/100
#         self.__proceed_move_x(right_delta)

#     def __proceed_move_x(self, delta: float) -> None:
#         self.world_window.translate(delta, 0)
#         self.viewport.update()

    # def __procced_move_y(self, delta: float) -> None:
    #     self.window.translate(0, delta)
    #     self.viewport.update()

#     def run_object_creation(self, name: str, validated_fields: list[tuple[int]]) -> None:
#         points = [CartesianPoint(item[0], item[1]) for item in validated_fields]
#         self.__g_object_handler.create_element(name, points)
#         self.__objects_list.add_element(name)
#         self.viewport.update()
#         self.write_feedback(f'[SUCESSO] Objeto {name} (pontos {validated_fields}) criado!')

#     def run_object_creation_from_shape(self, final_shape: GraphicObject) -> None:
#         self.__g_object_handler.create_element_from_object(final_shape)
#         self.__objects_list.add_element(final_shape.name)
#         self.viewport.update()
#         self.write_feedback(f'[SUCESSO] Objeto {final_shape.name} (pontos {final_shape.points}) criado!')

#     def run_object_remotion(self, index: int) -> None:
#         removed = self.__g_object_handler.remove_element(index)
#         self.viewport.update()
#         self.write_feedback(f'[SUCESSO] Objeto {removed.name} (pontos {removed.points}) removido')

#     def run(self):
#         self.show()

# class ObjectsList(QtWidgets.QListWidget):
#     def __init__(self, root: QtWidgets.QWidget, parent: QtWidgets.QFrame, g_object_handler: GObjectHandler, viewport: Viewport):
#         super().__init__(parent)
#         self.__root = root
#         self.setGeometry(OBJECT_LIST_GEOMETRY)
#         layout = QtWidgets.QVBoxLayout()
#         self.__edit_button = self.__build_button('Editar', (GENERAL_MARGIN, 130, CRUD_BUTTONS_SIZE[0], CRUD_BUTTONS_SIZE[1]), parent, layout, BACKGROUND_YELLOW)
#         self.__remove_button = self.__build_button('Remover', (GENERAL_MARGIN, 150, CRUD_BUTTONS_SIZE[0], CRUD_BUTTONS_SIZE[1]), parent, layout, BACKGROUND_RED)
#         self.__create_button = self.__build_button('Criar objeto', (GENERAL_MARGIN, 170, CRUD_BUTTONS_SIZE[0], CRUD_BUTTONS_SIZE[1]), parent, layout, BACKGROUND_GREEN)
#         self.__layout = layout
#         self.viewport = viewport

#         self.__edit_button.clicked.connect(self.__handle_click_on_edit)
#         self.__create_button.clicked.connect(self.__handle_click_on_create)
#         self.__remove_button.clicked.connect(self.__handle_click_on_remove)
#         self.itemDoubleClicked.connect(self.__handle_click_on_edit)

#     def __build_button(self, text: str, geometry: tuple[int], parent: QtWidgets.QWidget, layout: QtWidgets.QLayout, style: str) -> QtWidgets.QPushButton:
#         button = QtWidgets.QPushButton(text, parent)
#         button.setGeometry(geometry[0], geometry[1], geometry[2], geometry[3])
#         layout.addWidget(button)
#         button.setStyleSheet(style)
#         return button

#     def add_element(self, name: str, g_type: GraphicObjectEnum = None) -> None:
#         self.addItem(f'{name}')
    
#     def remove_element(self, row: int) -> None:
#         self.takeItem(row)

#     def __handle_click_on_create(self, root: QtWidgets.QWidget) -> None:
#         creation_popup = CreationPopup(self.__root, self.viewport)
#         creation_popup.exec_()

#     def __handle_click_on_remove(self, root: QtWidgets.QWidget) -> None:
#         selected_item = self.currentItem()
#         if selected_item != None:
#             selected_item_name = self.currentItem().text()
#             selected_row = self.currentRow()
#             remove_popup = RemovePopup(self.__root, selected_item_name, selected_row)
#             if remove_popup.exec_() == QtWidgets.QDialog.Accepted:
#                 self.takeItem(selected_row)
    
    
#     def __handle_click_on_edit(self):
#         selected_item = self.currentItem()
#         if selected_item:
#             edit_popup = EditPopup(self.currentRow(), self)
#             if edit_popup.exec_() == QtWidgets.QDialog.Accepted:
#                 # TODO PARA O TRABALHO 2
#                 # Chamar o GObjectHandler.edit(), passando as informações do formulário
#                 pass

# class RemovePopup(QtWidgets.QDialog):
#     """
#     Class to handle with remotion of elements on list
#     """
#     # TODO identificar e passar o tipo nesse construtor
#     def __init__(self, parent: QtWidgets.QWidget, name: str, index: int):
#         super().__init__(parent)
#         self.setWindowTitle(REMOVE_POPUP_TITLE)
#         self.__label = QtWidgets.QLabel(f"Você quer mesmo deletar o objeto {name}?")
#         self.__object_index = index
#         self.__draw_elements()
#         self.__configure()
        
#     def __configure(self) -> None:
#         self.__confirm_button.clicked.connect(self.__handle_confirm)
#         self.__cancel_button.clicked.connect(self.__handle_cancel)
    
#     def __draw_elements(self) -> None:
#         self.__confirm_button = QtWidgets.QPushButton("Sim, deletar")
#         self.__confirm_button.setStyleSheet(BACKGROUND_RED)
#         self.__cancel_button = QtWidgets.QPushButton("Cancelar")

#         layout = QtWidgets.QGridLayout()
#         layout.addWidget(self.__label, 0, 0)
#         layout.addWidget(self.__confirm_button, 1, 0)
#         layout.addWidget(self.__cancel_button, 1, 1)
#         self.setLayout(layout)

#     def __handle_confirm(self) -> None:
#         self.parent().run_object_remotion(self.__object_index)
#         self.accept()
    
#     def __handle_cancel(self) -> None:
#         self.reject()


# class CreationPopup(QtWidgets.QDialog):
#     """
#     Class to the popup of graphic objects cretion
#     """
#     def __init__(self, parent: QtWidgets.QWidget, viewport: Viewport):
#         super().__init__(parent)
#         self.__configure()
#         self.__draw_elements()
#         self.viewport = viewport

#     def __configure(self):
#         self.setModal(True)
#         self.setFixedSize(POPUP_SIZE[0], POPUP_SIZE[1])
#         self.setWindowTitle(CREATION_POPUP_TITLE)

#     def __draw_elements(self) -> None:
#         """
#         Draw PyQT5 elements on the popup
#         """
#         tab = QtWidgets.QTabWidget(self)
#         tab.setGeometry(0, 0, POPUP_SIZE[0], POPUP_SIZE[1] - 200)

#         items = {
#             'POINT': 1,
#             'LINE': 2
#         }

#         fields = {}

#         for num, item in enumerate(GraphicObjectEnum):
#             if item == GraphicObjectEnum.TEMP_SHAPE:
#                 break
#             item_str = GraphicObjectEnum.get_value(item)

#             item_tab = QtWidgets.QWidget()
#             form = QtWidgets.QFormLayout()
#             item_tab.setLayout(form)
#             tab.addTab(item_tab, item_str)

#             name_field = QtWidgets.QLineEdit()
#             form.addRow(f'Nome do {item_str}:', name_field)
#             points_field = QtWidgets.QLineEdit()
#             placeholder_txt = self.__generate_placeholder(num + 1)
#             points_field.setPlaceholderText(placeholder_txt)
#             form.addRow(f'Ponto(s):', points_field)

#             fields[item_str] = [name_field]
#             fields[item_str].append(points_field)

#             if item == GraphicObjectEnum.WIREFRAME:
#                 qtd_points_field = QtWidgets.QSpinBox(value=3,
#                                                minimum=3,
#                                                maximum=100,
#                                                singleStep=1)
#                 form.addRow('Qtd de pontos', qtd_points_field)
#                 fields[item_str].append(qtd_points_field)

#         button = QtWidgets.QPushButton('Criar elemento', self,
#                                  clicked = lambda: self.__create_object(tab.currentIndex()))
#         button.setGeometry(SUBMIT_CREATION_BUTTON_GEOMETRY)

#         dyn_button = QtWidgets.QPushButton('Criar elemento por cliques', self,
#                                      clicked = lambda: (self.__validate_and_allow_clicking(tab.currentIndex()), self.close()))
#         dyn_button.setGeometry(MOUSE_CREATION_BUTTON_GEOMETRY)
#         dyn_button.setStyleSheet(BACKGROUND_GREEN)

#         self.__fields = fields

#     def __validate_and_allow_clicking(self, tab_index: int):
#         try:
#             name = self.__validate_name_field(tab_index)
#             if tab_index > 2:
#                 self.viewport.allow_clicking_points(tab_index, name, None)
#             else:
#                 self.viewport.allow_clicking_points(tab_index, name, self.__fields['WIREFRAME'][2].value())
#         except Exception as e:
#             self.parent().write_feedback('[ERRO] Formulário de criação inválido! Tente novamente...')
#             self.reject()

#     def __validate_name_field(self, tab_index: int) -> str:
#         fields = self.__fields[list(self.__fields.keys())[tab_index]]
#         fields_text = [field.text() for field in fields]
#         if fields_text[0] == '':
#             raise FormValidationError()
#         return fields_text[0]

#     def __generate_placeholder(self, qtd: int) -> str:
#         string = ''
#         for i in range(qtd): string += f'(x{i}, y{1}),'
#         return string[:-1]

#     def __create_object(self, tab_index: int) -> None:
#         """
#         High level logic of creation
#         """
#         try:
#             name, validated_fields = self.__validate_form(tab_index)
#             self.parent().run_object_creation(name, validated_fields)
#             self.accept()
#         except Exception as e:
#             self.parent().write_feedback('[ERRO] Formulário de criação inválido! Tente novamente...')
#             self.reject()

#     def __validate_form(self, tab_index: int) -> list:
#         """
#         Validates the form of creation of elements
#         """
#         try:
#             name = self.__validate_name_field(tab_index)
#             fields = self.__fields[list(self.__fields.keys())[tab_index]]
#             validated_coords = []
#             points_str = fields[1].text()[1:-1].split('),(')
#             if tab_index == 2: assert len(points_str) == int(fields[2].value())
#             for point in points_str:
#                 x_str, y_str = point.strip().split(',')
#                 new_point = (float(x_str), float(y_str))
#                 validated_coords.append(new_point)
#             return name, validated_coords
#         except Exception as e:
#             raise FormValidationError()

#     def run(self):
#         self.show()
    
# class EditPopup(QtWidgets.QDialog):
#     # TODO definir para o trabalho 2
#     """
#     Popup to be used to edit the elements (tranformations)
#     """
#     def __init__(self, index: int, parent: QtWidgets.QWidget):
#         super().__init__(parent)
#         self.setWindowTitle(EDIT_POPUP_TITLE)
#         self.__label = QtWidgets.QLabel("Essa tela será utilizada no trabalho 2")
#         self.__draw_elements()
#         self.__configure()
        
#     def __configure(self):
#         self.__save_button.clicked.connect(self.__handle_save)
#         self.__cancel_button.clicked.connect(self.reject)
    
#     def __draw_elements(self):
#         self.__save_button = QtWidgets.QPushButton("Salvar")
#         self.__cancel_button = QtWidgets.QPushButton("Cancelar")

#         layout = QtWidgets.QVBoxLayout()
#         layout.addWidget(self.__label)
#         # layout.addWidget(self.__text_edit)
#         layout.addWidget(self.__save_button)
#         layout.addWidget(self.__cancel_button)
#         self.setLayout(layout)

#     def __handle_save(self):
#         # TODO PARA O TRABALHO 2
#         # new_text = self.text_edit.text()
#         # if new_text:
#         self.accept()
#         # else:
#             # QtWidgets.QMessageBox.warning(self, "Aviso", "O texto não pode estar vazio!")
