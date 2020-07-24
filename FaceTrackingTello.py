from utlis import *
import cv2

global FR, batt
FR = 50
batt = ".."
w, h = 360, 240
pid = [0.4, 0.4, 0]
pError = 0
startCounter = 0  # for no Flight 1   - for flight 0


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

    # Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    # STEP 1
    img = telloGetFrame(myDrone, w, h)
    # STEP 2
    img, info = findFace(img)
    # print(info[0][0])

    # Step 3
    pError = trackFace(myDrone, info, w, pid, pError)
    # print(info[0][0])

    # print(myDrone.get_battery())
    # print(FR)

    # DISPLAY IMAGE
    cv2.putText(img, "Battery:{} UPDATE {}".format(battery(myDrone), str(
        FR)), (20, 15), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1)
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break
