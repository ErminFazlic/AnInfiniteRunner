import mediapipe as mp
import cv2
import time

class Hand():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5 ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, show = True):
        RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(RGBimg)

        if self.results.multi_hand_landmarks:
            for landmarks in self.results.multi_hand_landmarks:
                if show:
                    self.mpDraw.draw_landmarks(img, landmarks, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPos(self, img, handNumber = 0, show = True):

        posList = []

        if self.results.multi_hand_landmarks:
            height, width, channel = img.shape
            hand = self.results.multi_hand_landmarks[handNumber]
            for i, landmarks in enumerate(hand.landmark):
                lmX = int(landmarks.x*width)
                lmY = int(landmarks.y*height)
                posList.append([i, lmX, lmY])
        return posList
