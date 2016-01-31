"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import wave
import datetime
import os.path

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "auditory-memory/" +  str(datetime.date.today()) + ".wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

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
