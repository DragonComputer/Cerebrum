import numpy as np
import cv2
import argparse
import time

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

while True:
    # Create some random colors
    color = np.random.randint(0,255,(100,3))

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    #p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    #print p0
    #print type(p0[0][0][0])

    p0 = np.random.randint(720, size=(100, 1, 2))
    p0 = p0.astype(np.float32)
    print p0
    print type(p0[0][0][0])

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)

    while True:
        ret,frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        if p1 is None:
            break

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

       # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()
            c,d = old.ravel()
            cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
            cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        img = cv2.add(frame,mask)

        cv2.imshow('frame',img)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)


cv2.destroyAllWindows()
cap.release()
