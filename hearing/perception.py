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
import cv2

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SAVE_PERIOD = 10
THRESHOLD = 1000
SILENCE_DETECTION = 5
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

def draw_spectrogram():
	global all_frames
	plt.figure(figsize=(2,4))
	while True:
		data = ''.join(all_frames[-50:])
		data = numpy.fromstring(data, 'int16')
		plt.specgram(data, NFFT=CHUNK, Fs=wf.getframerate(), noverlap=900, cmap=plt.cm.gray)
		plt.draw()
		plt.pause(0.2)

def draw_waveform():
	global all_frames
	plt.figure(figsize=(30,2))
	while True:
		data = ''.join(all_frames[-50:])
		data = numpy.fromstring(data, 'int16')
		plt.clf()
		plt.plot(data, color='silver', alpha=0.7, linestyle='dotted')
		ax = plt.gca()
		ax.patch.set_facecolor('black')
		ax.patch.set_alpha(0.5)
		plt.ylim([-10000,10000])
		plt.draw()
		plt.pause(0.05)



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

#save_counter = 0
data = wf.readframes(CHUNK)
all_frames.append(data)

thread = threading.Thread(target=draw_waveform)
thread.daemon = True
thread.start()

while data != '':
	previous_data = data
	stream.write(data)
	#draw_spectrogram(all_frames)
	data = wf.readframes(CHUNK)
	all_frames.append(data)
	rms = audioop.rms(data, 2)
	#print rms
	if rms >= THRESHOLD:
		frames.append(previous_data)
		frames.append(data)
		silence_counter = 0
		while silence_counter < SILENCE_DETECTION:
			stream.write(data)
			#draw_spectrogram(all_frames)
			data = wf.readframes(CHUNK)
			all_frames.append(data)
			frames.append(data)
			rms = audioop.rms(data, 2)
			#print rms
			if rms < THRESHOLD:
				silence_counter += 1
			else:
				silence_counter = 0
			sys.stdout.write("/")
			sys.stdout.flush()
		del frames[-(SILENCE_DETECTION-2):]
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
