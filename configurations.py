
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
        return (0, 0, Configurations.view_frame()[2], Configurations.view_frame()[3])

    @staticmethod
    def objects_frame():
        return (10, 10, 280, 175)
    
    @staticmethod
    def control_frame():
        return (10, 195, 280, 175)
    
    @staticmethod
    def min_coord():
        return -1000000000
    
    @staticmethod
    def max_coord():
        return 1000000000