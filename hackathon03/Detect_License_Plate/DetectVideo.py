from PIL import Image
import cv2
import torch
import math 
import function.utils_rotate as utils_rotate
from IPython.display import display
import os
import time
import argparse
import function.helper as helper
import numpy
import Detect

def detectvideo(video_url):
    cap = cv2.VideoCapture(video_url)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(fps, frame_count)

    frames = []
    for i in range(frame_count):
        if i % round(fps) == 0:
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
            else:
                break
    
    cap.release()
    detectframes = []
    i=0
    for frame in frames:
        detectframes.append(Detect.detect(frame)[1])
        i += 1
        print(i)

    for frame in detectframes:
        cv2.imshow('Frame', frame)
        cv2.waitKey(round(1000*10/fps))

detectvideo('video.gif')
