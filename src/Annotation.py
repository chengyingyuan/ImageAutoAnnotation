import threading
import cv2
import logging
import json
import time

WINNAME = "ImageAutoAnnotation"
RECTCOLOR = (0,255,0)
RECTTHICKNESS = 2

class AnnotationThread(threading.Thread):
    def __init__(self, cam, alg, exp, heu, io, rate=12):
        threading.Thread.__init__(self)
        self._cam = cam
        #self._alg = DifferentialCollins(5, 15)
        self._alg = alg
        self._exp = exp
        self._heu = heu
        self._io = io
        self._rate = rate
        self._frames = None
        self._framelast = None
    
    def run(self):
        win = cv2.namedWindow(WINNAME)
        interval = int(1000.0 / self._rate)
        self._frames = self._cam.captureFrames(3)
        self._alg.initialize(self._frames)
        while True:
            start = int(time.time()*1000)
            frame = self._cam.capture()
            if frame is not None:
                self._frames.pop(0)
                self._framelast = frame
                self._frames.append(frame)
                data = {}
                ev = self._alg.evaluate(self._frames)
                self._exp.calculate(ev, data)
                if self._heu.isValid(ev, data):
                    rectangle = data['rectangle']
                    x1,y1,x2,y2 = rectangle
                    # TODO: Clone a new frame
                    frame = cv2.rectangle(frame, (x1,y1), (x2,y2), RECTCOLOR, RECTTHICKNESS)
                    self._io.enque(self._framelast, rectangle, self._cam.orgfile)
                cv2.imshow(WINNAME, frame)
            else:
                logging.info("No image captured")
                break
            end = int(time.time()*1000)
            delay = max(interval - (end - start), 1)
            cv2.waitKey(delay)
