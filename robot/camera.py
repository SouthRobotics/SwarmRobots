from __future__ import division
import cv2
import numpy as np
import socket
import struct
import math
import threading
from picamera.array import PiRGBArray
from picamera import PiCamera

class FrameSegment(object):
    """ 
    Object to break down image frame segment
    if the size of image exceed maximum datagram size 
    """
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64 # extract 64 bytes in case UDP frame overflown
    def __init__(self, sock, port, addr="127.0.0.1"):
        self.s = sock
        self.port = port
        self.addr = addr

    def udp_frame(self, img):
        """ 
        Compress image and Break down
        into data segments 
        """
        compress_img = cv2.imencode('.jpg', img)[1]
        dat = compress_img.tostring()
        size = len(dat)
        count = math.ceil(size/(self.MAX_IMAGE_DGRAM))
        array_pos_start = 0
        while count:
            array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(struct.pack("B", count) +
                dat[array_pos_start:array_pos_end], 
                (self.addr, self.port)
                )
            array_pos_start = array_pos_end
            count -= 1


def _start():
    """ Top level main function """
    # Set up UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 9656

    camera = PiCamera()
    camera.resolution = (1920, 1080)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(1920, 1080))
    #camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)
    camera.capture(rawCapture, format="bgr", use_video_port=True)

    fs = FrameSegment(s, port)

    
    while (True):
        cap = rawCapture.array
        fs.udp_frame(cap)

    cap.release()
    cv2.destroyAllWindows()
    s.close()

def start():
    t = threading.Thread(target = _start)
    t.start()