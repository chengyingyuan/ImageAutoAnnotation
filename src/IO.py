import cv2
import queue
import time
import threading

FSIO_INTERVAL = 0.1

class DummyIOThread(threading.Thread):
    def __init__(self, fileprefix, cropsuffix='_crop', saveorg=False):
        super().__init__()
        self._fileprefix = fileprefix
        self._cropsuffix = cropsuffix
        self._saveorg = saveorg
        self._queue = queue.Queue()
        self._giveup = False

    @property
    def giveup(self):
        return self._giveup
    
    @giveup.setter
    def giveup(self, value):
        self._giveup = value
    
    def enque(self, frame, rectangle, orgfile=None):
        pass
    
    def save(self, all=True):
        return 0

    def run(self):
        while not self.giveup:
            nfiles = self.save()
            if nfiles > 0:
                continue
            time.sleep(FSIO_INTERVAL)

class FSIOThread(threading.Thread):
    def __init__(self, fileprefix=None, cropsuffix='_crop', saveorg=False):
        super().__init__()
        self._fileprefix = fileprefix
        self._cropsuffix = cropsuffix
        self._saveorg = saveorg
        self._queue = queue.Queue()
        self._giveup = False

    @property
    def giveup(self):
        return self._giveup
    
    @giveup.setter
    def giveup(self, value):
        self._giveup = value
    
    def enque(self, frame, rectangle, orgfile=None):
        self._queue.put((time.time(), frame, rectangle, orgfile))
    
    def save(self, all=True):
        nfiles = 0
        while not self._queue.empty():
            ts, frame, rect, orgfile = self._queue.get_nowait()
            x1,y1,x2,y2 = rect
            if orgfile is None: # Auto generate original file
                fid = int(ts*1000)
                orgfile = "{}{}.jpg".format(self._fileprefix, fid)
            cropsuffix = self._cropsuffix
            pos = "{}x{}x{}x{}".format(x1,y1,x2,y2)
            cropfile = "{}{}{}.jpg".format(orgfile, cropsuffix, pos)
            croppedframe = frame[y1:y2, x1:x2]
            cv2.imwrite(cropfile, croppedframe)
            if self._saveorg:
                cv2.imwrite(orgfile, frame)
            nfiles += 1
            if not all:
                break
        return nfiles

    def run(self):
        while not self.giveup:
            nfiles = self.save()
            if nfiles > 0:
                continue
            time.sleep(FSIO_INTERVAL)
