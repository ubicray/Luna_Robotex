import serial

class RefereeController(object):
    motor_controller = ""

    def __init__(self, motor_controller):
        self.serialChannel = serial.Serial("COM4", 9600)
        self.settings = {'playingField': 'B', 'robotID': "D", 'ackMsg': 'ACK-----', 'allRobotsChar': 'X', 'initialCharSignal': 'a'}
        self.CharCounter = 0
        self.initChar = self.settings['initialCharSignal']
        self.kill_received = False
        self.game_state = False
        self.respond = False
        self.listening = False
        self.motor_controller = motor_controller
        self.ackMsg = self.initChar + self.settings["playingField"] + self.settings["robotID"] + \
                      self.settings["ackMsg"]
        self.encodedAckMsg = self.ackMsg.encode()

    def send_ack_msg(self):
        print("message: " + self.encodedAckMsg)
        self.serialChannel.write(self.encodedAckMsg)

    def game_status(self):
        return self.game_state

    def listen(self):
        while not self.kill_received:
            self.CharCounter += 1
            char_signal = self.serialChannel.read().decode()
            print(char_signal)
            if char_signal == self.initChar:
                self.CharCounter = 0
                self.listening = True
                continue
            if not self.listening:
                continue  # wait for next a
            if self.CharCounter == 1 and char_signal != self.settings['playingField']:
                self.listening = False
            if self.CharCounter == 2 and char_signal != self.settings['robotID'] and char_signal != \
                        self.settings['allRobotsChar']:
                self.listening = False
            if self.CharCounter == 2 and char_signal == self.settings['robotID']:
                self.respond = True
            if self.CharCounter == 2 and char_signal == self.settings['allRobotsChar']:
                self.respond = False
            if self.CharCounter == 2 and self.listening:
                msg = ""
                for self.CharCounter in range(3, 12):
                    char_signal = self.serialChannel.read().decode()
                    print(char_signal)
                    if char_signal == self.initChar:
                        self.CharCounter = 0
                        break
                    if char_signal == "-":
                        self.listening = False
                        break
                    msg += char_signal
                    if msg in ["START", "STOP"]:
                        print("msg:",msg)
                        if self.respond:
                            self.send_ack_msg()

                        if "START" in msg:
                            self.game_state = True
                        elif "STOP" in msg:
                            self.motor_controller.stopall()
                            self.game_state = False
