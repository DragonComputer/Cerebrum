# USAGE
# python hearing/perception.py __trainingData/audio_name.wav

import pyaudio # Provides Python bindings for PortAudio, the cross platform audio API
import wave # Provides a convenient interface to the WAV sound format
import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
import audioop # Operates on sound fragments consisting of signed integer samples 8, 16 or 32 bits wide, stored in Python strings.
import numpy # The fundamental package for scientific computing with Python.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import imutils # A series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization etc.
import pyqtgraph as pg # A pure-python graphics and GUI library built on PyQt4 / PySide and numpy
from PyQt4 import QtCore, QtGui # A comprehensive set of Python bindings for Digia's Qt cross platform GUI toolkit.
import time # Provides various time-related functions.

CHUNK = 1024 # Smallest unit of audio. 1024 bytes
FORMAT = pyaudio.paInt16 # Data format
CHANNELS = 2 # Number of channels
RATE = 44100 # Bit Rate of audio stream / Frame Rate
THRESHOLD = 1000 # Threshhold value for detecting stimulant
SILENCE_DETECTION = 5 # Wait number of frames to decide whether it fell silent or not
EMPTY_CHUNK = chr(int('000000', 2)) * CHUNK * 4 # Create an empty unit of audio for just once
WAVE_OUTPUT_FILENAME = "hearing/memory/" +  str(datetime.date.today()) + ".wav" # Example path if saving needed

# A function that will save recordings to a file
def save_file():
	if not os.path.isfile(WAVE_OUTPUT_FILENAME): # If there is not such a file
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # Create the file
		wf.setnchannels(CHANNELS) # Set number of channels
		wf.setsampwidth(p.get_sample_size(FORMAT)) # Set sampling format
		wf.setframerate(RATE) # Set Bit Rate / Frame Rate
		wf.writeframes("") # Write nothing
		wf.close() # Close the session

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb') # Open the file with only read permission
	n_frames = wf.getnframes() # Get all frames in it
	previous_wav = wf.readframes(n_frames) # Assign all frames to a variable
	wf.close() # Close the session

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb') # Open the file with write permission
	wf.setnchannels(CHANNELS) # Set number of channels
	wf.setsampwidth(p.get_sample_size(FORMAT)) # Set sampling format
	wf.setframerate(RATE) # Set Bit Rate / Frame Rate
	wf.writeframes(previous_wav + b''.join(frames)) # Write the all frames including previous ones
	wf.close() # Close the session

# A function that will compute frequency of chunk with Fourier Transform
def find_frequency(data):
	T = 1.0/RATE # Reciprocal of Bit Rate
	N = data.shape[0] # Number of rows in data(numpy array)
	Pxx = (1./N)*numpy.fft.fft(data) # Compute the one-dimensional n-point discrete Fourier Transform (DFT) of data with the efficient Fast Fourier Transform (FFT) algorithm [CT]
	f = numpy.fft.fftfreq(N,T) # Return the Discrete Fourier Transform sample frequencies
	Pxx = numpy.fft.fftshift(Pxx) # Shift the zero-frequency component to the center of the spectrum
	f = numpy.fft.fftshift(f) # Shift the zero-frequency component to the center of the spectrum
	return f.tolist(), (numpy.absolute(Pxx)).tolist() # Return the results

