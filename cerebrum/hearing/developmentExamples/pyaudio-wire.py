"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).
"""

import pyaudio
import time
import numpy as np
from matplotlib import pyplot as plt

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = ""

time.sleep(RECORD_SECONDS)

print("* recording finished")
print("* playing")

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames = frames + data
    stream.write(data, CHUNK)

print("* done")

numpydata = np.fromstring(frames, dtype=np.int16)

print len(numpydata)
print numpydata[100000]

# plot data
plt.plot(numpydata)
plt.show()

stream.stop_stream()
stream.close()

p.terminate()
