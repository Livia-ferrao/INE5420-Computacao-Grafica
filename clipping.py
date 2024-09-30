from type import Type

class Clipping:
    @staticmethod
    def clip(obj, coords, window):
        if obj.tipo == Type.POINT:
            return Clipping.pointClipping(coords, window)
        elif obj.tipo == Type.LINE:
            #return Clipping.cohenSutherland(coords, window)
            return Clipping.liangBarsky(coords, window)
        elif obj.tipo == Type.WIREFRAME:
            return Clipping.sutherlandHodgeman(coords, window)
    
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
        code1 = Clipping.CSRegionCode(x1, y1, window)
        code2 = Clipping.CSRegionCode(x2, y2, window)

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
                    code1 = Clipping.CSRegionCode(x1, y1, window)
                
                else:
                    x2 = x
                    y2 = y
                    code2 = Clipping.CSRegionCode(x2, y2, window)

    @staticmethod
    def CSRegionCode(x, y, window):
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
    def liangBarsky(coords, window):
        x1 = coords[0][0]
        y1 = coords[0][1]
        x2 = coords[1][0]
        y2 = coords[1][1]

        p = [-(x2 - x1), x2 - x1, -(y2 - y1), y2 - y1]
        q = [x1 - window.xmin_scn, window.xmax_scn - x1, y1 - window.ymin_scn, window.ymax_scn - y1]

        fora_dentro = 0
        dentro_fora = 1

        for idx, pk in enumerate(p):
            if pk == 0 and q[idx] < 0:
                return (False, coords)
            elif pk < 0:
                r = q[idx]/pk
                fora_dentro = max(fora_dentro, r)
            elif pk > 0:
                r = q[idx]/pk
                dentro_fora = min(dentro_fora, r)

        if fora_dentro > dentro_fora:
            return (False, coords)
        
        new_x1 = x1 + fora_dentro*(x2-x1)
        new_y1 = y1 + fora_dentro*(y2-y1)
        new_x2 = x1 + dentro_fora*(x2-x1)
        new_y2 = y1 + dentro_fora*(y2-y1)
        print(new_x1, new_y1, new_x2, new_y2)
        return (True, [[new_x1, new_y1], [new_x2, new_y2]])
    
    @staticmethod
    def sutherlandHodgeman(coords, window):
        clipping_window = [[window.xmin_scn, window.ymin_scn],
                       [window.xmin_scn, window.ymax_scn],
                       [window.xmax_scn, window.ymax_scn],
                       [window.xmax_scn, window.ymin_scn]]

        clipped_coords = coords

        for i in range(len(clipping_window)):
            previous_coords = clipped_coords
            clipped_coords = []

            window_edge1 = clipping_window[i]
            window_edge2 = clipping_window[(i+1)%len(clipping_window)]

            for j in range(len(previous_coords)):
                current_point = previous_coords[j]
                next_point = previous_coords[(j+1)%len(previous_coords)]

                current_inside = Clipping.SHInside(current_point, window_edge1, window_edge2)
                next_inside = Clipping.SHInside(next_point, window_edge1, window_edge2)

                if next_inside:
                    if not current_inside:
                        clipped_coords.append(Clipping.SHIntersection(current_point, next_point, window_edge1, window_edge2))
                    clipped_coords.append(next_point)

                elif current_inside:
                    clipped_coords.append(Clipping.SHIntersection(current_point, next_point, window_edge1, window_edge2))

        if len(clipped_coords) == 0:
            return (False, coords)
        else:
            return (True, clipped_coords)
    
    @staticmethod
    def SHInside(point, edge1, edge2):
            return ((edge2[0]-edge1[0]) * (point[1]-edge1[1])) < ((edge2[1]-edge1[1]) * (point[0]-edge1[0]))

    @staticmethod
    def SHIntersection(point1, point2, edge1, edge2):
        numx = (edge1[0]*edge2[1] - edge1[1]*edge2[0])*(point1[0]-point2[0]) - (edge1[0]-edge2[0])*(point1[0]*point2[1]-point1[1]*point2[0])
        den = (edge1[0]-edge2[0])*(point1[1]-point2[1]) - (edge1[1]-edge2[1])*(point1[0]-point2[0])
        numy = (edge1[0]*edge2[1] - edge1[1]*edge2[0])*(point1[1]-point2[1]) - (edge1[1]-edge2[1])*(point1[0]*point2[1]-point1[1]*point2[0])
        return (numx/den, numy/den)