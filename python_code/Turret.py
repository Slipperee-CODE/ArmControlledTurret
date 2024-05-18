from working_but_old.HandTracker import HandTracker
import serial.tools.list_ports
import time
import cv2

tracking_index = 1
raw_tracks = []
pid_tracks = []
#handTracker = ArmTracker(0, .5, .05, 1)
handTracker = HandTracker(0, .5, .05, 1)
#IMPLEMENT A ROLLING AVERAGE (AVERAGE OF LAST N POS IS NEW POS)
#IMPLEMENT WEIGHTED ROLLING AVERAGE (MOST RECENT POS MOST IMPORTANT)


#MAKE POSTER EXPLAINING THE MATH AND PROCESS
#MAKE #1 ON POSTER
#CREATE POSTER LAYOUT/OUTLINE

#FIX NO HAND FREAKOUT

#CLEAN UP CODE USING NUMPY


useSerial = False

if useSerial:
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial('COM3', 115200)
    time.sleep(1)

#try:
while True:
    servoPos = handTracker.update(True, True)
    rawServoPos = handTracker.rawServoPos
    raw_tracks.append(rawServoPos[tracking_index])
    pid_tracks.append(servoPos[tracking_index])

    #print("PID ARRAY " + str(servoPos))
    if useSerial:
        for i in range(len(servoPos)):
            servoPos[i] = str(round(servoPos[i], 3))
        serialInst.write(" ".join(servoPos).encode("utf"))
    cv2.waitKey(1)

"""
except:

    pyplot.plot(list(range(len(raw_tracks))),raw_tracks)
    pyplot.plot(list(range(len(pid_tracks))),pid_tracks)
    pyplot.show()
"""