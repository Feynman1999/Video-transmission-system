from threading import Thread, Lock
import cv2
import sys, os
import numpy as np 
import _global

class displayer_all(Thread):
    name = 'Deecamp'
    height = 960
    width = 1280
    def __init__(self, window_id, num, rate):
        """Constructor.
        """
        Thread.__init__(self)
        self.running = True
        self.lock = Lock()
        self.id = window_id
        self.client_num = num
        self.rate = rate
        assert self.client_num >=2 and self.client_num % 2 ==0

    def stop(self):
        self.running = False 

    def get_frame(self):
        lists = _global.get_value('1')
        ans = []
        for i in range(1, self.client_num+1, 2):
            ans.append(np.concatenate((cv2.resize(lists[i].buffer,(0,0), fx=self.rate , fy=self.rate),
                                     cv2.resize(lists[i+1].buffer,(0,0), fx=self.rate , fy=self.rate)), axis=1))
        res = ans[0]
        for i in range(1,len(ans)):
            res = np.concatenate((res, ans[i]),axis=0)
        return res
    
    def run(self):
        # 一直显示
        while self.running:
            # self.lock.acquire()
            cv2.imshow(displayer_all.name, self.get_frame())
            # self.lock.release()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                print("窗口{}退出...".format(self.name)) # 再次调用run来激活

    def __str__(self):
        return displayer_all.name

        