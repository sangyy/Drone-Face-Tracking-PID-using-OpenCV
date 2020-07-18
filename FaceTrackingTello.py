from utlis import *
import cv2

global FR, batt
FR = 50
batt = ".."
w, h = 640, 480


def battery(self):
    global FR
    global batt
    FR -= 1
    if FR == 0:
        batt = self.get_battery()
        FR = 50
    if isinstance(batt, str):
        return batt[:2]
    else:
        return "wait..."


myDrone = intializeTello()


while True:

    # STEP 1
    img = telloGetFrame(myDrone, w, h)

    # DISPLAY IMAGE
    cv2.putText(img, "Battery:{} UPDATE {}".format(battery(myDrone), str(
        FR)), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("MyResult", img)
    # print(myDrone.get_battery())
    # print(FR)

    # WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) and 0xFF == ord('q'):  # replace the 'and' with '&amp;'
        myDrone.land()
        break
