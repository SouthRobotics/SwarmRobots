from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor as reactor
import threading



class Robot:
    motorRSpeed = 0
    motorLSpeed = 0
    motorAngle  = 90
    coordlat = 0
    coordlon = 0
    speed = 0
    heading = 0



class Com(LineReceiver):
    def __init__(self, robot):
        self.robot = robot
        self.robot["0"] = self
        #self.robotObj = Robot()
    def connectionMade(self):
        self.sendLine(bytes("1", 'utf-8'))

    def lineReceived(self, line):
        print(" ( " +line.decode("utf-8") + " ) ")
        vars = line.decode("utf-8").split("--")

        Robot.motorRSpeed = vars[0]
        Robot.motorLSpeed = vars[1]
        Robot.motorAngle = vars[2]

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
    reactor.connectTCP(IP, 9655, factory)
    t = threading.Thread(target=reactor.run, args=(False,))
    #twisted_reactor.run()
    #print("on2")
    t.start()

    return factory
    
def send(factory, data):
    if "0" in factory.robot.keys():
        factory.robot["0"].sendLine(bytes(str(data), 'utf-8')) 
    