# A function that will draw a spectrum analyzer graphic to screen (PyQtGraph)
def draw_spectrum_analyzer(all_frames, thresh_frames):
	time.sleep(1) # Wait just one second
	pw = pg.plot(title="Spectrum Analyzer") # Window title
	pg.setConfigOptions(antialias=True) # Enable antialias for better resolution
	pw.win.resize(800, 300) # Define window size
	pw.win.move(540, 500) # Define window position
	while True: # Loop over the frames of the audio / data chunks
		data = ''.join(all_frames[-1:]) # Get only the last frame of all frames
		data = numpy.fromstring(data, 'int16') # Binary string to numpy int16 data format
		pw.setMouseEnabled(y=False) # Disable mouse
		pw.setYRange(0,1000) # Set Y range of graph
		pw.setXRange(-(RATE/16), (RATE/16), padding=0) # Set X range of graph relative to Bit Rate
		pwAxis = pw.getAxis("bottom") # Get bottom axis
		pwAxis.setLabel("Frequency [Hz]") # Set bottom axis label
		f, Pxx = find_frequency(data) # Call find frequency function
		try: # Try this block
			if thresh_frames[-1:][0] == EMPTY_CHUNK: # If last thresh frame is equal to EMPTY CHUNK
				pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('w', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with white pen
			else: # If last thresh frame is not equal to EMPTY CHUNK
				pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('y', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with yellow pen
		except IndexError: # If we are getting an IndexError because of this -> thresh_frames[-1:][0]
			pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('w', width=1.0, style=QtCore.Qt.SolidLine)) # Then plot with white pen
		pg.QtGui.QApplication.processEvents() # ???
		time.sleep(0.05) # Wait a few miliseconds

# A function that will draw a waveform graphic to screen (PyQtGraph)
def draw_waveform(all_frames, thresh_frames):
	time.sleep(1) # Wait just one second
	pw = pg.plot(title="Waveform") # Window title
	pg.setConfigOptions(antialias=True) # Enable antialias for better resolution
	pw.win.resize(1300, 160) # Define window size
	pw.win.move(300, 850) # Define window position
	pw.showAxis('bottom', False) # Hide bottom axis
	while True: # Loop over the frames of the audio / data chunks
		data = ''.join(all_frames[-20:]) # Join last 20 frames of all frames
		data = numpy.fromstring(data, 'int16') # Binary string to numpy int16 data format
		data2 = ''.join(thresh_frames[-20:]) # Join last 20 frames of thrsh frames
		data2 = numpy.fromstring(data2, 'int16') # Binary string to numpy int16 data format
		pw.setMouseEnabled(x=False) # Disable mouse
		pw.setRange(yRange=[-10000,10000]) # Set Y range of graph
		pw.plot(data, clear=True, pen=pg.mkPen('w', width=0.5, style=QtCore.Qt.DotLine)) # Plot all frames with white pen
		pw.plot(data2, pen=pg.mkPen('y', width=0.5, style=QtCore.Qt.DotLine)) # Plot thresh frames with yellow pen
		text = pg.TextItem("Seconds : " + str(int(len(all_frames)/(RATE/CHUNK))), color=(255, 255, 255)) # Define seconds according to number of total frames as a text
		pw.addItem(text) # Display seconds according to number of total frames
		text.setPos(500, 0) # Set text position
		pg.QtGui.QApplication.processEvents()
		time.sleep(0.05) # Wait a few miliseconds

# MAIN CODE BLOCK
if __name__ == "__main__":

	if len(sys.argv) < 2: # If system arguments less than 2
		print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0]) # Print a warning message
		sys.exit(-1) # Exit the program

	wf = wave.open(sys.argv[1], 'rb') # Open .wav file from given path in system arguments

	p = pyaudio.PyAudio() # Create a PyAudio session

	# Create a stream
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)

	manager = multiprocessing.Manager() # Shared memory space manager
	target_frames = [] # Define target frames array
	all_frames = manager.list() # Define all_frames array in shared memory
	thresh_frames = manager.list() # Define thresh_frames array in shared memory

	data = wf.readframes(CHUNK) # Get first data frame from .wav file
	all_frames.append(data) # Append to all frames
	thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

	process1 = multiprocessing.Process(target=draw_waveform, args=(all_frames, thresh_frames)) # Define draw waveform process
	process1.start() # Start draw waveform process

	process2 = multiprocessing.Process(target=draw_spectrum_analyzer, args=(all_frames, thresh_frames)) # Define draw spectrum analyzer process
	process2.start() # Start drar spectrum analyzer process

	# Loop over the frames of the audio / data chunks
	while data != '':
		previous_data = data # Get previous chunk that coming from end of the loop
		stream.write(data) # Monitor current chunk
		data = wf.readframes(CHUNK) # Read a new chunk from the stream
		all_frames.append(data) # Append this chunk to all frames
		thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY CHUNK to thresh frames

		rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk
		if rms >= THRESHOLD: # If Root Mean Square value is greater than THRESHOLD constant
			thresh_frames.pop() # Pop out last frame of thresh frames
			thresh_frames.pop() # Pop out last frame of thresh frames
			target_frames.append(previous_data) # Append previous chunk to target frames
			thresh_frames.append(previous_data) # APpend previos chunk to thresh frames
			target_frames.append(data) # Append current chunk to target frames
			thresh_frames.append(data) # Append current chunk to thresh frames
			silence_counter = 0 # Define silence counter
			while silence_counter < SILENCE_DETECTION: # While silence counter value less than SILENCE_DETECTION constant
				stream.write(data) # Monitor current chunk
				data = wf.readframes(CHUNK) # Read a new chunk from the stream
				all_frames.append(data) # Append this chunk to all frames
				target_frames.append(data) # Append this chunk to target frames
				thresh_frames.append(data) # Append this chunk to thresh frames
				rms = audioop.rms(data, 2) # Calculate Root Mean Square of current chunk again

				if rms < THRESHOLD: # If Root Mean Square value is less than THRESHOLD constant
					silence_counter += 1 # Then increase silence counter
				else: # Else
					silence_counter = 0 # Assign zero value to silence counter

			del target_frames[-(SILENCE_DETECTION-2):] # Delete last frames of target frames as much as SILENCE_DETECTION constant
			del thresh_frames[-(SILENCE_DETECTION-2):] # Delete last frames of thresh frames as much as SILENCE_DETECTION constant
			for i in range(SILENCE_DETECTION-2): # SILENCE_DETECTION constant times
				thresh_frames.append(EMPTY_CHUNK) # Append an EMPTY_CHUNK

			target_frames = [] # Empty target frames
			sys.stdout.write("HEARING STIMULI")
			sys.stdout.flush()

	stream.stop_stream() # Stop the stream
	stream.close() # Close the stream
	p.terminate() # Terminate the session
