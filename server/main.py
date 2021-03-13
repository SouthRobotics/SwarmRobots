import coms as coms
import time
import camera as cam
import cv2





#Subsystem Intilaization

factory = coms.start()
cam.work_addr = "192.168.1.137"
cam.start()



while True:
    time.sleep(3)
    #coms.send(factory, 1)

    
                