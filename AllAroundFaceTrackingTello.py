from AllAroundutlis import *
import cv2

global FR, batt
FR = 50
batt = ".."
w, h = 360, 240
pid = [0.4, 0.4, 0]
pError = [0, 0, 0]
startCounter = 0  # for no Flight 1   - for flight 0
state = "land"


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
    k = cv2.waitKey(20) & 0xFF
    # print(k)

    # Flight
    if startCounter == 0 and k == ord('t'):
        myDrone.takeoff()
        print("takeoff!!!")
        startCounter = 1

    # STEP 1
    img = telloGetFrame(myDrone, w, h)
    # STEP 2
    img, info = findFace(img)
    # print(info[0][0])

    # Step 3
    pError = trackFace(myDrone, info, w, h, pid, pError)
    # print("pError is", pError)
    # print(info[0][0])

    # print(myDrone.get_battery())
    # print(FR)

    # DISPLAY IMAGE
    cv2.circle(img,(w//2,h//2),6,(0,255,0),2)
    cv2.putText(img, "Battery:{} UPDATE {} stat:{}".format(battery(myDrone), str(
        FR), str(state)), (20, 15), cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 255), 1)
    cv2.imshow('Image', img)
    if k == ord('q') or k == ord('l'):
        myDrone.land()
        print("landing!!!")
        break
