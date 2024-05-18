import mediapipe as mp
import cv2
import math

class HandTracker:
    def __init__(self, webcamNum, P, D, DISTANCE_CONSTANT):

        self.DISTANCE_CONSTANT = DISTANCE_CONSTANT
        self.P, self.D = P, D
        self.webcamNum = webcamNum
        self.handPos = [0.0, 0.0, 0.0]
        self.servoPos = [0.0, 0.0, 0.0]
        self.lastServoPos = []
        self.errorDelta = [0.0, 0.0, 0.0]
        self.lastError = [0.0, 0.0, 0.0]
        self.rawServoPos = [0.0, 0.0, 0.0]
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_drawing = mp.solutions.drawing_utils
        self.vid = cv2.VideoCapture(webcamNum)





    @staticmethod
    def addArrays(arr1, arr2):
        newArr = []
        for i in range(len(arr1)):
            newArr.append(arr1[i]+arr2[i])

        return newArr

    @staticmethod
    def subtractArrays(arr1, arr2):
        newArr = []
        for i in range(len(arr1)):
            newArr.append(arr1[i] - arr2[i])

        return newArr

    @staticmethod
    def multiplyArray(arr1, num):
        newArr = []
        for i in range(len(arr1)):
            newArr.append(arr1[i] * num)

        return newArr


    def findPIDResult(self, error):
        newArr = []
        for i in range(len(error)):
            newArr.append(self.P*error[i] + self.D*self.errorDelta[i])

        return newArr


    def smoothTransfer(self):
        #PUT PID STUFF BETWEEN OLD SERVO POSES AND CURRENT POSES HERE
        error = self.subtractArrays(self.lastServoPos, self.servoPos)
        self.errorDelta = self.subtractArrays(error, self.lastError)

        errorWithPID = self.findPIDResult(error)

        self.lastError = error
        return errorWithPID


    def getServoPosFromArmPos(self, results):
        if results.multi_hand_landmarks:
            if results.multi_hand_landmarks[0].landmark[0]:
                self.handPos[0] = results.multi_hand_landmarks[0].landmark[0].x
                self.handPos[1] = 1 - results.multi_hand_landmarks[0].landmark[0].y


        self.handPos[0] = max(0.00001, min(self.handPos[0], 1))
        self.handPos[1] = max(0.00001, min(self.handPos[1], 1))
        #print("ARM POS: " + str(self.armPos))


        baseAngle = math.atan(2 * (self.handPos[0] - 0.5) / (self.handPos[1])) #* 180/math.pi
        distance = math.sqrt((self.handPos[0] - 0.5) ** 2 + self.handPos[1] * self.handPos[1])
        #print("DISTANCE:", distance)
        armAngleClose = math.acos(self.DISTANCE_CONSTANT * distance) #* 180/math.pi #WAS ARCOS
        armAngleFar = 2*armAngleClose

        # ^ This and the other line with
        # this comment ultimately result to
        # nothing but its peace of mind

        servoPosForBaseAngle = 1/math.pi * baseAngle + .5
        servoPosForArmAngleClose = -2/math.pi * armAngleClose + 1
        servoPosForArmAngleFar = -1/math.pi * armAngleFar + 1
        # ^ This and the other line with
        # this comment ultimately result to
        # nothing but its peace of mind


        #BEFORE USING THIS CODE ON THE ARM!!!
        # FAR SERVO GOES 180 DEGREES WHILE CLOSE ONLY GOES 90
        # set the close servo 0,1 to be 0,90 degrees
        # set the far servo 0,1 to be 0,180 degrees


        # Test arm servo positions using old code to
        # make sure both arm servos
        # are behaving properly when set to
        # they are going to be set to


        self.servoPos = self.rawServoPos = [servoPosForBaseAngle, servoPosForArmAngleClose, servoPosForArmAngleFar]
        #print("SERVO ARRAY " + str(self.servoPos))


        if self.lastServoPos:
            #self.servoPos = self.addArrays(self.lastServoPos, self.smoothTransfer())
            self.servoPos = self.smoothTransfer()
            #print("PID ARRAY " + str(self.servoPos))

        self.lastServoPos = self.servoPos
        return self.multiplyArray(self.servoPos, -1)

    def update(self, showConnections=False, telemetry=False):
        _, frame = self.vid.read()

        imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)

        if results.multi_hand_landmarks and showConnections:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(imageRGB, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        if telemetry:
            pass
            #print(self.armPos)
            #print("SERVO POS ARRAY" + str(self.servoPos))

        cv2.imshow("Connected to " + str(self.webcamNum), imageRGB)

        return self.getServoPosFromArmPos(results)