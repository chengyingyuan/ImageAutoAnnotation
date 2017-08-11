import threading
import cv2
import logging
import json
import time
from Capture import USBCamera

CAMID = 0
CAMDIM = None
BGIMAGE_FILEPATH = "bgImage.jpg"

def main():
    loglevel = logging.DEBUG
    logdatefmt = "%Y-%m-%d %H:%M:%S"
    logfmt = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s"
    logging.basicConfig(format=logfmt, level=loglevel, datefmt=logdatefmt)
    
    cam = USBCamera(CAMID, CAMDIM)
    frame = cam.capture()
    cv2.waitKey(10)
    cv2.imwrite(BGIMAGE_FILEPATH, frame)

if __name__ == "__main__":
    main()
