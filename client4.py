import socket
import time
from init import *
from camera import *


address_dict = get_addresses()
server_address = (address_dict['server']['host'],int(address_dict['server']['port']))


buffersize = 65507
jpeg_quality = 80
ID_length = 10

if __name__ == '__main__':
    grabber1 = VideoGrabber(jpeg_quality,0)
    grabber1.setDaemon(True)
    grabber1.start()

    running = True

    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # sk.bind(client_address)
    tot_frame = 0
    time_sta = time.time()
    ID = os.path.basename(sys.argv[0]).split(".")[0] #ID是文件名
    ID = ID[-1].zfill(ID_length).encode(encoding='utf-8') # 只适用于个位数

    while(running):
        
        time.sleep(0.01)
        buffer = grabber1.get_buffer()
        if buffer is None:
            continue
    
        if len(buffer) > 65507:
            print("The message is too large to be sent within a single UDP datagram. We do not handle splitting the message in multiple datagrams")
            sk.sendto(ID+b"FAIL",server_address)
            continue
            
        sk.sendto(ID+buffer.tobytes(), server_address)
        tot_frame +=1
        if tot_frame % 10000 ==0 :
            print("{:.2f}fps".format(tot_frame/(time.time()-time_sta)))
            break

    print("Quitting..")
    sk.sendto(ID+b"FAIL",server_address)
    print("已发送失败消息")
    grabber1.stop()
    grabber1.join()
    sk.close()

