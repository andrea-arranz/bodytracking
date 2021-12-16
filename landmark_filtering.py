import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
from pygame import mixer
# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose


def landmarkFiltering(landmarks, output_image, display=False):
    
    # right_elbow
    # right_shoulder
    # right_hip
    label1 = int(calcAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                      landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]))

    label2 = int(calcAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]))

    label1 = int(label1/5.6)
    label2 = int(label2/4.5)

    mixer.init()
    label_name = str(label1).rjust(3, str(0))
    if('000' == label_name):
        label_name = '001'
    filename = 'piano/{}.wav'.format(label_name)
    mixer.music.load(filename)
    mixer.music.play()



    cv2.putText(output_image, str(label1), (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2)
    cv2.putText(output_image, str(label2), (10, 60),cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2)

    return output_image


def calcAngle(l1,l2,l3):
    x1, y1, _ = l1
    x2, y2, _ = l2
    x3, y3, _ = l3

    angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))

    if angle < 0:
        angle += 360

    return angle