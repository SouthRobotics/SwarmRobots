import time



class Propulsion:

    def __init__ (self, pi, ESCL, ESCR, ServoL, ServoR):


        self.ESCMin = 1000
        self.ESCMax = 2000
        self.ServoMin = 500
        self.ServoMax = 2500
        self.ServoCenter = int((self.ServoMax-self.ServoMin)/2 + self.ServoMin)

        self.pi = pi
        self.ESCL = ESCL
        self.ESCR = ESCR
        self.ServoL = ServoL
        self.ServoR = ServoR

        self.pi.set_servo_pulsewidth(self.ESCL, self.ESCMin)
        self.pi.set_servo_pulsewidth(self.ESCR, self.ESCMin)
        time.sleep(7)
        pi.set_servo_pulsewidth(self.ESCL, 0)
        pi.set_servo_pulsewidth(self.ESCR, 0)
        time.sleep(2)
        pi.set_servo_pulsewidth(self.ESCL, self.ESCMin)
        pi.set_servo_pulsewidth(self.ESCR, self.ESCMin)
        time.sleep(1)

        self.pi.set_servo_pulsewidth(self.ESCL, self.ESCMin)
        self.pi.set_servo_pulsewidth(self.ESCR, self.ESCMin)
        self.pi.set_servo_pulsewidth(self.ServoL, self.ServoCenter)
        self.pi.set_servo_pulsewidth(self.ServoR, self.ServoCenter)

    def setSpeedAngle(self, Lspeed, Rspeed, Angle): #0->1, 0->1, 0->180
        if(Lspeed >=0 and Lspeed <= 1 and Rspeed >=0 and Rspeed <= 1 and Angle >=0 and Angle <= 180):
        
            self.pi.set_servo_pulsewidth(self.ESCL, int(Lspeed*(self.ESCMax-self.ESCMin)+self.ESCMin))
            self.pi.set_servo_pulsewidth(self.ESCR, int(Rspeed*(self.ESCMax-self.ESCMin)+self.ESCMin))
            self.pi.set_servo_pulsewidth(self.ServoR, int((180-Angle)*((self.ServoMax-self.ServoMin)/180)+self.ServoMin))
            self.pi.set_servo_pulsewidth(self.ServoL, int((180-Angle)*((self.ServoMax-self.ServoMin)/180)+self.ServoMin))

    def getSpeedAngle(self):
        return (self.pi.get_servo_pulsewidth(self.ESCL)-self.ESCMin)/(self.ESCMax-self.ESCMin), (self.pi.get_servo_pulsewidth(self.ESCR)-self.ESCMin)/(self.ESCMax-self.ESCMin), (self.pi.get_servo_pulsewidth(self.ServoL)-self.ServoMin)/((self.ServoMax-self.ServoMin)/180)
