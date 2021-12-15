import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose


def landmarkFiltering(landmarks, output_image, display=False):
    
    # right_elbow
    # right_shoulder
    # right_hip
    label = calcAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    label = str(label)
    cv2.putText(output_image, label, (10, 30),cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)

    return output_image


def calcAngle(l1,l2,l3):
    x1, y1, _ = l1
    x2, y2, _ = l2
    x3, y3, _ = l3

    angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))

    if angle < 0:
        angle += 360

    return angle