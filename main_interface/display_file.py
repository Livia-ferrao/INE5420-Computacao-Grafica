
class DisplayFile:
    def __init__(self):
        self.__objects_list = []

    def addObject(self, g_object):
        self.__objects_list.append(g_object)
    
    def removeObject(self, i):
        self.__objects_list.pop(i)
    
    # Retorna os nomes de todos os objetos do display file
    def getNames(self):
        names = []
        for obj in self.__objects_list:
            names.append(obj.name)
        return names
    
    # Dado o nome de um objeto, retorna o objeto 
    def getObject(self, name):
        for obj in self.__objects_list:
            if name == obj.name:
                return obj
        return None
    
    def updateObject(self, index, updated_object):
        self.__objects_list[index] = updated_object

    @property
    def objects_list(self):
        return self.__objects_list
    