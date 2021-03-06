import math
import cv2
import numpy as np
from time import time
from landmark_filtering import landmarkFiltering
import mediapipe as mp
import matplotlib.pyplot as plt
from pose_detection import detectPose
from pygame import mixer


mp_pose = mp.solutions.pose
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=2)
video = cv2.VideoCapture(0)
cv2.namedWindow('Bodytracking', cv2.WINDOW_NORMAL)
video.set(3,1280)
video.set(4,960)
frame_counter = 0
play_sound = False
while video.isOpened():
    
    ok, frame = video.read()
    if not ok:
        break

    # avoid - mirroring
    frame = cv2.flip(frame, 1)

    # frame sizing
    frame_height, frame_width, _ =  frame.shape
    frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
    
    # detect landmarks
    frame, landmarks = detectPose(frame, pose_video, display=False)
    
    if landmarks:
        mixer.init()
        frame = landmarkFiltering(landmarks, frame, frame_counter, play_sound)

    cv2.imshow('Bodytracking', frame)

    frame_counter = frame_counter + 1

    k = cv2.waitKey(1) & 0xFF
    if(k == 27):
        break
    if(k == 32):
        if (play_sound == False):
            play_sound = True
        else:
            play_sound = False

video.release()
cv2.destroyAllWindows()