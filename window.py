import numpy as np
from configurations import Configurations

class Window:
    def __init__(self):
        # X e Y max e min da window
        self.__xw_min = Configurations.windowXmin()
        self.__xw_max = Configurations.windowXmax()
        self.__yw_min = Configurations.windowYmin()
        self.__yw_max = Configurations.windowYmax()

    # Movimentação para esquerda
    def moveLeft(self, scale):
        d = (self.__xw_max - self.__xw_min) * (scale/100)
        self.__xw_max -= d
        self.__xw_min -= d

    # Movimentação para direita
    def moveRight(self, scale):
        d = (self.__xw_max - self.__xw_min) * (scale/100)
        self.__xw_max += d
        self.__xw_min += d

    # Movimentação para cima
    def moveUp(self, scale):
        d = (self.__yw_max - self.__yw_min) * (scale/100)
        self.__yw_max += d
        self.__yw_min += d

    # Movimentação para baixo
    def moveDown(self, scale):
        d = (self.__yw_max - self.__yw_min) * (scale/100)
        self.__yw_max -= d
        self.__yw_min -= d

    # Zoom in
    def zoomIn(self, scale):
        scale = scale/100
        dx = ((self.__xw_max - self.__xw_min) * scale)/2
        dy = ((self.__yw_max - self.__yw_min) * scale)/2

        self.__xw_min += dx
        self.__xw_max -= dx
        self.__yw_min += dy
        self.__yw_max -= dy

    # Zoom out
    def zoomOut(self, scale):
        scale = scale/100
        dx = ((self.__xw_max - self.__xw_min) * scale)/2
        dy = ((self.__yw_max - self.__yw_min) * scale)/2

        self.__xw_min -= dx
        self.__xw_max += dx
        self.__yw_min -= dy
        self.__yw_max += dy

    @property
    def xw_min(self):
        return self.__xw_min
    
    @property
    def xw_max(self):
        return self.__xw_max
    
    @property
    def yw_min(self):
        return self.__yw_min
    
    @property
    def yw_max(self):
        return self.__yw_max