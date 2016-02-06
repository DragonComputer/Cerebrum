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
import os

STABILIZATION_DETECTION = 5

if not os.path.isfile("memory/" + str(datetime.date.today()) + ".avi"):
	AVI_OUTPUT_FILENAME_ORIGINAL = "memory/" + str(datetime.date.today()) + ".avi"
	AVI_OUTPUT_FILENAME_THRESH = "memory/" + str(datetime.date.today()) + "-thresh.avi"
	AVI_OUTPUT_FILENAME_DELTA = "memory/" + str(datetime.date.today()) + "-delta.avi"
	AVI_OUTPUT_FILENAME_DELTA_COLORED = "memory/" + str(datetime.date.today()) + "-delta-colored.avi"
	MULTIPLE_RECORDS = 0
else:
	AVI_OUTPUT_FILENAME_ORIGINAL = "memory/." + str(datetime.date.today()) + "-TEMP.avi"
	AVI_OUTPUT_FILENAME_THRESH = "memory/." + str(datetime.date.today()) + "-thresh-TEMP.avi"
	AVI_OUTPUT_FILENAME_DELTA = "memory/." + str(datetime.date.today()) + "-delta-TEMP.avi"
	AVI_OUTPUT_FILENAME_DELTA_COLORED = "memory/." + str(datetime.date.today()) + "-delta-colored-TEMP.avi"
	MULTIPLE_RECORDS = 1

CODEC = cv2.cv.CV_FOURCC('X','V','I','D')

original_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_ORIGINAL, CODEC, 25.0, (640,360))
thresh_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_THRESH, CODEC, 25.0, (640,360))
delta_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_DELTA, CODEC, 25.0, (640,360))
delta_colored_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_DELTA_COLORED, CODEC, 25.0, (640,360))

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

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	delta_value = 0

	height, width = frame.shape[:2]
	if not height == 720 or not width == 1280:
		raise ValueError('Aspect ratio of input stream must be [16:9]')

	#frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
	frame = imutils.resize(frame, height=360)


	# resize the frame, convert it to grayscale, and blur it
	#frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	#gray = cv2.blur(gray,(12,12))
	#gray = cv2.GaussianBlur(gray, (5, 5), 0)
	gray = cv2.bilateralFilter(gray,9,75,75)

	# if the first frame is None, initialize it
	if referenceFrame is None:
		referenceFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(referenceFrame, gray)
	thresh = cv2.threshold(frameDelta, 12, 255, cv2.THRESH_BINARY)[1]
	#Below line adaptive threshold is not good for this project
	#thresh = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
	# dilate the thresholded image to fill in holes
	thresh = cv2.dilate(thresh, None, iterations=1)
	frameDeltaColored = cv2.bitwise_and(frame,frame, mask= thresh)

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
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
		delta_colored_out.write(frameDeltaColored)

		if len(delta_value_stack) >= STABILIZATION_DETECTION:
			delta_value_stack.pop(0)
			if min(delta_value_stack) > (numpy.mean(delta_value_stack) - args["min_area"] / 2) and max(delta_value_stack) < (numpy.mean(delta_value_stack) + args["min_area"] / 2):
				on_delta_situation = 0
				delta_value_stack = []
				referenceFrame = None

				#if MULTIPLE_RECORDS:

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
	cv2.imshow("Frame Delta Colored", frameDeltaColored)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q") or key == ord("\x1b"):
		if MULTIPLE_RECORDS:
			ffmpeg_concat_original = "ffmpeg -y -i \"concat:memory/" + str(datetime.date.today()) + ".avi|memory/." + str(datetime.date.today()) + "-TEMP.avi\" -c copy memory/.original-TEMP.avi"
			ffmpeg_concat_thresh = "ffmpeg -y -i \"concat:memory/" + str(datetime.date.today()) + "-thresh.avi|memory/." + str(datetime.date.today()) + "-thresh-TEMP.avi\" -c copy memory/.thresh-TEMP.avi"
			ffmpeg_concat_delta = "ffmpeg -y -i \"concat:memory/" + str(datetime.date.today()) + "-delta.avi|memory/." + str(datetime.date.today()) + "-delta-TEMP.avi\" -c copy memory/.delta-TEMP.avi"
			ffmpeg_concat_delta_colored = "ffmpeg -y -i \"concat:memory/" + str(datetime.date.today()) + "-delta-colored.avi|memory/." + str(datetime.date.today()) + "-delta-colored-TEMP.avi\" -c copy memory/.delta-colored-TEMP.avi"

			os.system(ffmpeg_concat_original)
			os.system(ffmpeg_concat_thresh)
			os.system(ffmpeg_concat_delta)
			os.system(ffmpeg_concat_delta_colored)

			os.system("rm memory/" + str(datetime.date.today()) + "*.avi")
			os.system("rm memory/." + str(datetime.date.today()) + "*.avi")

			os.system("mv memory/.original-TEMP.avi memory/" + str(datetime.date.today()) + ".avi")
			os.system("mv memory/.thresh-TEMP.avi memory/" + str(datetime.date.today()) + "-thresh.avi")
			os.system("mv memory/.delta-TEMP.avi memory/" + str(datetime.date.today()) + "-delta.avi")
			os.system("mv memory/.delta-colored-TEMP.avi memory/" + str(datetime.date.today()) + "-delta-colored.avi")

		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
