import gpsd
import time
import pigpio
import coms as coms
import camera as cam
from propulsion import *

BASE_IP = "192.168.1.190"

robot = coms.start(BASE_IP)
cam.start(BASE_IP)
gpsd.connect()
time.sleep(3)



pi = pigpio.pi()
ESCL = 21
ESCR = 22
SERVOL = 23
SERVOR = 24

propulsion = Propulsion(pi, ESCL, ESCR, SERVOL, SERVOR)


while True:
    packet = gpsd.get_current()
    print(packet.position())
    if "0" in robot.robot.keys():
        print(robot.robot["0"].robotObj.mode)
    coms.send(robot, packet.position())


#loop in one thread that constanyl sets and sends Location
#loop in another  thread that constantly recieves and sets motor speeds