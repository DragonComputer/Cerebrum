# USAGE
# python motion_detector.py
# python motion_detector.py --video PATH/example_01.mp4

import argparse
import datetime
import imutils
import time
import cv2
import numpy
import os

STABILIZATION_DETECTION = 5

# Define record files's path and filenames
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

CODEC = cv2.cv.CV_FOURCC('X','V','I','D') # Define desired codec (Only XVID tested)

# Create video record files. CAUTION: VideoWriter always removes existing files.
original_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_ORIGINAL, CODEC, 25.0, (640,360))
thresh_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_THRESH, CODEC, 25.0, (640,360))
delta_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_DELTA, CODEC, 25.0, (640,360))
delta_colored_out = cv2.VideoWriter(AVI_OUTPUT_FILENAME_DELTA_COLORED, CODEC, 25.0, (640,360))

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

referenceFrame = None # Initialize the first frame in the video stream

(grabbed, first_frame) = camera.read() # Grab the first frame

height, width = first_frame.shape[:2] # Get video height and width (size)
#if not height == 720 or not width == 1280:

if float(width) / float(height) != float(16) / float(9):
	raise ValueError('Aspect ratio of input stream must be [16:9]')

frame_counter = 0 # Define frame counter variable
on_delta_situation = 0 # Delta situation checking variable
delta_value_stack = [] # List of delta values

while True: # Loop over the frames of the video

	frame_counter += 1 # Increase frame counter's value

	(grabbed, frame) = camera.read() # Grab the current frame and initialize the occupied/unoccupied

	if not grabbed: # If the frame could not be grabbed, then we have reached the end of the video
		break

	delta_value = 0 # Delta Value for storing max continuous contour area for current frame

	frame = imutils.resize(frame, height=360) # Resize frame to 360p. Alternative resizing method:
	#frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert frame to grayscale

	gray = cv2.bilateralFilter(gray,9,75,75) # Blur current frame with Bilateral Filter for noise reduction
	# http://docs.opencv.org/master/d4/d13/tutorial_py_filtering.html
	# Alternative Blur Methods:
	#gray = cv2.blur(gray,(12,12))
	#gray = cv2.GaussianBlur(gray, (5, 5), 0)

	if referenceFrame is None: # If Reference Frame is None, initialize it
		referenceFrame = gray
		continue

	frameDelta = cv2.absdiff(referenceFrame, gray) # Compute the absolute difference between the current frame and reference frame
	thresh = cv2.threshold(frameDelta, 12, 255, cv2.THRESH_BINARY)[1] # Apply OpenCV's threshold function to get binary frame
	# Below line adaptive threshold is not good for this project
	#thresh = cv2.adaptiveThreshold(frameDelta,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

	thresh = cv2.dilate(thresh, None, iterations=1) # Dilate the thresholded image to fill in holes
	frameDeltaColored = cv2.bitwise_and(frame,frame, mask= thresh) # Bitwise and - to get delta frame

	# Find contours on thresholded image
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	contour_area_stack = [] # List of contour areas's values

	# Loop over the contours
	if cnts:
		for c in cnts: # Contour in Contours
			contour_area_stack.append(cv2.contourArea(c)) # Calculate contour area and append to contour stack
			if cv2.contourArea(c) > args["min_area"]: # If contour area greater than min area
				(x, y, w, h) = cv2.boundingRect(c) # Compute the bounding box for this contour
				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw it on the frame
		delta_value = max(contour_area_stack) # Assign max contour area to delta value

		if delta_value > args["min_area"]: # If max contour area (delta value) greater than min area
			on_delta_situation = 1 # Initialize delta situation

	if on_delta_situation: # If we are on delta situation

		delta_value_stack.append(delta_value) # Append max contour area (delta value) to delta value stack

		original_out.write(frame) # Write Original Frame to file
		thresh_out.write(cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)) # Write Frame Threshhold to file
		delta_out.write(cv2.cvtColor(frameDelta, cv2.COLOR_GRAY2BGR)) # Write Frame Delta to file
		delta_colored_out.write(frameDeltaColored) # Write Frame Delta Colored to file

		if len(delta_value_stack) >= STABILIZATION_DETECTION: # If length of delta value stack is greater than or equal to STABILIZATION_DETECTION constant
			delta_value_stack.pop(0) # Pop first element of delta value stack
			# If minimum delta value is greater than (mean of last 5 frame - minimum area / 2) and maximum delta value is less than (mean of last 5 frame + minimum area / 2)
			if min(delta_value_stack) > (numpy.mean(delta_value_stack) - args["min_area"] / 2) and max(delta_value_stack) < (numpy.mean(delta_value_stack) + args["min_area"] / 2):
				on_delta_situation = 0 # Then video STABILIZED
				delta_value_stack = [] # Empty delta value stack
				referenceFrame = None  # Clear reference frame

	# Draw the text and timestamp on the frame
	cv2.putText(frame, "Diff    : {}".format(delta_value), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Thresh : {}".format(args["min_area"]), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Frame : {}".format(frame_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Delta  : {}".format(on_delta_situation), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

	# Show the frames and record if the user presses ESC or q
	cv2.imshow("Original Frame", frame)
	cv2.imshow("Frame Threshhold", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	cv2.imshow("Frame Delta Colored", frameDeltaColored)
	key = cv2.waitKey(1) & 0xFF

	# if the `ESC` or `q` key is pressed, break from the loop
	if key == ord("q") or key == ord("\x1b"):
		if MULTIPLE_RECORDS: # If there are multiple records

			# Then concatenate them with ffmpeg
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
			# Concatenate finished

		break

cv2.destroyAllWindows() # Close any open windows
camera.release() # Release the capture device
