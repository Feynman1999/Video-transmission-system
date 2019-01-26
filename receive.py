from threading import Thread, Lock
import socket
import sys, os

class packet_receive(Thread):
    def __init__(self, window_id):
        """Constructor.
        """
        Thread.__init__(self)
        self.running = True
        self.lock = Lock()
        self.id = window_id

    def stop(self):
        self.running = False 

    def run(self):
        # 一直显示
        while self.running:
            data, client = sk.recvfrom(buffersize)
            