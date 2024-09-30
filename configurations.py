
class Configurations:

    # Largura da main_window
    @staticmethod
    def window_X():
        return 850
    
    # Altura da main_window
    @staticmethod
    def window_Y():
        return 600
    
    # Geometria do frame de ferramentas
    @staticmethod
    def tool_frame():
        return (10, 10, 300, 580)

    # Geometria do frame de visualização
    @staticmethod
    def view_frame():
        return (320, 10, 520, 580)
    
    # Geometria da 
    @staticmethod
    def view_area():
        return (10, 10, 500, 500)
    
    # Geometria da viewport
    @staticmethod
    def viewport():
        return (10, 10, 480, 480)

    # Geometria do frame de objetos
    @staticmethod
    def objects_frame():
        return (10, 30, 280, 165)
    
    # Geometria do frame de controle
    @staticmethod
    def control_frame():
        return (10, 225, 280, 165)
    
    # Geometria do frame de gerência de arquivos
    @staticmethod
    def files_frame():
        return (10, 420, 280, 60)
    
    # Geometria do frame de escolher método de clipping de linhas
    @staticmethod
    def clipping_frame():
        return (10, 510, 280, 60)
    
    # Menor coordenada possível para x ou y do objeto
    @staticmethod
    def min_coord():
        return -1000000000
    
    # Maior coordenada possível para x ou y do objeto
    @staticmethod
    def max_coord():
        return 1000000000
    
    # x max inicial da window
    @staticmethod
    def windowXmax():
        return 1000
    
    # x min inicial da window
    @staticmethod
    def windowXmin():
        return -1000
    
    # y max inicial da window
    @staticmethod
    def windowYmax():
        return 1000
    
    # y min inicial da window
    @staticmethod
    def windowYmin():
        return -1000

    # x min da viewport
    @staticmethod
    def viewportXmin():
        return Configurations.viewport()[0]

    # x max da viewport
    @staticmethod
    def viewportXmax():
        return Configurations.viewport()[0] + Configurations.viewport()[2]

    # y min da viewport
    @staticmethod
    def viewportYmin():
        return Configurations.viewport()[1]

    # y max da viewport
    @staticmethod
    def viewportYmax():
        return Configurations.viewport()[1] + Configurations.viewport()[3]
