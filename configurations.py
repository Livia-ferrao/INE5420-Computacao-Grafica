
class Configurations:

    # Valores iniciais da Window
    @staticmethod
    def window_X():
        return 900
    
    @staticmethod
    def window_Y():
        return 600
    
    @staticmethod
    def tool_frame():
        return (10, 10, 300, 580)

    @staticmethod
    def view_frame():
        return (320, 10, 570, 580)
    
    @staticmethod
    def viewport():
        return (10, 30, 550, 540)

    @staticmethod
    def objects_frame():
        return (10, 30, 280, 165)
    
    @staticmethod
    def control_frame():
        return (10, 225, 280, 165)
    
    @staticmethod
    def min_coord():
        return -1000000000
    
    @staticmethod
    def max_coord():
        return 1000000000
    
    @staticmethod
    def windowXmax():
        return 1000
    
    @staticmethod
    def windowXmin():
        return -1000
    
    @staticmethod
    def windowYmax():
        return 1000
    
    @staticmethod
    def windowYmin():
        return -1000

    # ViewPort
    @staticmethod
    def viewportXmin():
        return Configurations.viewport()[0]

    @staticmethod
    def viewportXmax():
        return Configurations.viewport()[0] + Configurations.viewport()[2]

    @staticmethod
    def viewportYmin():
        return Configurations.viewport()[1]

    @staticmethod
    def viewportYmax():
        return Configurations.viewport()[1] + Configurations.viewport()[3]
