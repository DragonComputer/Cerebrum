# USAGE
# python perception.py
# python perception.py --video PATH/example_01.mp4

import argparse
import datetime
import imutils
import time
import cv2
import numpy
import os

STABILIZATION_DETECTION = 5

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

if args.get("video", None) is None: # If the video argument is None, then we are reading from webcam
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)
else:								# Otherwise, we are reading from a video file
	camera = cv2.VideoCapture(args["video"])

referenceFrame = None # Initialize the reference frame in the video stream

(grabbed, first_frame) = camera.read() # Grab the first frame

height, width = first_frame.shape[:2] # Get video height and width  from first frame(size)
#if not height == 720 or not width == 1280:
if float(width) / float(height) != float(16) / float(9):
	raise ValueError('Aspect ratio of input stream must be [16:9]')

frame_counter = 1 # Define frame counter variable
on_delta_situation = 0 # Delta situation checking variable
delta_value_stack = [] # List of delta values
