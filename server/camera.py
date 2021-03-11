from __future__ import division
import cv2
import numpy as np
import socket
import struct
import threading

img = None
work_addr = "10.0.0.21"
MAX_DGRAM = 2**16

def dump_buffer(s):

    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            break

def _start():
    global successful
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 9656))
    dat = b''
    dump_buffer(s)

    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(str(addr))
        if str(addr) == work_addr:
            if struct.unpack("B", seg[0:1])[0] > 1:
                dat += seg[1:]
            else:
                dat += seg[1:]
                img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
                cv2.imshow('frame', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                dat = b''

    # cap.release()
    cv2.destroyAllWindows()
    s.close()

def start():
    t = threading.Thread(target = _start)
    t.start()
    