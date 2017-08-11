import cv2

class RectangleExpositor(object):
    def __init__(self, x1, y1, x2, y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
    
    def calculate(self, image, data):
        self.calculate2(image, data)
    
    def calculate2(self, image, data):
        maxx = len(image[0])
        maxy = len(image)
        rx1 = maxx
        ry1 = maxy
        rx2 = 0
        ry2 = 0
        numOfChanges = 0
        anz = cv2.findNonZero(image)
        if anz is not None:
            numOfChanges = len(anz)
            anz = anz.reshape((-1,2))
            anzx = anz[:,0]
            anzy = anz[:,1]
            rx1,rx2,_rx1loc,_rx2loc = cv2.minMaxLoc(anzx)
            ry1,ry2,_ry1loc,_ry2loc = cv2.minMaxLoc(anzy)
        data['rectangle'] = (int(rx1),int(ry1),int(rx2),int(ry2))
        data['numOfChanges'] = numOfChanges

    def calculate1(self, image, data):
        maxx = len(image[0])
        maxy = len(image)
        rx1 = maxx
        ry1 = maxy
        rx2 = 0
        ry2 = 0
        x = self._x1
        numOfChanges = 0
        while x < self._x2:
            y = self._y1
            while y < self._y2:
                v = image[y][x]
                if v != 255:
                    y += 1
                    continue
                numOfChanges += 1
                if rx1 > x:
                    rx1 = x
                if rx2 < x:
                    rx2 = x
                if ry1 > y:
                    ry1 = y
                if ry2 < y:
                    ry2 = y
                y += 1
            x += 1
        if rx1-10 > 0:
            rx1 -= 10
        if ry1-10 > 0:
            ry1 -= 10
        if rx2+10 < maxx-1:
            rx2 += 10
        if ry2+10 < maxy-1:
            ry2 += 10
        data['rectangle'] = (rx1,ry1,rx2,ry2)
        data['numOfChanges'] = numOfChanges
