# USAGE
# python hearing/perception.py __trainingData/audio_name.wav

import pyaudio
import wave
import datetime
import os.path
import sys
import audioop
import numpy
import matplotlib.pyplot as plt
import threading
import imutils
import pyqtgraph as pg
from PyQt4 import QtCore, QtGui

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SAVE_PERIOD = 10
THRESHOLD = 1000
SILENCE_DETECTION = 5
EMPTY_CHUNK = chr(int('000000', 2)) * CHUNK * 4
WAVE_OUTPUT_FILENAME = "hearing/memory/" +  str(datetime.date.today()) + ".wav"

def save_file():
	if not os.path.isfile(WAVE_OUTPUT_FILENAME):
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes("")
		wf.close()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
	n_frames = wf.getnframes()
	previous_wav = wf.readframes(n_frames)
	wf.close()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(previous_wav + b''.join(frames))
	wf.close()

def draw_spectrum_analyzer():
	global all_frames
	global thresh_frames
	pw = pg.plot(title="Spectrum Analyzer")
	pg.setConfigOptions(antialias=True)
	pw.win.resize(800, 300)
	pw.win.move(300, 850)
	while True:
		data = ''.join(all_frames[-1:])
		data = numpy.fromstring(data, 'int16')
		pw.setMouseEnabled(y=False)
		pw.setYRange(0,1000)
		pw.setXRange(-(RATE/2), (RATE/2), padding=0)
		pwAxis = pw.getAxis("bottom")
		pwAxis.setLabel("Frequency [Hz]")
		T = 1.0/RATE
		N = data.shape[0]
		Pxx = (1./N)*numpy.fft.fft(data)
		f = numpy.fft.fftfreq(N,T)
		Pxx = numpy.fft.fftshift(Pxx)
		f = numpy.fft.fftshift(f)
		f = f.tolist()
		Pxx = (numpy.absolute(Pxx)).tolist()
		if thresh_frames[-1:] == EMPTY_CHUNK:
			pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('w', width=0.3, style=QtCore.Qt.SolidLine))
		else:
			pw.plot(x=f,y=Pxx, clear=True, pen=pg.mkPen('y', width=0.3, style=QtCore.Qt.SolidLine))
		pg.QtGui.QApplication.processEvents()

def draw_waveform():
	global all_frames
	global thresh_frames
	pw = pg.plot(title="Waveform")
	pg.setConfigOptions(antialias=True)
	pw.win.resize(1300, 160)
	pw.win.move(300, 850)
	pw.showAxis('bottom', False)
	while True:
		data = ''.join(all_frames[-50:])
		data = numpy.fromstring(data, 'int16')
		data2 = ''.join(thresh_frames[-50:])
		data2 = numpy.fromstring(data2, 'int16')
		pw.setRange(yRange=[-10000,10000])
		pw.plot(data, clear=True, pen=pg.mkPen('w', width=0.5, style=QtCore.Qt.DotLine))
		pw.plot(data2, pen=pg.mkPen('y', width=0.5, style=QtCore.Qt.DotLine))
		text = pg.TextItem("Seconds : " + str(int(len(all_frames)/(RATE/CHUNK))), color=(255, 255, 255))
		pw.addItem(text)
		text.setPos(500, 0)
		pg.QtGui.QApplication.processEvents()



if len(sys.argv) < 2:
	print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
	sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
				channels=wf.getnchannels(),
				rate=wf.getframerate(),
				output=True)

print("PROCESSING STARTED")

frames = []
all_frames = []
thresh_frames = []

#save_counter = 0
data = wf.readframes(CHUNK)
all_frames.append(data)
thresh_frames.append(EMPTY_CHUNK)

thread = threading.Thread(target=draw_waveform)
thread.daemon = True
thread.start()

while data != '':
	previous_data = data
	stream.write(data)
	data = wf.readframes(CHUNK)
	all_frames.append(data)
	thresh_frames.append(EMPTY_CHUNK)

	rms = audioop.rms(data, 2)
	#print rms
	if rms >= THRESHOLD:
		thresh_frames.pop()
		thresh_frames.pop()
		frames.append(previous_data)
		thresh_frames.append(previous_data)
		frames.append(data)
		thresh_frames.append(data)
		silence_counter = 0
		while silence_counter < SILENCE_DETECTION:
			stream.write(data)
			data = wf.readframes(CHUNK)
			all_frames.append(data)
			frames.append(data)
			thresh_frames.append(data)
			rms = audioop.rms(data, 2)
			#print rms
			if rms < THRESHOLD:
				silence_counter += 1
			else:
				silence_counter = 0
			sys.stdout.write("/")
			sys.stdout.flush()
		del frames[-(SILENCE_DETECTION-2):]
		del thresh_frames[-(SILENCE_DETECTION-2):]
		for i in range(SILENCE_DETECTION-2):
			thresh_frames.append(EMPTY_CHUNK)
		#save_file()
		frames = []
	sys.stdout.write(".")
	sys.stdout.flush()
	#save_counter += 1
	#if save_counter >= SAVE_PERIOD:
	#    save_counter = 0
	#    save_file()
	#    frames = []

print("\nPROCESSING ENDED")

stream.stop_stream()
stream.close()
p.terminate()
