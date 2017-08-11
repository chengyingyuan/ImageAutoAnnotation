import time

class SequenceHeuristic(object):
    def __init__(self, minChanges, minDuration, noMotionDelay):
        self._minChanges = minChanges
        self._minDuration = minDuration
        self._noMotionDelay = noMotionDelay
        self._duration = 0
    
    def isValid(self, image, data):
        numOfChanges = data['numOfChanges']
        if numOfChanges >= self._minChanges:
            self._duration += 1
            if self._duration >= self._minDuration:
                return True
        else:
            if self._duration > 0: # No sleep if duration is in effect
                self._duration -= 1
            else:
                if self._noMotionDelay:
                    time.sleep(self._noMotionDelay/1000.0)
        return False
