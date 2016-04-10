__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
from cerebrum.crossmodal import MapperUtil # BUILT-IN Crosmodal operations package
from cerebrum.hearing import HearingPerception, HearingMemoryUtil # BUILT-IN Hearing Memory perception package
from cerebrum.vision import VisionPerception, VisionMemoryUtil # BUILT-IN Vision Memory operations package
from cerebrum.language import LanguageAnalyzer, LanguageMemoryUtil # BUILT-IN Language Memory operations package
import time # Provides various time-related functions.
import pyaudio
import cv2 # (Open Source Computer Vision) is a library of programming functions mainly aimed at real-time computer vision.
import numpy # The fundamental package for scientific computing with Python.
from pybrain.datasets import SequentialDataSet
from itertools import cycle
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import LSTMLayer
from pybrain.supervised import RPropMinusTrainer
from sys import stdout
import matplotlib.pyplot as plt
import rethinkdb as r # Rethinkdb Python driver
from sklearn import datasets, linear_model

CHUNK = 1024 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 2 # Number of channels
RATE = 44100 # Bit Rate of audio stream / Frame Rate

class NeuralWeaver():

	# MAIN CODE BLOCK
	@staticmethod
	def start():
		pairs = MapperUtil.get_allpairs() # Get pairs starting from 0th line
		if not pairs:
			print ("No pairs found.")
			sys.exit()

		p = pyaudio.PyAudio() # Create a PyAudio session

		# Create a stream
		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						output=True)

		#h2v_net = buildNetwork(2048, 5, 230400, hiddenclass=LSTMLayer, outputbias=False, recurrent=True)
		#data = [1] * 3 + [2] * 3
		# Loop over the pairs coming from CROSSMODAL
		for pair in pairs:
			   #time.sleep(0.5) # Wait 0.5 seconds to prevent aggressive loop
			   print pair

			   if pair['direction'] == "H2V":
				   print "____________________________________________________________\n"
				   print pair['timestamp1']

				   hearing_memory = HearingMemoryUtil.get_memory(pair['timestamp1'])
				   hearing_memory = hearing_memory.next()['data']
				   #print hearing_memory.next()['data']
				   #chunky_array = numpy.fromstring(hearing_memory.next()['data'], 'int16')
				   #print chunky_array
				   stream.write(hearing_memory)

				   numpy_audio = numpy.fromstring(hearing_memory, numpy.uint8)
				   print numpy_audio
				   print "Audio: ",numpy_audio.shape


				   vision_memory = VisionMemoryUtil.get_memory(pair['timestamp2'])
				   vision_memory = vision_memory.next()

				   frame_amodal = numpy.fromstring(vision_memory['amodal'], numpy.uint8)
				   print "Frame Threshold: ",frame_amodal.shape
				   cv2.imshow("Frame Threshhold", frame_amodal.reshape(360,640))
				   cv2.moveWindow("Frame Threshhold",50,100)

				   frame_color = numpy.fromstring(vision_memory['color'], numpy.uint8)
				   print "Frame Delta Colored: ",frame_color.shape
				   cv2.imshow("Frame Delta Colored", frame_color.reshape(360,640,3))
				   cv2.moveWindow("Frame Delta Colored",1200,100)
				   key = cv2.waitKey(500) & 0xFF
				   #time.sleep(2.0)

				   regr = linear_model.LinearRegression()
				   regr.fit(numpy_audio, frame_amodal)

				   '''
					#ds = SequentialDataSet(2048, 230400)
					hearing_memory = HearingMemoryUtil.get_memory(pair['timestamp1'])
					vision_memory = VisionMemoryUtil.get_memory(pair['timestamp2'])
					if not vision_memory:
						continue
					#for mem in hearing_memory:
					#	print mem


					hearing_data = numpy.fromstring((dict(hearing_memory))['data'], 'int16')
					for chunky in hearing_data:
						chunky_array = numpy.fromstring(chunky, 'int16')
						print (chunky_array)
						#ds.addSample(chunky_array, numpy.fromstring(vision_memory['amodal'][0], numpy.uint8))
						stream.write(chunky)
					#print len(vision_memory['amodal'])
					for frame in vision_memory['amodal']:
						frame = numpy.fromstring(frame, numpy.uint8).reshape(360,640)
						#print frame.shape
						cv2.imshow("Frame Threshhold", frame)
						cv2.moveWindow("Frame Threshhold",50,100)
						key = cv2.waitKey(1) & 0xFF
					for frame in vision_memory['color']:
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
					'''
