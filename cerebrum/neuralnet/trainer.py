import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) # Append parent directory to system path for importing sibling modules in next lines
import crossmodal.cmops # BUILT-IN Crosmodal operations package
import hearing.memops # BUILT-IN Hearing Memory operations package
import vision.memops # BUILT-IN Vision Memory operations package
import time # Provides various time-related functions.
import pyaudio
import cv2 # (Open Source Computer Vision) is a library of programming functions mainly aimed at real-time computer vision.
import numpy # The fundamental package for scientific computing with Python.

CHUNK = 1024 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 2 # Number of channels
RATE = 44100 # Bit Rate of audio stream / Frame Rate

# MAIN CODE BLOCK
def start():
	pairs = crossmodal.cmops.get_pairs(str(datetime.date.today()), 0) # Get pairs starting from 0th line
	if not pairs:
		print "No pairs found."
		sys.exit()

	p = pyaudio.PyAudio() # Create a PyAudio session

	# Create a stream
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					output=True)

	# Loop over the pairs coming from CROSSMODAL
	for pair in pairs:
		   time.sleep(0.5) # Wait 0.5 seconds to prevent aggressive loop
		   if pair['direction'] == "hearing to vision":
				hearing_memory = hearing.memops.read_memory(str(datetime.date.today()),pair['timestamp1'])
				for chunky in hearing_memory['data']:
					stream.write(chunky)
				vision_memory = vision.memops.read_memory(str(datetime.date.today()),pair['timestamp2'])
				print len(vision_memory['thresh_binary'])
				for frame in vision_memory['thresh_binary']:
					frame = numpy.fromstring(frame, 'int16').reshape(640,360)
					print frame.shape
					#cv2.imshow("Frame Threshhold", frame)
					#cv2.moveWindow("Frame Threshhold",50,550)
