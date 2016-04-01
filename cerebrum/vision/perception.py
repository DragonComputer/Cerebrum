__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import datetime # Supplies classes for manipulating dates and times in both simple and complex ways.
import imutils # A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization etc.
import time # Provides various time-related functions.
import cv2 # (Open Source Computer Vision) is a library of programming functions mainly aimed at real-time computer vision.
import numpy # The fundamental package for scientific computing with Python.
import os # Provides a portable way of using operating system dependent functionality.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
from cerebrum.vision.utilities import VisionMemoryUtil # BUILT-IN Memory operations package
import random # Pseudo-random number generators for various distributions.
import Tkinter

STABILIZATION_DETECTION = 5 # Number of frames to detect stabilization
NON_STATIONARY_PERCENTAGE = 70 # Percentage of frame for detecting NON-STATIONARY CAMERA. Like: ( height * width * float(X) / float(100) )
NON_ZERO_PERCENTAGE = 0 #  Percentage of frame(threshold) for detecting unnecessary movement
TARGET_HEIGHT = 360 # Number of horizontal lines for target video and processing. Like 720p, 360p etc.
MIN_AREA = 500 # Minimum area in square pixels to detect a motion
root = Tkinter.Tk()
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()

class VisionPerception():

	# MAIN CODE BLOCK
	@staticmethod
	def start(video_input, vision_perception_stimulated):

		if video_input == "0": # If the video_input is None, then we are reading from webcam
			camera = cv2.VideoCapture(0)
			time.sleep(0.25)
		else: # Otherwise, we are reading from a video file
			time.sleep(0.25)
			camera = cv2.VideoCapture(video_input)

		referenceFrame = None # Initialize the reference frame in the video stream

		starting_time = None
		memory_data_thresh = []
		memory_data_frameDeltaColored = []

		(grabbed, first_frame) = camera.read() # Grab the first frame

		height, width = first_frame.shape[:2] # Get video height and width  from first frame(size)
		#if not height == 720 or not width == 1280:
		if float(width) / float(height) != float(16) / float(9):
			if video_input == "0":
				# There is a STUPIDTY in here
				pass
			else:
				raise ValueError('Aspect ratio of input stream must be [16:9]')
			#warnings.warn("Aspect ratio of input stream must be [16:9]")

		frame_counter = 1 # Define frame counter variable
		motion_detected = 0 # Delta situation checking variable
		delta_value_stack = [] # List of delta values
		non_stationary_camera = 0
		motion_counter = 0
		nonzero_toolow = 0

		beginning_of_stream = datetime.datetime.now()
		while True: # Loop over the frames of the video

			(grabbed, frame) = camera.read() # Grab the current frame and initialize the occupied/unoccupied
			if not grabbed: # If the frame could not be grabbed, then we have reached the end of the video
				break
			frame_counter += 1 # Increase frame counter's value

			if video_input == "0":
				# If we are capturing from camera fuck Time Correction, there is also a STUPIDTY in here
				pass
			else:
				# -------------------- TIME CORRECTION --------------------
				time_delta = datetime.datetime.now() - beginning_of_stream
				current_time_of_realworld = time_delta.seconds + time_delta.microseconds / float(1000000)
				current_time_of_stream = frame_counter / camera.get(cv2.cv.CV_CAP_PROP_FPS)
				diff_of_time = current_time_of_stream - current_time_of_realworld
				if abs(diff_of_time) > (1 / camera.get(cv2.cv.CV_CAP_PROP_FPS)):
					if diff_of_time > 0:
						time.sleep(1 / camera.get(cv2.cv.CV_CAP_PROP_FPS))
					else:
						(grabbed, frame) = camera.read() # Grab the current frame and initialize the occupied/unoccupied
						if not grabbed: # If the frame could not be grabbed, then we have reached the end of the video
							break
						frame_counter += 1 # Increase frame counter's value
						continue
				# -------------------- TIME CORRECTION --------------------

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
					if cv2.contourArea(c) > MIN_AREA: # If contour area greater than min area
						(x, y, w, h) = cv2.boundingRect(c) # Compute the bounding box for this contour
						cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw it on the frame
				delta_value = max(contour_area_stack) # Assign max contour area to delta value

				if delta_value > MIN_AREA: # If max contour area (delta value) greater than min area
					motion_detected = 1 # Initialize delta situation

				if delta_value > (height * width * float(NON_STATIONARY_PERCENTAGE) / float(100)): # If delta value is too much
					non_stationary_camera = 1
					status_text = "WARNING: NON-STATIONARY CAMERA"
					frameDeltaColored = numpy.zeros_like(frame)
				else:
					non_stationary_camera = 0

				if cv2.countNonZero(thresh) < (height * width * float(NON_ZERO_PERCENTAGE) / float(100)): # If Non Zero count is too low
					nonzero_toolow = 1
					status_text = "WARNING: NON-ZERO TOO LOW"
					frameDeltaColored = numpy.zeros_like(frame)
				else:
					nonzero_toolow = 0

			if motion_detected: # If we are on delta situation

				if starting_time is None:
					starting_time = datetime.datetime.now() # Starting time of the memory
					vision_perception_stimulated.value = 1 # Vision perception stimulated

				if random.randint(0,2) == 1: # IMPORTANT
					memory_data_thresh.append(thresh.tostring())
					memory_data_frameDeltaColored.append(frameDeltaColored.tostring())
					#print type(memory_data_thresh[0])

				if not non_stationary_camera:
					status_text = "MOTION DETECTED"
				delta_value_stack.append(delta_value) # Append max contour area (delta value) to delta value stack

				if len(delta_value_stack) >= STABILIZATION_DETECTION: # If length of delta value stack is greater than or equal to STABILIZATION_DETECTION constant
					delta_value_stack.pop(0) # Pop first element of delta value stack
					# If minimum delta value is greater than (mean of last 5 frame - minimum area / 2) and maximum delta value is less than (mean of last 5 frame + minimum area / 2)
					if min(delta_value_stack) > (numpy.mean(delta_value_stack) - MIN_AREA / 2) and max(delta_value_stack) < (numpy.mean(delta_value_stack) + MIN_AREA / 2):
						ending_time = datetime.datetime.now() # Ending time of the memory
						vision_perception_stimulated.value = 0 # Vision perception NOT stimulated

						if memory_data_thresh and memory_data_frameDeltaColored:
							process4 = multiprocessing.Process(target=VisionMemoryUtil.add_memory, args=(memory_data_thresh, memory_data_frameDeltaColored, starting_time, ending_time)) # Define write memory process
							process4.start() # Start write memory process
						memory_data_thresh = []
						memory_data_frameDeltaColored = []
						starting_time = None

						motion_detected = 0 # Then video STABILIZED
						delta_value_stack = [] # Empty delta value stack
						referenceFrame = None  # Clear reference frame
						if not non_stationary_camera and not nonzero_toolow:
							motion_counter += 1
			else:
				if not non_stationary_camera and not nonzero_toolow:
					status_text = "MOTION UNDETECTED"
					frameDeltaColored = numpy.zeros_like(frame)

			# Draw the text and timestamp on the frame
			cv2.putText(frame, "Diff    : {}".format(delta_value), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
			cv2.putText(frame, "Thresh : {}".format(MIN_AREA), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
			cv2.putText(frame, "Frame : {}".format(frame_counter), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
			cv2.putText(frame, "Status  : {}".format(status_text), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
			cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

			# Show the frames and record if the user presses ESC or q
			cv2.imshow("Original Frame", frame)
			cv2.moveWindow("Original Frame",50 * SCREEN_WIDTH / 1920,100 * SCREEN_HEIGHT / 1080)
			cv2.imshow("Frame Threshhold", thresh)
			cv2.moveWindow("Frame Threshhold",50 * SCREEN_WIDTH / 1920,550 * SCREEN_HEIGHT / 1080)
			cv2.imshow("Frame Delta", frameDelta)
			cv2.moveWindow("Frame Delta",1200 * SCREEN_WIDTH / 1920,550 * SCREEN_HEIGHT / 1080)
			cv2.imshow("Frame Delta Colored", frameDeltaColored)
			cv2.moveWindow("Frame Delta Colored",1200 * SCREEN_WIDTH / 1920,100 * SCREEN_HEIGHT / 1080)
			key = cv2.waitKey(1) & 0xFF

			# if the `ESC` or `q` key is pressed, break the loop
			if key == ord("q") or key == ord("\x1b"):
				os.system("killall python") # Temporary line for practicality in DEVELOPMENT
				break

		cv2.destroyAllWindows() # Close any open windows
		camera.release() # Release the capture device
