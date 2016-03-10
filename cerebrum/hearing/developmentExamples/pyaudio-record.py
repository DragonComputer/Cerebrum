"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import wave
import datetime
import os.path
import sys
import audioop
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SAVE_PERIOD = 10
THRESHOLD = 1000
SILENCE_DETECTION = 20
WAVE_OUTPUT_FILENAME = "memory/" +  str(datetime.date.today()) + ".wav"

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






p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK)

print("* recording")

frames = []

#save_counter = 0
data = stream.read(CHUNK)
while True:
	previous_data = data
	start_time = time.time()
	data = stream.read(CHUNK)
	rms = audioop.rms(data, 2)
	#print rms
	if rms >= THRESHOLD:
		frames.append(previous_data)
		frames.append(data)
		silence_counter = 0
		while silence_counter < SILENCE_DETECTION:
			data = stream.read(CHUNK)
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
	print(time.time() - start_time)
	#save_counter += 1
	#if save_counter >= SAVE_PERIOD:
	#    save_counter = 0
	#    save_file()
	#    frames = []

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()
