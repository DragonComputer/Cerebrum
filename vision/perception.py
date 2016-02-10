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
import math
import random
from collections import Counter

STABILIZATION_DETECTION = 5 # Number of frames to detect stabilization
NON_STATIONARY_PERCENTAGE = 75 # Percentage of frame for detecting NON-STATIONARY CAMERA. Like: ( height * width * float(X) / float(100) )
TARGET_HEIGHT = 360 # Number of horizontal lines for target video and processing. Like 720p, 360p etc.
TRACKER_POINTS = 500 # How many points will be used to track the optical flow
CRAZY_LINE_DISTANCE =  50 # Distance value to detect crazy lines
CRAZY_LINE_LIMIT = 100 * TRACKER_POINTS / 1000 # Amount of crazy lines are indication of different shots
ABSDIFF_ANGLE = 20 # To determine the inconsistency between tangent values in degrees
LINE_THICKNESS = 3 # Lines thickness that we will use for mask delta
CONTOUR_LIMIT = 10 # Contour limit for detecting ZOOM, ZOOM + PAN, ZOOM + TILT, ZOOM + ROLL (Not just PAN, TILT, ROLL)
DELTA_LIMIT_DIVISOR = 3 # Divisor for detecting too much motion. Like: ( height * width / X )

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

# Parameters for Lucas Kanade Optical Flow
lk_params = dict( winSize  = (15,15),
				  maxLevel = 2,
				  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

referenceFrame = None # Initialize the reference frame in the video stream

(grabbed, first_frame) = camera.read() # Grab the first frame

height, width = first_frame.shape[:2] # Get video height and width  from first frame(size)
#if not height == 720 or not width == 1280:
if float(width) / float(height) != float(16) / float(9):
	raise ValueError('Aspect ratio of input stream must be [16:9]')

frame_counter = 1 # Define frame counter variable
motion_detected = 0 # Delta situation checking variable
delta_value_stack = [] # List of delta values

while True: # Loop over the frames of the video

	frame_counter += 1 # Increase frame counter's value

	(grabbed, frame) = camera.read() # Grab the current frame and initialize the occupied/unoccupied

	if not grabbed: # If the frame could not be grabbed, then we have reached the end of the video
		break

	delta_value = 0 # Delta Value for storing max continuous contour area for current frame

	frame = imutils.resize(frame, height=TARGET_HEIGHT) # Resize frame to 360p. Alternative resizing method:
	height, width = frame.shape[:2] # Get video height and width  from first frame(size)

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert frame to grayscale

	gray = cv2.bilateralFilter(gray,9,75,75) # Blur current frame with Bilateral Filter for noise reduction

	if referenceFrame is None: # If Reference Frame is None, initialize it
		referenceFrame = gray
		continue

	frameDelta = cv2.absdiff(referenceFrame, gray) # Compute the absolute difference between the current frame and reference frame
	thresh = cv2.threshold(frameDelta, 12, 255, cv2.THRESH_BINARY)[1] # Apply OpenCV's threshold function to get binary frame

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
			motion_detected = 1 # Initialize delta situation

		# ----------------------------------------(START) NON-STATIONARY CAMERA SITUATION (START)----------------------------------------
		# ----------------------------------------(START) NON-STATIONARY CAMERA SITUATION (START)----------------------------------------
		# ----------------------------------------(START) NON-STATIONARY CAMERA SITUATION (START)----------------------------------------

		if delta_value > (height * width * float(NON_STATIONARY_PERCENTAGE) / float(100)): # If delta value is too much
			print "NON-STATIONARY" # PPROBABLY!!! There is a NON_STAIONARY CAMERA situation

			while True: # On this level it gets only one frame

				color = numpy.random.randint(0,255,(TRACKER_POINTS,3)) # Create some random colors

				ret, old_frame = camera.read() # Take first frame
				old_frame = imutils.resize(old_frame, height=TARGET_HEIGHT) # Resize frame to 360p. Alternative resizing method:
				old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY) # Convert previous frame to grayscale

				height, width = old_frame.shape[:2] # Get video height and width (size)



				# --------------------(START) CHECK STATIONARY CAMERA AT THE SAME TIME (START)--------------------

				gray = cv2.bilateralFilter(old_gray,9,75,75) # Blur current frame with Bilateral Filter for noise reduction

				if referenceFrame is None: # If Reference Frame is None, initialize it
					referenceFrame = gray
					continue

				frameDelta = cv2.absdiff(referenceFrame, gray) # Compute the absolute difference between the current frame and reference frame
				thresh = cv2.threshold(frameDelta, 12, 255, cv2.THRESH_BINARY)[1] # Apply OpenCV's threshold function to get binary frame

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
							#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw it on the frame
					delta_value = max(contour_area_stack) # Assign max contour area to delta value

					if delta_value <= (height * width * float(NON_STATIONARY_PERCENTAGE) / float(100)):
						print "BREAK 1"
						break

				# --------------------(END) CHECK STATIONARY CAMERA AT THE SAME TIME (END)--------------------




				# Create random points on frame
				p1 = numpy.random.randint(width, size=(TRACKER_POINTS, 1, 2))
				for y in p1: # Get y values one by one
					 if y[0][1] > height: # If there is a y value that greater than max height
						 y[0][1] = numpy.random.random_integers(height) # Random again this time with max height value
				p1 = p1.astype(numpy.float32) # Change numpy array's data type to float32

				mask = numpy.zeros_like(old_frame) # Create a mask image for drawing purposes (original frame)
				mask_delta = numpy.zeros_like(old_frame) # Create a mask image for drawing purposes (delta frame)
				mask_white = numpy.ones_like(old_frame) # Create a white mask image for cloning original frame
				white_color = numpy.array([255,255,255]) # Define color white

				total_crazy_lines = 0 # Crazy line counter

				most_common_angle = None # Most common angle in general optical flow in shot

				while True: # Loop over the frames of the video

					mask_biggest_contour = numpy.zeros_like(old_frame) # Create a mask image for drawing purposes (biggest contour frame)

					ret,frame = camera.read() # Take a new frame
					frame = imutils.resize(frame, height=TARGET_HEIGHT) # Resize frame to 360p. Alternative resizing method:
					frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert it to grayscale




					# --------------------(START) CHECK STATIONARY CAMERA AT THE SAME TIME (START)--------------------

					gray = cv2.bilateralFilter(old_gray,9,75,75) # Blur current frame with Bilateral Filter for noise reduction

					if referenceFrame is None: # If Reference Frame is None, initialize it
						referenceFrame = gray
						continue

					frameDelta = cv2.absdiff(referenceFrame, gray) # Compute the absolute difference between the current frame and reference frame
					thresh = cv2.threshold(frameDelta, 12, 255, cv2.THRESH_BINARY)[1] # Apply OpenCV's threshold function to get binary frame

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
								#cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw it on the frame
						delta_value = max(contour_area_stack) # Assign max contour area to delta value

						if delta_value <= (height * width * float(NON_STATIONARY_PERCENTAGE) / float(100)):
							print "BREAK 2"
							break

					# --------------------(END) CHECK STATIONARY CAMERA AT THE SAME TIME (END)--------------------






					delta_value = 0 # Delta Value for storing max continuous contour area for current frame

					p2, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p1, None, **lk_params) # Calculate optical flow (Lucas Kanade Optical Flow function of OpenCV)

					if p2 is None: # If there are not any points that coming from Lucas Kanade Optical Flow function of OpenCV
						break      # Break the loop to reconstruct the optical flow

					# Select good points
					good_points2 = p2[st==1]
					good_points1 = p1[st==1]

					angles_array = [] # Angle list of all newly created tiny lines

					for i,(good_point2,good_point1) in enumerate(zip(good_points2,good_points1)): # Get point pairs one by one

						# Get coordinates of points
						x2,y2 = good_point2.ravel() # New point
						x1,y1 = good_point1.ravel() # Previous point

						distance = math.hypot(x2 - x1, y2 - y1) # Length of the tiny line between these two points.

						if distance >= CRAZY_LINE_DISTANCE: # If the line is not that "tiny" it's CRAZY! xD
							total_crazy_lines += 1          # Then increase total crazy line counter's value

						angle = math.atan2(y2-y1, x2-x1) # Calculate tangent value of the line (returns Radian)
						angle = math.degrees(angle)      # Radian to Degree
						angle = round(angle)             # Round up the degree
						angles_array.append(angle)       # Append the degree to Angle List

						if most_common_angle != None: # If there is a most common angle value
							if abs(most_common_angle - angle) > ABSDIFF_ANGLE: # If Absolute Difference between most common angle and the current line's angle greater than ABDSDIFF_ANGLE value, this line is inconsistent to current general optical flow
								cv2.line(mask_delta, (x2,y2),(x1,y1), white_color, LINE_THICKNESS) # Then draw a white line to mask_delta

						cv2.line(mask, (x2,y2),(x1,y1), color[i].tolist(), 1) # In every frame draw the colored lines to original frame for better understanding (optional)

					if angles_array: # If angles_array is not empty
						most_common_angle = Counter(angles_array).most_common()[0][0] # Find most common angle value in Angle List

					mask_delta_gray = cv2.cvtColor(mask_delta, cv2.COLOR_BGR2GRAY) # Convert mask_delta to grayscale
					thresh = cv2.threshold(mask_delta_gray, 12, 255, cv2.THRESH_BINARY)[1] # Apply OpenCV's threshold function to get binary frame
					thresh = cv2.dilate(thresh, None, iterations=1) # Dlation to increase white region for surrounding pixels

					# Find contours on thresholded image
					(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

					contour_area_stack = [] # List of contour areas's values
					contour_dictionary = {} # Dictionary of contours key = 'contour area' & value = 'contour coordinates (x,y,w,h)'
					biggest_contour_coordinates = None # Biggest contour coordinate

					frame_final_form = cv2.add(frame,mask_white)

					# Loop over the contours
					if cnts:
						for c in cnts: # Contour in Contours
							contour_area_stack.append(cv2.contourArea(c)) # Calculate contour area and append to contour stack
							if cv2.contourArea(c) > args["min_area"]: # If contour area greater than min area
								(x, y, w, h) = cv2.boundingRect(c) # Compute the bounding box for this contour
								cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw it on the frame
								contour_dictionary[cv2.contourArea(c)] = (x, y, w, h) # Add a key - value pair to contour dictionary
						delta_value = max(contour_area_stack) # Assign max contour area to delta value

						if contour_dictionary: # If contour dictionary is not empty
							biggest_contour_coordinates = contour_dictionary[delta_value] # Get coordinates of biggest contour

						if biggest_contour_coordinates: # If we have the coordinates it means there is a contour in the frame at the same time
							# Parse the coordinates
							x = biggest_contour_coordinates[0]
							y = biggest_contour_coordinates[1]
							w = biggest_contour_coordinates[2]
							h = biggest_contour_coordinates[3]
							cv2.rectangle(mask_biggest_contour, (x, y), (x + w, y + h), (255, 255, 255), -1) # Draw only one white rectange

					if delta_value > (height * width / DELTA_LIMIT_DIVISOR): # If delta value is too much
						break # Then break

					if len(contour_dictionary) > CONTOUR_LIMIT: # PROBABLY!!! There is a ZOOM, ZOOM + PAN, ZOOM + TILT, ZOOM + ROLL situation (Not just PAN, TILT, ROLL)
						# Then restart angle calculation. This time divide frame to quarters

						total_crazy_lines = 0 # Crazy line counter
						most_common_angle1 = None # Most common angle in general optical flow in shot
						angles_array1 = [] # Angle list of all newly created tiny lines
						most_common_angle2 = None # Most common angle in general optical flow in shot
						angles_array2 = [] # Angle list of all newly created tiny lines
						most_common_angle3 = None # Most common angle in general optical flow in shot
						angles_array3 = [] # Angle list of all newly created tiny lines
						most_common_angle4 = None # Most common angle in general optical flow in shot
						angles_array4 = [] # Angle list of all newly created tiny lines
						mask_delta = numpy.zeros_like(old_frame) # Create a mask image for drawing purposes (delta frame)

						for i,(good_point2,good_point1) in enumerate(zip(good_points2,good_points1)): # Get point pairs one by one

							# Get coordinates of points
							x2,y2 = good_point2.ravel() # New point
							x1,y1 = good_point1.ravel() # Previous point

							distance = math.hypot(x2 - x1, y2 - y1) # Length of the tiny line between these two points.

							if distance >= CRAZY_LINE_DISTANCE: # If the line is not that "tiny" it's CRAZY! xD
								total_crazy_lines += 1          # Then increase total crazy line counter's value

							angle = math.atan2(y2-y1, x2-x1) # Calculate tangent value of the line (returns Radian)
							angle = math.degrees(angle)      # Radian to Degree
							angle = round(angle)             # Round up the degree

							if (x1 <= (width / 2)) and (y1 <= (height / 2)):
								angles_array1.append(angle)       # Append the degree to Angle List
								if most_common_angle1 != None: # If there is a most common angle value
									if abs(most_common_angle1 - angle) > ABSDIFF_ANGLE: # If Absolute Difference between most common angle and the current line's angle greater than ABDSDIFF_ANGLE value, this line is inconsistent to current general optical flow
										cv2.line(mask_delta, (x2,y2),(x1,y1), white_color, LINE_THICKNESS) # Then draw a white line to mask_delta
							if (x1 >= (width / 2)) and (y1 <= (height / 2)):
								angles_array2.append(angle)       # Append the degree to Angle List
								if most_common_angle2 != None: # If there is a most common angle value
									if abs(most_common_angle2 - angle) > ABSDIFF_ANGLE: # If Absolute Difference between most common angle and the current line's angle greater than ABDSDIFF_ANGLE value, this line is inconsistent to current general optical flow
										cv2.line(mask_delta, (x2,y2),(x1,y1), white_color, LINE_THICKNESS) # Then draw a white line to mask_delta
							if (x1 <= (width / 2)) and (y1 >= (height / 2)):
								angles_array3.append(angle)       # Append the degree to Angle List
								if most_common_angle3 != None: # If there is a most common angle value
									if abs(most_common_angle3 - angle) > ABSDIFF_ANGLE: # If Absolute Difference between most common angle and the current line's angle greater than ABDSDIFF_ANGLE value, this line is inconsistent to current general optical flow
										cv2.line(mask_delta, (x2,y2),(x1,y1), white_color, LINE_THICKNESS) # Then draw a white line to mask_delta
							if (x1 >= (width / 2)) and (y1 >= (height / 2)):
								angles_array4.append(angle)       # Append the degree to Angle List
								if most_common_angle3 != None: # If there is a most common angle value
									if abs(most_common_angle3 - angle) > ABSDIFF_ANGLE: # If Absolute Difference between most common angle and the current line's angle greater than ABDSDIFF_ANGLE value, this line is inconsistent to current general optical flow
										cv2.line(mask_delta, (x2,y2),(x1,y1), white_color, LINE_THICKNESS) # Then draw a white line to mask_delta

							cv2.line(mask, (x2,y2),(x1,y1), color[i].tolist(), 1) # In every frame draw the colored lines to original frame for better understanding (optional)

						if angles_array1: # If angles_array is not empty
							most_common_angle1 = Counter(angles_array1).most_common()[0][0] # Find most common angle value in Angle List
						if angles_array2: # If angles_array is not empty
							most_common_angle2 = Counter(angles_array2).most_common()[0][0] # Find most common angle value in Angle List
						if angles_array3: # If angles_array is not empty
							most_common_angle3 = Counter(angles_array3).most_common()[0][0] # Find most common angle value in Angle List
						if angles_array4: # If angles_array is not empty
							most_common_angle4 = Counter(angles_array4).most_common()[0][0] # Find most common angle value in Angle List


						mask_delta_gray = cv2.cvtColor(mask_delta, cv2.COLOR_BGR2GRAY) # Convert mask_delta to grayscale
						thresh = cv2.threshold(mask_delta_gray, 12, 255, cv2.THRESH_BINARY)[1] # Apply OpenCV's threshold function to get binary frame
						thresh = cv2.dilate(thresh, None, iterations=1) # Dlation to increase white region for surrounding pixels

						# Find contours on thresholded image
						(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

						contour_area_stack = [] # List of contour areas's values
						contour_dictionary = {} # Dictionary of contours key = 'contour area' & value = 'contour coordinates (x,y,w,h)'
						biggest_contour_coordinates = None # Biggest contour coordinate

						frame_final_form = cv2.add(frame,mask_white)

						# Loop over the contours
						if cnts:
							for c in cnts: # Contour in Contours
								contour_area_stack.append(cv2.contourArea(c)) # Calculate contour area and append to contour stack
								if cv2.contourArea(c) > args["min_area"]: # If contour area greater than min area
									(x, y, w, h) = cv2.boundingRect(c) # Compute the bounding box for this contour
									cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw it on the frame
									contour_dictionary[cv2.contourArea(c)] = (x, y, w, h) # Add a key - value pair to contour dictionary
							delta_value = max(contour_area_stack) # Assign max contour area to delta value

							if contour_dictionary: # If contour dictionary is not empty
								biggest_contour_coordinates = contour_dictionary[delta_value] # Get coordinates of biggest contour

							if biggest_contour_coordinates: # If we have the coordinates it means there is a contour in the frame at the same time
								# Parse the coordinates
								x = biggest_contour_coordinates[0]
								y = biggest_contour_coordinates[1]
								w = biggest_contour_coordinates[2]
								h = biggest_contour_coordinates[3]
								cv2.rectangle(mask_biggest_contour, (x, y), (x + w, y + h), (255, 255, 255), -1) # Draw only one white rectange

						if delta_value > (height * width / DELTA_LIMIT_DIVISOR): # If delta value is too much
							break # Then break

					else: # There is just a PAN, TILT, ROLL situation. Don't touch anything.
						pass

					mask_biggest_contour_gray = cv2.cvtColor(mask_biggest_contour, cv2.COLOR_BGR2GRAY) # Convert mask_biggest_contour to grayscale
					thresh_biggest_contour = cv2.threshold(mask_biggest_contour_gray, 12, 255, cv2.THRESH_BINARY)[1] # Apply OpenCV's threshold function to get binary frame

					thresh_final_form = cv2.bitwise_and(thresh,thresh, mask= thresh_biggest_contour) # Bitwise and - biggest contour and tresh lines
					thresh_final_form = cv2.dilate(thresh_final_form, None, iterations=1) # Dlation to increase white region for surrounding pixels

					frameDelta = cv2.bitwise_and(frame_final_form,frame_final_form, mask= thresh_final_form) # Bitwise and - to get delta frame

					if total_crazy_lines >= CRAZY_LINE_LIMIT: # If amout of total crazy lines is greater than CRAZY_LINE_LIMIT
						break # Break the loop to reconstruct the optical flow

					frame_with_mask = cv2.add(frame,mask) # Add mask layer over frame
					cv2.imshow('Original Frame',frame_with_mask) # Show Original Frame
					cv2.imshow('Frame Threshhold',thresh_final_form) # Show Mask Delta Frame
					cv2.imshow('Frame Delta Colored',frameDelta) # Show Frame Delta

					k = cv2.waitKey(30) & 0xff # DEVELOPMENT
					if k == 27: # DEVELOPMENT PRESS ESC
						break # DEVELOPMENT BREAK

					old_gray = frame_gray.copy() # Update the previous frame
					p1 = good_points2.reshape(-1,1,2) # Update previous points


		# ----------------------------------------(END) NON-STATIONARY CAMERA SITUATION (END)----------------------------------------
		# ----------------------------------------(END) NON-STATIONARY CAMERA SITUATION (END)----------------------------------------
		# ----------------------------------------(END) NON-STATIONARY CAMERA SITUATION (END)----------------------------------------


	if motion_detected: # If we are on delta situation

		delta_value_stack.append(delta_value) # Append max contour area (delta value) to delta value stack

		if len(delta_value_stack) >= STABILIZATION_DETECTION: # If length of delta value stack is greater than or equal to STABILIZATION_DETECTION constant
			delta_value_stack.pop(0) # Pop first element of delta value stack
			# If minimum delta value is greater than (mean of last 5 frame - minimum area / 2) and maximum delta value is less than (mean of last 5 frame + minimum area / 2)
			if min(delta_value_stack) > (numpy.mean(delta_value_stack) - args["min_area"] / 2) and max(delta_value_stack) < (numpy.mean(delta_value_stack) + args["min_area"] / 2):
				motion_detected = 0 # Then video STABILIZED
				delta_value_stack = [] # Empty delta value stack
				referenceFrame = None  # Clear reference frame

	# Draw the text and timestamp on the frame
	cv2.putText(frame, "Diff    : {}".format(delta_value), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Thresh : {}".format(args["min_area"]), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Frame : {}".format(frame_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, "Delta  : {}".format(motion_detected), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

	# Show the frames and record if the user presses ESC or q
	cv2.imshow("Original Frame", frame)
	cv2.imshow("Frame Threshhold", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	cv2.imshow("Frame Delta Colored", frameDeltaColored)
	key = cv2.waitKey(1) & 0xFF

	# if the `ESC` or `q` key is pressed, break the loop
	if key == ord("q") or key == ord("\x1b"):
		break

cv2.destroyAllWindows() # Close any open windows
camera.release() # Release the capture device
