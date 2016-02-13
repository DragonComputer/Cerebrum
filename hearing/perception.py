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
import imutils

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SAVE_PERIOD = 10
THRESHOLD = 1000
SILENCE_DETECTION = 3
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
	global thresh_frames
	fig = plt.figure(figsize=(20,2))
	while True:
		data = ''.join(all_frames[-50:])
		data = numpy.fromstring(data, 'int16')
		data2 = ''.join(thresh_frames[-50:])
		data2 = numpy.fromstring(data2, 'int16')
		plt.clf()
		plt.plot(data, color='silver', alpha=0.7, linestyle='dotted', drawstyle='steps-pre', antialiased="False", linewidth="0.5", rasterized="True")
		plt.plot(data2, color='#33cc33', alpha=0.7, linestyle='dotted', drawstyle='steps-pre', antialiased="False", linewidth="0.5", rasterized="True")
		ax = plt.gca()
		ax.axes.get_xaxis().set_visible(False)
		ax.axes.get_yaxis().set_visible(False)
		ax.patch.set_facecolor('#4d4d4d')
		#ax.patch.set_alpha(1.0)
		plt.ylim([-10000,10000])
		#plt.draw()
		plt.tight_layout()
		fig.canvas.draw()
		img = numpy.fromstring(fig.canvas.tostring_rgb(), dtype=numpy.uint8, sep='')
		img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
		img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		img = imutils.resize(img, height=160) # Resize frame to 160p.
		crop_img = img[15:145, 50:1350]
		cv2.putText(img, "Seconds : {}".format(int(len(all_frames)/43.06640625)), (70, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 155), 2)
		cv2.imshow("Waveform",crop_img)
		cv2.moveWindow("Waveform",300,850)
		cv2.waitKey(1)
		#plt.pause(0.1)



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
	#draw_spectrogram(all_frames)
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
			#draw_spectrogram(all_frames)
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
