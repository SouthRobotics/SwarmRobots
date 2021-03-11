from location import Location
import time
import pigpio
import coms as coms
import camera as cam
from propulsion import *



robot = coms.start()
cam.start()

#pi = pigpio.pi()
ESCL = 21
ESCR = 22
SERVOL = 23
SERVOR = 24

#propulsion = Propulsion(pi, ESCL, ESCR, SERVOL, SERVOR)
while True:
    time.sleep(3)
    coms.send(robot, "hi")


#loop in one thread that constanyl sets and sends Location
#loop in another  thread that constantly recieves and sets motor speeds