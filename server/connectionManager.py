import server.byteConverter as _byteConverter
#from raspi_lora import LoRa, ModemConfig
from server.lora import LoRa


class Robot:

    def __init__(self, _robotID):
        self.robotmode = 0 #0-> coord based 1-> direct motor control
        self.coordlat = 0
        self.coordlon = 0
        self.Gocoordlat = 0
        self.Gocoordlon = 0
        self.motorRpos = 90 #0-180
        self.motorRspeed = 0 #0-1
        self.motorLpos = 90 #0-180
        self.motorLspeed = 0 #0-1
        self.robotID = _robotID

 
"""example code to connect to module and send/recieve
lora = LoRa(serial_port, timeout, timeout, debug)

    lora.send(tx_data)

    lora.recv_mode()

    rx_data = lora.recv()

    print(rx_str)
"""

class connectionManager:

    def __init__(self, robots):
        self.robots = robots
        self.lora = LoRa(1, 5000, 5000, False)

    def sendRobotMode(self, robotID, robotmode):
        if not (any(robot.robotID == robotID for robot in self.robots)):
            print("Invalid Robot ID: " + robotID)
            return False
        if not ():
            print("Invalid Robot ID: " + robotID)
            return False
        

