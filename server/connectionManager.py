import server.byteConverter as _byteConverter
from raspi_lora import LoRa, ModemConfig


class Robotstats:

    def __init__(self, _broadcastID):
        self.coordlat = 0
        self.coordlon = 0
        self.motorRpos = 90
        self.motorRspeed = 0
        self.motorLpos = 90
        self.motorLspeed = 0
        self.broadcastID = _broadcastID


class connectionManager:

    def __init__(self, _broadcastID):
        self.robots = []
        for i, ID in enumerate(_broadcastID):
            self.robots.append = Robotstats(ID)
    
    