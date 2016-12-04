import time

mainboard = ''


class Logic:
    def __init__(self, mainboard):
        self.mainboard = mainboard

    def movetoball(self, balldetails):
        if balldetails==[0,0,0]:
            self.mainboard.circlearound()
        else:
            self.mainboard.forwardspeed()
            if balldetails[0] > 330:
                self.mainboard.turnleft()
            elif balldetails[0] < 310:
                self.mainboard.turnright()
            elif (balldetails[0] > 310 and balldetails[0] < 330):
                self.mainboard.backwheel(0)

    def grabtheball(self, balldetails):
        # if balldetails[0] > 330:
        #     self.mainboard.turnleft()
        # elif balldetails[0] < 310:
        #     self.mainboard.turnright()
        # elif (balldetails[0] > 310 and balldetails[0] < 330):
        self.mainboard.backwheel(0)
        self.mainboard.forwardspeed()
        self.mainboard.sendwheelcommand()
        time.sleep(2)
        return True
        # return False

    def aimandshoot(self, goaldetails):
        print (goaldetails)
        if goaldetails==[0, 0, 0]:
            self.mainboard.circlearound()
        else:
            if goaldetails[0] > 330:
                self.mainboard.turnleft(150)
            elif goaldetails[0] < 310:
                self.mainboard.turnright(150)
            elif (goaldetails[0] > 310 and goaldetails[0] < 330):
                self.mainboard.kick()
                return True
        return False

    def aimanddrag(self, goaldetails):
        self.mainboard.forwardspeed()
        print (goaldetails)
        if goaldetails==[0, 0, 0]:
            self.mainboard.circlearound()
        else:
            if goaldetails[0] > 330:
                self.mainboard.turnleft()
            elif goaldetails[0] < 310:
                self.mainboard.turnright()
            elif (goaldetails[0] > 310 and goaldetails[0] < 330):
                return False
        return False
