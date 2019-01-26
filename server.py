import _global
import socket
import time 
from init import *
from display import *
from receive import *
from detection import *
from dis_all import *

_global._init()

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address_dict = get_addresses()
server_address = (address_dict['server']['host'],int(address_dict['server']['port']))
sk.bind(server_address)

buffersize = 65507
client_num = 4
threshold = 0.2
ID_length = 10
delay_interval = 30

if __name__ == '__main__':
    displayers = [0]
    for i in range(1, client_num+1):
        displayers.append(Videodisplay(i))
        displayers[i].setDaemon(True)
        if Videodisplay.in_same_flag :
            displayers[i].running = False
        displayers[i].start()

    _global.set_value('1', displayers) # 跨文件传输
    if Videodisplay.in_same_flag :
        displayer_all1 = displayer_all(0, client_num, 0.8)
        displayer_all1.setDaemon(True)
        displayer_all1.start()

    detection_1 = delay_detection(client_num, threshold, delay_interval)
    detection_1.setDaemon(True)
    detection_1.start()

    while(True):
        data, client = sk.recvfrom(buffersize)
        ID = int(data[0:ID_length].decode(encoding='utf-8'))
        assert ID>=1 and ID <=client_num
        # print(ID)
        if data[ID_length:] == b"FAIL":
            displayers[ID].set_cover() 
        elif data[ID_length:] == b"STOP":
            displayers[ID].set_cover()
        else:
            displayers[ID].set_buffer(data[ID_length:])
            detection_1.refresh_time(ID)
            # if displayers[ID].running == False:
            #     displayers[ID].running = True
            #     displayers[ID].run()

    print("The server is quitting. ")

    for i in range(1, client_num+1):
        displayers[i].stop()
        displayers[i].join()

    detection_1.stop()
    detection_1.join()

    if Videodisplay.in_same_flag :
        displayer_all1.stop()
        displayer_all1.join()
    sk.close()


