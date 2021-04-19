from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import threading


class Robot:

    def __init__(self, _robotID):
        self.motorRSpeed = 0
        self.motorLSpeed = 0
        self.motorAngle  = 90
        self.coordlat = 0
        self.coordlon = 0
        self.speed = 0
        self.heading = 0
        self.robotID = _robotID


class Com(LineReceiver):
    def __init__(self, robots):
        self.robots = robots
        self.state = "GETID"
        self.ID = 1
        #print("on", flush=True)
        

    def connectionMade(self):
        self.sendLine(bytes("ID", 'utf-8'))

    def connectionLost(self, reason):
        if self.robot in self.robots:
            del self.robots[self.robot]

    def lineReceived(self, line):
        #print(line.decode("utf-8"))
        if self.state == "GETID":
            self.handle_GETID(line)
        else:
            self.handle_NORMAL(line)

    def handle_GETID(self, ID):
        self.ID = ID.decode("utf-8") 
        self.robots[ID.decode("utf-8")] = self
        self.robot = Robot(self.ID)
        self.state = "NORMAL"
        print("Robot " + str(self.ID) + " connected!")

    def handle_NORMAL(self, message):
        print(self.ID + " ( " +message.decode("utf-8") + " ) ")

        vars = message.decode("utf-8").split("--")

        self.robot.coordlat = vars[0]
        self.robot.coordlon = vars[1]
        self.robot.speed = vars[2]
        self.robot.heading = vars[3]

        #message = "<{}> {}".format(self.ID, message)
        #for name, protocol in self.robots.iteritems():
        #    if protocol != self:
        #        protocol.sendLine(message)


class ComFactory(Factory):
    protocol = Com
    def __init__(self):
        self.robots = {}

    def buildProtocol(self, addr):
        #print("on1",flush=True)
        return Com(self.robots)


def start():
    factory = ComFactory()
    reactor.listenTCP(9655, factory)
    t = threading.Thread(target=reactor.run, args=(False,))
    #twisted_reactor.run()
    #print("on2")
    t.start()
    
    return factory

def send(factory, ID, data):
    #print(factory.robots.keys())
    if str(ID) in factory.robots.keys():
            factory.robots[str(ID)].sendLine(bytes(str(data), 'utf-8')) 

def RobotObj(factory, id):
    try:
        if str(id) in factory.robot.keys():
            return factory.robot[str(id)].robotObj
        return None
    except:
        return None