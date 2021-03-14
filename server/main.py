import coms as coms
import time
import camera as cam
import cv2
import pygame
from pygame.locals import *
import math

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

#set current operating robot
current_robot = 1


#Subsystem Intilaization

factory = coms.start()
cam.work_addr = "192.168.1.137"
cam.start()
pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()

#print(pygame.joystick.get_count())
#print(controller.get_numaxes())

#Main Recive/Proccescing loop




# Main Controll Sending Loop
while True:
    #time.sleep(3)

    pygame.event.pump()
    coms.send(factory, current_robot, str(truncate((controller.get_axis(4)+1)/2, 3)) + "--" + str(truncate((controller.get_axis(5)+1)/2,3))  + "--" +  str(truncate(((controller.get_axis(0)+1)*90),3)))
    print(str(truncate((controller.get_axis(4)+1)/2, 3)) + "--" + str(truncate((controller.get_axis(5)+1)/2,3))  + "--" +  str(truncate(((controller.get_axis(0)+1)*90),3)))
    #coms.send(factory, 1)

    
            
