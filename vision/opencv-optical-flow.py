import numpy as np
import cv2
import argparse
import time
import random
import math
from collections import Counter

TRACKER_POINTS = 2000
CRAZY_LINE_DISTANCE =  50
CRAZY_LINE_LIMIT = 100 * TRACKER_POINTS / 1000

def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	cap = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	cap = cv2.VideoCapture(args["video"])

# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

frame_counter = 0

while True:
    # Create some random colors
    color = np.random.randint(0,255,(TRACKER_POINTS,3))

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    frame_counter += 1
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    #p1 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    #print p1
    #print type(p1[0][0][0])

    #For Polygon Model
    lines = [[]] * TRACKER_POINTS

    #For Triangle Model
    p0 = None

    p1 = np.random.randint(1280, size=(TRACKER_POINTS, 1, 2))
    for y in p1:
         if y[0][1] > 960:
             y[0][1] = np.random.random_integers(960)

    #print type(p1[0][0][0])
    p1 = p1.astype(np.float32)
    #print p1
    #print type(p1[0][0][0])

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    mask_delta = np.zeros_like(old_frame)
    white_color = np.array([255,255,255])

    total_crazy_lines = 0

    most_common_angle = None

    while True:
        ret,frame = cap.read()
        frame_counter += 1
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # calculate optical flow
        p2, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p1, None, **lk_params)

        if p2 is None:
            break

        # Select good points
        good_points2 = p2[st==1]
        good_points1 = p1[st==1]

        angles_array = []

       # draw the tracks
        for i,(good_point2,good_point1) in enumerate(zip(good_points2,good_points1)):
            x2,y2 = good_point2.ravel()
            x1,y1 = good_point1.ravel()

            tup2 = (x2,y2)
            tup1 = (x1,y1)

            distance = math.hypot(x2 - x1, y2 - y1)
            if distance >= CRAZY_LINE_DISTANCE:
                total_crazy_lines += 1

            angle = math.atan2(y2-y1, x2-x1)
            angle = math.degrees(angle)
            angle = round(angle)
            #print angle
            angles_array.append(angle)

            if most_common_angle != None:
                if abs(most_common_angle - angle) > 20:
                    cv2.line(mask_delta, (x2,y2),(x1,y1), white_color, 3)

            cv2.line(mask, (x2,y2),(x1,y1), color[i].tolist(), 1)
            #cv2.circle(frame,(x2,y2),5,color[i].tolist(),-1)

        if angles_array:
            print Counter(angles_array).most_common()[0]
            most_common_angle = Counter(angles_array).most_common()[0][0]

        img = cv2.add(frame,mask)

        mask_delta_gray = cv2.cvtColor(mask_delta, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(mask_delta_gray, 12, 255, cv2.THRESH_BINARY)[1]
        frameDelta = cv2.bitwise_and(frame,frame, mask= thresh)

        cv2.imshow('frame',img)
        cv2.imshow('mask delta',mask_delta)
        cv2.imshow('frame delta',frameDelta)

        #print total_crazy_lines
        if total_crazy_lines >= CRAZY_LINE_LIMIT:
            break

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        #p0 = p1
        p1 = good_points2.reshape(-1,1,2)


cv2.destroyAllWindows()
cap.release()
