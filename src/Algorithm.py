import cv2
import time

class DifferentialCollins(object):
    def __init__(self, erode, thresh):
        self._erode = erode
        self._thresh = thresh
        erodeSize = (erode, erode)
        self._erodeKernel = cv2.getStructuringElement(cv2.MORPH_RECT, erodeSize)
    
    def initialize(self, images):
        for i,image in enumerate(images):
            images[i] = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    def evaluate(self, images):
        images[2] = cv2.cvtColor(images[2], cv2.COLOR_RGB2GRAY)
        d1 = cv2.absdiff(images[0], images[2])
        d2 = cv2.absdiff(images[1], images[2])
        ev = cv2.bitwise_and(d1, d2)
        rv, ev = cv2.threshold(ev, self._thresh, 255, cv2.THRESH_BINARY)
        ev = cv2.erode(ev, self._erodeKernel)
        return ev

class DifferentialBackground(object):
    def __init__(self, erode, thresh, bgpath=None):
        self._bgpath = bgpath
        self._erode = erode
        self._thresh = thresh
        erodeSize = (erode, erode)
        self._erodeKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, erodeSize)
        self._bgImage = None
        self._mog = None
    
    def initialize(self, images):
        self._mog = cv2.createBackgroundSubtractorMOG2()
        if self._bgpath:
            bgImage = cv2.imread(self._bgpath)
            self._mog.apply(bgImage)
        for image in images:
            self._mog.apply(image)
        #cv2.imshow("test", bgImage)
        #time.sleep(2)
        #self._bgImage = cv2.cvtColor(bgImage, cv2.COLOR_BGR2GRAY)
        #self._bgImage = cv2.GaussianBlur(self._bgImage, (21,21), 0)
    
    def evaluate(self, images):
        #images[2] = cv2.cvtColor(images[2], cv2.COLOR_BGR2GRAY)
        #images[2] = cv2.GaussianBlur(images[2], (21,21), 0)
        #differ = cv2.absdiff(images[2], self._bgImage)
        differ = self._mog.apply(images[2])
        #time.sleep(2)
        ev = cv2.morphologyEx(differ, cv2.MORPH_OPEN, self._erodeKernel)
        cv2.imshow("test", ev)
        #rv, ev = cv2.threshold(differ, 25, 255, cv2.THRESH_BINARY)
        #ev = cv2.dilate(ev, None, iterations=2)
        #ev = cv2.erode(ev, self._erodeKernel)
        return ev
