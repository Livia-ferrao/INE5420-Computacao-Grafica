import numpy as np
from configurations import Configurations

class Window:
    def __init__(self):
        self._viewport = None
        
        self.translating_matrix = self.create_translating_matrix(0, 0)
        self.scaling_matrix = self.create_scaling_matrix(1, 1)
        self.transform_matrix()

        self.xw_min = -1000
        self.xw_max = 1000
        self.yw_min = -1000
        self.yw_max = 1000

        self.x_center = 0
        self.y_center = 0
        self.x_min = self.xw_min
        self.x_max = self.xw_max
        self.y_min = self.yw_min
        self.y_max = self.yw_max
        self.current_scale = 1
    
    def create_translating_matrix(self, x, y):
        return [[1, 0, 0],
                [0, 1, 0],
                [x, y, 1]]
    
    def create_scaling_matrix(self, x, y):
        return [[x, 0, 0],
                [0, y, 0],
                [0, 0, 1]]
    
    def transform_matrix(self):
        t_np = np.array(self.translating_matrix)
        s_np = np.array(self.scaling_matrix)
        result = np.matmul(t_np, s_np)
        print("translating", t_np)
        print("scaling", s_np)
        self.transforming_matrix = result.tolist()

    def set_viewport(self, viewport):
        self._viewport = viewport

    def move_left(self, scale):
        d = (self.x_max - self.x_min) * (scale/100)
        self.x_center += d
        self.translating_matrix = self.create_translating_matrix(self.x_center, self.y_center)
        self.transform_matrix()
    
    def move_right(self, scale):
        d = (self.x_max - self.x_min) * (scale/100)
        print('d', d)
        print('xmin', self.x_min)
        print('xmax', self.x_max)
        self.x_center -= d
        print(self.x_center)
        self.translating_matrix = self.create_translating_matrix(self.x_center, self.y_center)
        self.transform_matrix()
    
    def move_up(self, scale):
        d = (self.y_max - self.y_min) * (scale/100)
        self.y_center -= d
        self.translating_matrix = self.create_translating_matrix(self.x_center, self.y_center)
        self.transform_matrix()
    
    def move_down(self, scale):
        d = (self.y_max - self.y_min) * (scale/100)
        self.y_center += d
        self.translating_matrix = self.create_translating_matrix(self.x_center, self.y_center)
        self.transform_matrix()

    def getCenter(self):
        x = (self.x_max+self.x_min)/2
        y = (self.y_max+self.y_min)/2
        return (x, y)
    
    def zoom_in(self, scale):
        scale = scale/100
        x = ((self.x_max - self.x_min) * scale)/2
        y = ((self.y_max - self.y_min) * scale)/2

        print("antes", self.x_min, self.x_max)
        print("x", x)
        print("y", y)
        self.x_min += x
        self.x_max -= x
        self.y_min += y
        self.y_max -= y
        # self.current_scale *= 1+scale
        # print(self.current_scale)
        print("depois", self.x_min, self.x_max)

        sx = 2000/(self.x_max-self.x_min)
        sy = 2000/(self.y_max-self.y_min)
        print(sx, sy)
        self.scaling_matrix = self.create_scaling_matrix(sx, sy)
        self.transform_matrix()

    def zoom_out(self, scale):
        scale = scale/100
        x = ((self.x_max - self.x_min) * scale)/2
        y = ((self.y_max - self.y_min) * scale)/2
        print("antes", self.x_min, self.x_max)
        print("x", x)
        print("y", y)
        self.x_min -= x
        self.x_max += x
        self.y_min -= y
        self.y_max += y

        #self.current_scale *= 1/(1+scale)
        #print(self.current_scale)
        print("depois", self.x_min, self.x_max)
        
        sx = 2000/(self.x_max-self.x_min)
        sy = 2000/(self.y_max-self.y_min)
        print(sx, sy)
        self.scaling_matrix = self.create_scaling_matrix(sx, sy)
        self.transform_matrix()
