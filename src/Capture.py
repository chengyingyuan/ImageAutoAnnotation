import logging
import glob
import sys, os
import cv2


CAPTURE_DELAY = 50 # 1000/50 = 20fps

class USBCamera(object):
    def __init__(self, camid=0, camdim=None):
        self._camid = camid
        self._camdim = camdim
        self._cam = cv2.VideoCapture(self._camid)
        if self._camdim:
            width, height = self._camdim
            if not self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, width):
                logging.warn("Failed set frame width to {}".format(width))
            if not self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height):
                logging.warn("Failed set frame height to {}".format(height))
        width = self._cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self._cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self._dim = (width, height)
        logging.info("Camera {} dimension: {}".format(self._camid, self._dim))
    
    @property
    def dimension(self):
        return self._dim

    @property
    def orgfile(self):
        return None
    
    def capture(self):
        flag, frame = self._cam.read()
        if not flag:
            frame = None
        return frame
    
    def captureFrames(self, nFrames, delay=CAPTURE_DELAY):
        frames = []
        while len(frames) < nFrames:
            frames.append(self.capture())
            cv2.waitKey(delay)
        return frames

class FSCamera(object):
    def __init__(self, dpath, ext='*.jpg'):
        self._dpath = dpath
        files = glob.glob(os.path.join(dpath, ext))
        files.sort()
        #self._files = [file.replace('\\', '/') for file in files]
        self._files = files
        self._nfiles = len(self._files)
        i = cv2.imread(self._files[0])
        width, height = len(i[0]),len(i)
        self._dim = (width, height)
        self._index = -1
        logging.info("FSCamera {} files {} dimension {}".format(dpath,len(files),self._dim))

    @property
    def dimension(self):
        return self._dim
    
    @property
    def orgfile(self):
        if self._index >= self._nfiles:
            return None
        return self._files[self._index]
    
    def capture(self):
        self._index += 1
        if self._index >= self._nfiles:
            return None
        frame = cv2.imread(self._files[self._index])
        return frame
    
    def captureFrames(self, nFrames, delay=CAPTURE_DELAY):
        frames = []
        while len(frames) < nFrames:
            frames.append(self.capture())
            cv2.waitKey(delay)
        return frames
