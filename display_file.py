from classes.graphic_object import GraphicObject

class DisplayFile:
    """
    Class containing the objects
    """
    def __init__(self):
        self.__objects_list = []
        self.__tmp_objects = []
    
    def add_object(self, g_object: GraphicObject, tmp=False) -> None:
        if tmp:
            self.__tmp_objects.append(g_object)
        else:
            self.__objects_list.append(g_object)
    
    def remove_object(self, index: int) -> GraphicObject:
        # We can't remove the axis
        obj =  self.__objects_list.pop(index)
        return obj
    
    def objects(self, tmp_included=False) -> list[GraphicObject]:
        if tmp_included:
            return self.__objects_list + self.__tmp_objects
        return self.__objects_list
