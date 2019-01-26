from threading import Thread, Lock
import cv2
import sys, os
import numpy as np 

class Videodisplay(Thread):
    """ 
        A threaded video display
    """
    in_same_flag = False
    def __init__(self, window_id):
        """Constructor.
        """
        Thread.__init__(self)
        self.running = True
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.lock = Lock()
        self.id = window_id
        self.set_cover()

    def stop(self):
        self.running = False 
    
    def set_buffer(self, raw_data):
        array = np.frombuffer(raw_data, dtype=np.uint8)
        img = cv2.imdecode(array, 1)   
        self.lock.acquire()
        self.buffer = img        
        self.lock.release()

    # def set_error_cover(self):
    #     self.lock.acquire()
    #     cv2.putText(self.buffer, 'error', (50, 255), self.font, 3, (255, 255, 0), 2)
    #     self.lock.release()

    def set_cover(self):
        self.lock.acquire()
        self.buffer = cv2.imread(os.path.join(sys.path[0],'cover.png') ,cv2.IMREAD_COLOR)
        self.lock.release()

    def run(self):
        # 一直显示
        while self.running:
            self.lock.acquire()
            cv2.imshow(str(self.id), self.buffer)
            self.lock.release()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                print("窗口{}退出...".format(self.id)) # 再次调用run来激活

    def __str__(self):
        return str(self.id)

        