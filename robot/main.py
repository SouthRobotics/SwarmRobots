import gpsd
import time
import pigpio
import coms as coms
import camera as cam
from propulsion import *
import threading
import math
import gyro as gyro

def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper



BASE_IP = "192.168.1.190"

factory = coms.start(BASE_IP)
cam.start(BASE_IP)
gpsd.connect()
time.sleep(3)



pi = pigpio.pi()
ESCL = 13
ESCR = 19
SERVOL = 5
SERVOR = 12

propulsion = Propulsion(pi, ESCL, ESCR, SERVOL, SERVOR)

icm20948=gyro.ICM20948()

#Main coordinate sending loop
def sendLoop():
    global successful
    while True:
        packet = gpsd.get_current()
        time.sleep(1)
        #print(packet.position())

        #if coms.RobotObj(robot):
        #    print(coms.RobotObj(robot).mode)
        
        #coms.send(factory, str(truncate(packet.lat, 5)) +"--"+ str(truncate(packet.lon, 5)) +"--"+ str(truncate(packet.speed(), 5)))hspeed
        print(str(truncate(packet.lat, 7)) +"--"+ str(truncate(packet.lon, 7)) +"--"+ str(truncate(packet.speed(), 7))+"--"+ str(truncate(gyro.update(icm20948), 2)), flush=True)

#Main Control Loop
def controlLoop():
    global successful
    while True:
        if coms.RobotObj(factory) is not None:
            print(coms.RobotObj(factory).motorRSpeed, flush=True)
            print(coms.RobotObj(factory).motorLSpeed, flush=True)
            print(coms.RobotObj(factory).motorAngle, flush=True)




t2 = threading.Thread(target=controlLoop)
t2.start()
t1 = threading.Thread(target=sendLoop)
t1.start()

#loop in one thread that constanyl sets and sends Location
#loop in another  thread that constantly recieves and sets motor speeds