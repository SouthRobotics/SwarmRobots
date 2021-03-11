import coms as coms
import time
import camera as cam
import cv2





#Subsystem Intilaization

factory = coms.start()
cam.start()
cam.work_addr = "10.0.0.21"


while True:
    time.sleep(3)
    coms.send(factory, 1)
    try:
        cv2.imshow('frame', cam.img)
    except:
        pass
    
                