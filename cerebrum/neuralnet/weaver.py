from __future__ import print_function
import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
import cerebrum.crossmodal.cmops # BUILT-IN Crosmodal operations package
import cerebrum.hearing.memops # BUILT-IN Hearing Memory operations package
import cerebrum.hearing.perception # BUILT-IN Hearing Memory perception package
import cerebrum.vision.memops # BUILT-IN Vision Memory operations package
import time # Provides various time-related functions.
import pyaudio
import cv2 # (Open Source Computer Vision) is a library of programming functions mainly aimed at real-time computer vision.
import numpy # The fundamental package for scientific computing with Python.
from cerebrum.neuralnet.datasets.sequential import SequentialDataSet
from itertools import cycle
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.supervised import RPropMinusTrainer
from sys import stdout
import matplotlib.pyplot as plt

CHUNK = 1024 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 2 # Number of channels
RATE = 44100 # Bit Rate of audio stream / Frame Rate

# MAIN CODE BLOCK
def start():
	pairs = cerebrum.crossmodal.cmops.get_pairs(str(datetime.date.today()), 0) # Get pairs starting from 0th line
	if not pairs:
		print ("No pairs found.")
		sys.exit()

	p = pyaudio.PyAudio() # Create a PyAudio session

	# Create a stream
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					output=True)

	h2v_net = buildNetwork(2048, 5, 230400, hiddenclass=LSTMLayer, outputbias=False, recurrent=True)
	data = [1] * 3 + [2] * 3
	# Loop over the pairs coming from CROSSMODAL
	for pair in pairs:
		   #time.sleep(0.5) # Wait 0.5 seconds to prevent aggressive loop
		   if pair['direction'] == "hearing to vision":
				ds = SequentialDataSet(2048, 230400)
				hearing_memory = cerebrum.hearing.memops.read_memory(str(datetime.date.today()),pair['timestamp1'])
				vision_memory = cerebrum.vision.memops.read_memory(str(datetime.date.today()),pair['timestamp2'])
				if not vision_memory:
					continue
				for chunky in hearing_memory['data']:
					chunky_array = numpy.fromstring(chunky, 'int16')
					print (chunky_array)
					ds.addSample(chunky_array, numpy.fromstring(vision_memory['thresh_binary'][0], numpy.uint8))
					stream.write(chunky)
				#print len(vision_memory['thresh_binary'])
				for frame in vision_memory['thresh_binary']:
					frame = numpy.fromstring(frame, numpy.uint8).reshape(360,640)
					#print frame.shape
					cv2.imshow("Frame Threshhold", frame)
					cv2.moveWindow("Frame Threshhold",50,100)
					key = cv2.waitKey(1) & 0xFF
				for frame in vision_memory['frame_delta_colored']:
					frame = numpy.fromstring(frame, numpy.uint8).reshape(360,640,3)
					#print frame.shape
					cv2.imshow("Frame Delta Colored", frame)
					cv2.moveWindow("Frame Delta Colored",1200,100)
					key = cv2.waitKey(1) & 0xFF

				trainer = RPropMinusTrainer(h2v_net, dataset=ds)
				train_errors = [] # save errors for plotting later
				EPOCHS_PER_CYCLE = 5
				CYCLES = 100
				EPOCHS = EPOCHS_PER_CYCLE * CYCLES
				for i in xrange(CYCLES):
					t0 = time.time() # Initiation time
					trainer.trainEpochs(EPOCHS_PER_CYCLE)
					train_errors.append(trainer.testOnData())
					epoch = (i+1) * EPOCHS_PER_CYCLE
					#print (time.time() - t0) # Elapsed time
					print("\r epoch {}/{} --- {}".format(epoch, EPOCHS, (time.time() - t0)), end="")
					stdout.flush()

				print()
				print("final error =", train_errors[-1])
