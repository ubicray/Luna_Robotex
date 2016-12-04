import cv2
import threading
from detector import Detector
from mainboard_controller import MainboardController
from logic import Logic
from referee_controller import RefereeController

camera = cv2.VideoCapture(0)
detect = Detector()
mainboard = MainboardController()
logic = Logic(mainboard)
referee = RefereeController(mainboard)
state = "movingtoball"
balldetails = ""
goaldetails = ""
seeingaball = False
ballindribler = False
ballisclose = False
reset = False
dribblerison = False


# right - 0, left - 1, back - 2

# Possible states: movingtoball, aimandshoot

td1 = threading.Thread(target=referee.listen)
td1.start()

while True:
    (frameready, frame) = camera.read(1)
    if referee.game_status():
        if frameready:

            balldetails, goaldetails = detect.coordinates(frame)

            print (balldetails)
            print (goaldetails)

            if state == "movingtoball":
                print (balldetails)
                # if balldetails != [0, 0, 0]:
                #     seeingaball = True
                # else:
                #     seeingaball = False

                if balldetails[1]>450:
                    ballisclose=True

                logic.movetoball(balldetails)
            elif state == "grabtheball":
                if dribblerison == False:
                    mainboard.dribbler_on()
                    dribblerison=True
                ballindribler=logic.grabtheball(balldetails)
            elif state == "aimandshoot":
                reset = logic.aimandshoot(goaldetails)

            if (reset):
                ballindribler = False
                ballisclose = False
                reset = False

            if (ballindribler):
                state = "aimandshoot"
            elif (ballisclose):
                state = "grabtheball"
            else:
                state = "movingtoball"

            mainboard.sendwheelcommand()

            print(state)


    keypress = cv2.waitKey(50) & 0xFF
    if keypress == 27:
        mainboard.stopall()
        camera.release()
        cv2.destroyAllWindows()
        break
    if keypress == 8:
        # mainboard.dribbler_init()
        # time.sleep(3)
        ballindribler = True