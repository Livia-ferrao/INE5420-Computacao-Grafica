# from configurations import Configurations
# from abc import abstractmethod
# from add_object import AddObject

# class EditObject(AddObject):
#     def __init__(self, existing_object):
#         super().__init__()
#         self.existing_object = existing_object
#         self.populate_fields()

#     def populate_fields(self):
#         self.name_input.setText(self.existing_object.name)
#         for i, (x, y) in enumerate(zip(self.existing_object.x_coords, self.existing_object.y_coords)):
#             if i < len(self.x_inputs):
#                 self.x_inputs[i].setValue(x)
#                 self.y_inputs[i].setValue(y)

#     def setTitle(self):
#         self.setWindowTitle("Edit Object")

#     def accept(self):
#         # Update the existing object with the data from the input fields
#         self.existing_object.name = self.name_input.text()
#         self.existing_object.x_coords = [spinbox.value() for spinbox in self.x_inputs]
#         self.existing_object.y_coords = [spinbox.value() for spinbox in self.y_inputs]
#         super().accept()