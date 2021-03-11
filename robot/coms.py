from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor as twisted_reactor
import threading

def reactor():
    t = threading.Thread(
        target=twisted_reactor.run,
        kwargs={"installSignalHandlers": False},
        daemon=True,
    )
    t.start()

    yield twisted_reactor

    twisted_reactor.callFromThread(twisted_reactor.stop)
    t.join()


class Robot:
    mode = 0 #0 or 1, 0 = manual control, 1 auto
    motorRSpeed = 0
    motorLSpeed = 0
    motorAngle  = 90
    coordlat = 0
    coordlon = 0
    GOcoordlat = 0
    GOcoordlon = 0



class Com(LineReceiver):
    def __init__(self, robot):
        self.robot = robot
        self.robot["0"] = self
        self.robotObj = Robot()
    def connectionMade(self):
        self.sendLine(bytes("1", 'utf-8'))

    def lineReceived(self, line):

        pass

    def handle_GETNAME(self, name):
        pass


class ComFactory(Factory):
    def __init__(self):
        self.robot = {}
    
    def startedConnecting(self, connector):
        print('Started to connect.', flush=True)

    def buildProtocol(self, addr):
        print('Connected.', flush=True)
        return Com(self.robot)

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason, flush=True)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason, flush=True)

def start(IP):
    factory = ComFactory()
    #twisted_reactor.connectTCP("10.0.0.1", 8123, factory)
    twisted_reactor.connectTCP(IP, 9655, factory)
    
    reactor()
    return factory
    
def send(factory, data):
    if "0" in factory.robot.keys():
        factory.robot["0"].sendLine(bytes(data, 'utf-8')) 
    