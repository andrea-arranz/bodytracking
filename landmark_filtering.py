import math
import cv2
import numpy as np
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
from pygame import mixer
import time
# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose


def landmarkFiltering(landmarks, output_image, frame_counter, play_sound):
    
    # right_elbow
    # right_shoulder
    # right_hip
    label1 = int(calcAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                           landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]))

    label2 = int(calcAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]))

    # 7 notes 3 octaves
    # c d e f g a b
    note_angle = int(label1)
    octave_angle = int(label2)
    if play_sound:
        if (frame_counter % 3 == 0):
            getNote(note_angle, octave_angle)
    

    x1, x2, _ = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

    cv2.putText(output_image, 'Note angle: {}'.format(note_angle), (x1, x2),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)
    cv2.putText(output_image, 'Octave angle: {}'.format(octave_angle), (10, 50),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 3)

    return output_image
 

def getNote(note_angle, octave_angle):
    if 0 <= note_angle <= 50:
        playNote('C', getOctave(octave_angle))
    elif 51 <= note_angle <= 100:
        playNote('D', getOctave(octave_angle))
    elif 101 <= note_angle <= 150:
        playNote('E', getOctave(octave_angle))
    elif 151 <= note_angle <= 200:
        playNote('F', getOctave(octave_angle))
    elif 201 <= note_angle <= 250:
        playNote('G', getOctave(octave_angle))
    elif 251 <= note_angle <= 300:
        playNote('A', getOctave(octave_angle))
    elif 301 <= note_angle <= 360:
        playNote('B', getOctave(octave_angle))


def getOctave(angle):
    if 0 <= angle <= 60:
        return '3'
    elif 61 <= angle <= 120:
        return '4'
    elif 121 <= angle <= 180:
        return '5'
    else:
        return '3'

def playNote(note, octave):
    mixer.music.load('piano-mp3/{}{}.mp3'.format(note, octave))
    mixer.music.play()

def old(label1, label2):

    label1 = int(label1/5)
    label2 = int(label2/5.6)
    label_name = str(label1).rjust(3, str(0))
    if('000' == label_name):
        label_name = '001'
    filename = 'piano/{}.wav'.format(label_name)
    mixer.music.load(filename)
    mixer.music.play()

def calcAngle(l1,l2,l3):
    x1, y1, _ = l1
    x2, y2, _ = l2
    x3, y3, _ = l3

    angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))

    if angle < 0:
        angle += 360

    return angle