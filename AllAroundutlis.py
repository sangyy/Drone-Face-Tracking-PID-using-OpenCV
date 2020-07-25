from djitellopy import Tello
import cv2
import numpy as np


def intializeTello():
    # CONNECT TO TELLO
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    # print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone


def telloGetFrame(myDrone, w=360, h=240):
    # GET THE IMGAE FROM TELLO
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img


def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 4)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cx = x+w//2
        cy = y+h//2
        area = w*h
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0, ], 0]


def trackFace(myDrone, info, w, h, pid, pError):

    # PID yaw
    errorYaw = info[0][0] - w//2
    speedYaw = pid[0]*errorYaw + pid[1]*(errorYaw-pError[0])
    speedYaw = int(np.clip(speedYaw, -100, 100))
    # print(speed)

    # PID up
    errorUp = info[0][1] - h//2
    # print("upround:",errorUp)
    speedUp = pid[0]*errorUp + pid[1]*(errorUp-pError[1])
    speedUp = -int(np.clip(speedUp, -100, 100))
    # print("up:",errorUp,speedUp)

    # PID for_back
    errorFor = info[1] - 5000
    if errorFor > 0:
        speedFor = -30
    elif errorFor < 0:
        speedFor = 10
    else:
        speedFor = 0
    # print("Forround:",errorFor)
    # speedFor = pid[0]*errorFor + pid[1]*(errorFor-pError[2])
    # speedFor = -int(np.clip(speedFor, -100, 100))
    print("for_back:", errorFor, speedFor)

    if info[0][0] != 0:
        myDrone.yaw_velocity = speedYaw
        myDrone.for_back_velocity = speedFor
        myDrone.up_down_velocity = speedUp
        error = [errorYaw, errorUp, errorFor]

        # state = "yaw_following"
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = [0, 0, 0]
        # state = "unlock"
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    return error
