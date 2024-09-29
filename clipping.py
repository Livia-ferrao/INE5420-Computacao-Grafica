from type import Type

class Clipping:
    @staticmethod
    def clip(obj, coords, window):
        if obj.tipo == Type.POINT:
            return Clipping.pointClipping(coords, window)
        elif obj.tipo == Type.LINE:
            return Clipping.cohenSutherland(coords, window)
        elif obj.tipo == Type.WIREFRAME:
            return Clipping.poligono(coords, window)
    
    @staticmethod
    def pointClipping(coords, window):
        if window.xmin_scn <= coords[0][0] <= window.xmax_scn and window.ymin_scn <= coords[0][1] <= window.ymax_scn:
            return (True, coords)
        else:
            return (False, coords)
    
    @staticmethod
    def cohenSutherland(coords, window):
        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]
        code1 = Clipping.regionCode(x1, y1, window)
        code2 = Clipping.regionCode(x2, y2, window)

        while True:
            if code1 == code2 == 0b0000:
                return (True, [[x1, y1], [x2, y2]])
            elif (code1 & code2) != 0b0000:
                return (False, coords)
            else:
                if code1 != 0b0000:
                    out = code1
                else:
                    out = code2
                if out & 0b0001: # Esquerda
                    m = (y2 - y1)/(x2 - x1)
                    x = window.xmin_scn
                    y = m * (x - x1) + y1
                elif out & 0b0010: # Direita
                    m = (y2 - y1)/(x2 - x1)
                    x = window.xmax_scn
                    y = m * (x - x1) + y1
                elif out & 0b0100: # Baixo
                    m = (x2 - x1)/(y2 - y1)
                    y = window.ymin_scn
                    x = x1 + m * (y - y1)
                elif out & 0b1000: # Cima
                    m = (x2 - x1)/(y2 - y1)
                    y = window.ymax_scn
                    x = x1 + m * (y - y1)
                
                if out == code1:
                    x1 = x
                    y1 = y
                    code1 = Clipping.regionCode(x1, y1, window)
                
                else:
                    x2 = x
                    y2 = y
                    code2 = Clipping.regionCode(x2, y2, window)

    @staticmethod
    def regionCode(x, y, window):
        code = 0b0000
        if x < window.xmin_scn:
            code |= 0b0001
        elif x > window.xmax_scn:
            code |= 0b0010
        if y < window.ymin_scn:
            code |= 0b0100
        elif y > window.ymax_scn:
            code |= 0b1000
        return code
    
    @staticmethod
    def poligono(coords, window):
        return (True, coords)