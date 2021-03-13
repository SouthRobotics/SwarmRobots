from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import threading


class Robot:

    def __init__(self, _robotID):
        self.robotmode = 0  # 0-> coord based 1-> direct motor control
        self.coordlat = 0
        self.coordlon = 0
        self.Gocoordlat = 0
        self.Gocoordlon = 0
        self.motorRpos = 90  # 0-180
        self.motorRspeed = 0  # 0-1
        self.motorLpos = 90  # 0-180
        self.motorLspeed = 0  # 0-1
        self.robotID = _robotID


class Com(LineReceiver):
    def __init__(self, robots):
        self.robots = robots
        self.state = "GETID"
        self.ID = 1
        print("on", flush=True)
        

    def connectionMade(self):
        self.sendLine(bytes("ID", 'utf-8'))

    def connectionLost(self, reason):
        if self.robot in self.robots:
            del self.robots[self.robot]

    def lineReceived(self, line):
        if self.state == "GETID":
            self.handle_GETID(line)
        else:
            self.handle_NORMAL(line)

    def handle_GETID(self, ID):
        self.ID = ID.decode("utf-8") 
        self.robots[ID.decode("utf-8")] = self
        self.robot = Robot(self.ID)
        self.state = "NORMAL"

    def handle_NORMAL(self, message):
        print(message)
        #message = "<{}> {}".format(self.ID, message)
        #for name, protocol in self.robots.iteritems():
        #    if protocol != self:
        #        protocol.sendLine(message)


class ComFactory(Factory):
    protocol = Com
    def __init__(self):
        self.robots = {}  # maps user names to Chat instances

    def buildProtocol(self, addr):
        print("on1",flush=True)
        return Com(self.robots)


def start():
    factory = ComFactory()
    reactor.listenTCP(9655, factory)
    t = threading.Thread(target=reactor.run, args=(False,))
    #twisted_reactor.run()
    #print("on2")
    t.start()
    
    return factory

def send(factory, ID):
    print(factory.robots.keys())
    if str(ID) in factory.robots.keys():
            factory.robots[str(ID)].sendLine(bytes("hi back", 'utf-8')) 