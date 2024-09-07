
class DisplayFile:
    """
    Class containing the objects
    """
    def __init__(self):
        self.objects_list = []

    def add_object(self, g_object):
        self.objects_list.append(g_object)
    
    def remove_object(self, i):
        self.objects_list.pop(i)
    