import serial
import time
from datetime import datetime

class MainboardController:
    port = "COM3"
    motor = ""
    # l+002r-112b+502

    leftwheelbuf=0
    rightwheelbuf=0
    backwheelbuf=0


    def __init__(self):
        self.motor = serial.Serial(self.port, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        self.motor.write('d50\n')

        time.sleep(0.5)
        self.motor.write('j\n')

    def circlearound(self, speed=100):
        self.leftwheelbuf = speed
        self.rightwheelbuf = speed
        self.backwheelbuf = speed

    def forwardspeed(self, speed=100):
        self.leftwheelbuf=speed*-1
        self.rightwheelbuf = speed

    def turnleft(self, speed=200):
        self.backwheel(speed)

    def turnright(self, speed=200):
        self.backwheel(-speed)

    def backwheel(self, speed=150):
        self.backwheelbuf = speed

    def sendwheelcommand(self):
        cmd= 'l' + str(self.leftwheelbuf).zfill(4) + 'r' + str(self.rightwheelbuf).zfill(4) + 'b' + str(self.backwheelbuf).zfill(4) + '\n'
        self.motor.write(cmd)
        print (cmd)
        self.leftwheelbuf = 0
        self.rightwheelbuf = 0
        self.backwheelbuf = 0

    def dribbler_init(self):
        self.motor.write('d50\n')

    def dribbler_on(self):
        time.sleep(0.1)
        self.motor.write('d170\n')
        time.sleep(0.1)

    def kick(self):
        self.stopwheels()
        time.sleep(0.5)
        self.motor.write('n\n')
        time.sleep(0.1)
        self.motor.write('j\n')
        time.sleep(0.1)
        print("KICKED!")

    def checkforball(self):
        self.motor.write('i\n')
        line = self.motor.readline().strip()
        print(line)

    def stopwheels(self):
        self.leftwheelbuf = 0
        self.rightwheelbuf = 0
        self.backwheelbuf = 0
        self.sendwheelcommand()

    def stopall(self):
        time.sleep(0.1)
        self.leftwheelbuf = 0
        self.rightwheelbuf = 0
        self.backwheelbuf = 0
        self.sendwheelcommand()
        time.sleep(0.1)
        self.dribbler_init()
        time.sleep(0.1)
