import threading
import logging
import time
from Capture import USBCamera,FSCamera
from Algorithm import DifferentialBackground
from Expositor import RectangleExpositor
from Heuristic import SequenceHeuristic
from IO import FSIOThread, DummyIOThread
from Annotation import AnnotationThread

FSPATH = 'F:\\BaiduYunDownload\\droneimages\\ZiZu550FourAxisII'
FSEXT = '*.JPG'

def main():
    loglevel = logging.DEBUG
    logdatefmt = "%Y-%m-%d %H:%M:%S"
    logfmt = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s"
    logging.basicConfig(format=logfmt, level=loglevel, datefmt=logdatefmt)
    
    #cam = FSCamera(FSPATH, FSEXT)
    #cam = USBCamera(camid=1, camdim=(1024,768))
    cam = USBCamera(camid=0)
    #alg = DifferentialCollins(5, 15)
    alg = DifferentialBackground(5, 15)
    exp = RectangleExpositor(0, 0, *cam.dimension)
    heu = SequenceHeuristic(20, 2, 0)
    #ioThread = DummyIOThread(fileprefix="F:\\tmp")
    ioThread = FSIOThread()
    annThread = AnnotationThread(cam, alg, exp, heu, ioThread, rate=5)
    """camThread.start()
    while camThread.isAlive():
        time.sleep(0.5)
    """
    try:
        ioThread.start()
        annThread.run()
    except KeyboardInterrupt:
        logging.info("Bye")
    ioThread.giveup = True
    ioThread.join()

if __name__ == "__main__":
    main()
