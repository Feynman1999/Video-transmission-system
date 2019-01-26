from threading import Thread, Lock
import socket
import sys, os
import time
import _global

class delay_detection(Thread):
    def __init__(self, num, threshold, delay_interval):
        """
        Constructor.
        """
        Thread.__init__(self)
        self.running = True
        self.delay_interval = delay_interval #多少帧计算一次delay
        self.lock = Lock()
        self.detection_num = num
        self.threshold = threshold  #  单位: s
        tm = time.time()
        self.last_change = [0]
        self.flags = [0]
        self.refresh_frequency = [0]
        self.delay = [0]
        for i in range(1, num+1):
            self.last_change.append(tm)
            self.flags.append(1)
            self.refresh_frequency.append(0) #开始均为0次
            self.delay.append(0) #过去interval帧的总延迟
        

    def stop(self):
        self.running = False 


    def refresh_time(self, id): # 更新最新的改动时间
        assert id<=self.detection_num and id>=1
        tm =time.time()
        if tm - self.last_change[id] < self.threshold: # 有效更新
            self.refresh_frequency[id] += 1
            self.delay[id] += tm - self.last_change[id]
            if self.refresh_frequency[id] % self.delay_interval == 0 and self.refresh_frequency[id] > 0 : #更新平均延迟时间
                print("{}号过去{}帧的平均延迟为{:.2f}ms (只统计有效传输)".format(id, self.delay_interval, self.delay[id]*1000/self.delay_interval))
                self.delay[id] = 0  #重新置零
        self.lock.acquire()
        self.last_change[id] = tm  
        self.flags[id] = 1   
        self.lock.release()
        



    def run(self):
        # 一直
        while self.running:
            time.sleep(0.001)
            for i in range(1, self.detection_num+1):
                if self.flags[i] == 0 : # 已经设置
                    continue
                self.lock.acquire()
                if time.time() - self.last_change[i] > self.threshold:
                    _global.get_value('1')[i].set_cover() 
                    self.flags[i] = 0
                    print("{}号等候超时".format(i))
                self.lock.release()