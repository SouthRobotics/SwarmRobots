



class Propulsion:

    def __init__ (self, pi, ESCL, ESCR, ServoL, ServoR):

        self.ESCMin = 1000
        self.ESCMax = 2000
        self.ServoMin = 1000
        self.ServoMax = 2000
        self.ServoCenter = int((self.ServoMax-self.ServoMin)/2 + self.ServoMin)

        self.pi = pi
        self.ESCL = ESCL
        self.ESCR = ESCR
        self.ServoL = ServoL
        self.ServoR = ServoR

        self.pi.set_servo_pulsewidth(self.ServoL, self.ServoCenter)
        self.pi.set_servo_pulsewidth(self.ServoR, self.ServoCenter)
        # need to implement ESC calibration procedure here
        self.pi.set_servo_pulsewidth(self.ESCL, self.ESCMin)
        self.pi.set_servo_pulsewidth(self.ESCR, self.ESCMin)

    def setSpeedAngle(self, Lspeed, Rspeed, Angle): #0->1, 0->1, 0->180
        if(Lspeed >=0 and Lspeed <= 1 and Rspeed >=0 and Rspeed <= 1 and Angle >=0 and Angle <= 180):
        
            self.pi.set_servo_pulsewidth(self.ESCL, int(Lspeed*1000+self.ESCMin))
            self.pi.set_servo_pulsewidth(self.ESCR, int(Rspeed*1000+self.ESCMin))
            self.pi.set_servo_pulsewidth(self.ServoR, int(Angle*5.555+self.ServoMin))
            self.pi.set_servo_pulsewidth(self.ServoL, int(Angle*5.555+self.ServoMin))

    def getSpeedAngle(self):
        return (self.pi.get_servo_pulsewidth(self.ESCL)-1000)/1000, (self.pi.get_servo_pulsewidth(self.ESCR)-1000)/1000, (self.pi.get_servo_pulsewidth(self.ServoL)-self.ServoMin)/5.555
