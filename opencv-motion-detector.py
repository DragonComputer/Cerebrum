# USAGE
# python motion_detector.py
# python motion_detector.py --video videos/example_01.mp4

# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy

STABILIZATION_DETECTION = 20
AVI_OUTPUT_FILENAME_ORIGINAL = "visual-memory/" + str(datetime.date.today()) + ".avi"
AVI_OUTPUT_FILENAME_THRESH = "visual-memory/" + str(datetime.date.today()) + "-thresh.avi"
AVI_OUTPUT_FILENAME_DELTA = "visual-memory/" + str(datetime.date.today()) + "-delta.avi"
CODEC = cv2.cv.CV_FOURCC('X','V','I','D')

original_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_ORIGINAL, CODEC, 20.0, (640,480))
thresh_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_THRESH, CODEC, 20.0, (640,480))
delta_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_DELTA, CODEC, 20.0, (640,480))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
referenceFrame = None

frame_counter = 0
on_delta_situation = 0
delta_value_stack = []
# loop over the frames of the video
while True:
	frame_counter += 1
	# grab the current frame and initialize the occupied/unoccupied
	# text
	(grabbed, frame) = camera.read()
	delta_value = 0

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	#frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if referenceFrame is None:
		referenceFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(referenceFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	#thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	countour_stack = []
	# loop over the contours
	if cnts:
		for c in cnts:
			countour_stack.append(cv2.contourArea(c))
			if cv2.contourArea(c) > args["min_area"]:
				# compute the bounding box for the contour, draw it on the frame,
				# and update the text
				(x, y, w, h) = cv2.boundingRect(c)
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		delta_value = max(countour_stack)

		# if the contour is too small, ignore it
		if delta_value > args["min_area"]:
			on_delta_situation = 1

	if on_delta_situation:
		delta_value_stack.append(delta_value)

		original_out.write(frame)
		thresh_out.write(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR))
		delta_out.write(cv2.cvtColor(frameDelta, cv2.COLOR_GRAY2BGR))

		if len(delta_value_stack) >= STABILIZATION_DETECTION:
			delta_value_stack.pop(0)
			if min(delta_value_stack) > (numpy.mean(delta_value_stack) - args["min_area"] / 2) and max(delta_value_stack) < (numpy.mean(delta_value_stack) + args["min_area"] / 2):
				on_delta_situation = 0
				delta_value_stack = []
				referenceFrame = None

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Diff    : {}".format(delta_value), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Thresh : {}".format(args["min_area"]), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Frame : {}".format(frame_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Delta  : {}".format(on_delta_situation), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

	# show the frame and record if the user presses a key
	cv2.imshow("Original Frame", frame)
	cv2.imshow("Frame Threshhold", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
