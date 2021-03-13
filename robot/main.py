import gpsd
import time
import pigpio
import coms as coms
import camera as cam
from propulsion import *
import threading

BASE_IP = "192.168.1.190"

robot = coms.start(BASE_IP)
cam.start(BASE_IP)
gpsd.connect()
time.sleep(3)



pi = pigpio.pi()
ESCL = 13
ESCR = 19
SERVOL = 5
SERVOR = 12

propulsion = Propulsion(pi, ESCL, ESCR, SERVOL, SERVOR)

def sendLoop():
    global successful
    while True:
        packet = gpsd.get_current()

        print(packet.position())
        if coms.RobotObj(robot):
            print(coms.RobotObj(robot).mode)
        coms.send(robot, packet.position())

t = threading.Thread(target=sendLoop, args=(False,))
t.start()

#loop in one thread that constanyl sets and sends Location
#loop in another  thread that constantly recieves and sets motor speeds