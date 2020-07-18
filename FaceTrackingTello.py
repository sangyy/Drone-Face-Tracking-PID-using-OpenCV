from utlis import *
import cv2

w, h = 640, 480

myDrone = intializeTello()

while True:

    # STEP 1
    img = telloGetFrame(myDrone, w, h)

    # DISPLAY IMAGE
    cv2.imshow("MyResult", img)

    # WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) and 0xFF == ord('q'):  # replace the 'and' with '&amp;'
        myDrone.land()
        break
