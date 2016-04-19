__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
from cerebrum.crossmodal import MapperUtil # BUILT-IN Crosmodal operations package
from cerebrum.hearing import HearingPerception, HearingMemoryUtil # BUILT-IN Hearing Memory perception package
from cerebrum.vision import VisionPerception, VisionMemoryUtil # BUILT-IN Vision Memory operations package
from cerebrum.language import LanguageAnalyzer, LanguageMemoryUtil # BUILT-IN Language Memory operations package
#from cerebrum.neuralnet.utilities import NeuralNetUtil
import time # Provides various time-related functions.
import pyaudio
import cv2 # (Open Source Computer Vision) is a library of programming functions mainly aimed at real-time computer vision.
import numpy # The fundamental package for scientific computing with Python.
from hpelm import HPELM
import os.path

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

		#H2V_cursor = NeuralNetUtil.get_neurons("H2V")
		elmH2V = None

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
				   #print numpy_audio
				   print "Audio: ",numpy_audio.shape
				   #print numpy.transpose(numpy_audio.reshape((numpy_audio.shape[0],1))).shape


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

				   modulo = numpy_audio.shape[0] % RATE
				   numpy_audio = numpy_audio[:-modulo]
				   for one_second in numpy.array_split(numpy_audio, int(numpy_audio.shape[0] / RATE)):
					   X = numpy.transpose(one_second.reshape((one_second.shape[0],1)))
					   T = numpy.transpose(frame_amodal.reshape((frame_amodal.shape[0],1)))
					   X = X.astype(numpy.float32, copy=False)
					   T = T.astype(numpy.float32, copy=False)
					   X[0] = X[0] / X[0].max()
					   T[0] = T[0] / T[0].max()
					   print X.shape
					   print T.shape
					   if elmH2V is None:
						   elmH2V = HPELM(X.shape[1],T.shape[1])
						   if os.path.exists(os.path.expanduser("~/CerebralCortexH2V.pkl")):
							   #elmH2V.nnet.neurons = H2V_cursor.next()['neurons']
							   elmH2V.load(os.path.expanduser("~/CerebralCortexH2V.pkl"))
						   else:
							   elmH2V.add_neurons(100, "sigm")
					   elmH2V.train(X, T, "LOO")
					   print elmH2V.predict(X)
					   cv2.imshow(">>>PREDICTION<<<", numpy.transpose(elmH2V.predict(X)).reshape(360,640))
					   cv2.moveWindow(">>>PREDICTION<<<",50,550)

		print elmH2V.nnet.neurons
		elmH2V.save(os.path.expanduser("~/CerebralCortexH2V.pkl"))
		#NeuralNetUtil.write_neurons(elmH2V.nnet.neurons, "H2V")
