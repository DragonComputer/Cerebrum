import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import pysrt
import time

def start(text_input,language_analysis_stimulated):
	time.sleep(0.5)
	t0 = time.time()
	if os.path.exists(text_input): # If captions file exist
		subs = pysrt.open(text_input)
		i = 0
		while i < len(subs):
			time.sleep(0.5)
			if (time.time() - t0) > subs[i].start.seconds:
				print subs[i].text + "\n"
				i  += 1
	else: # If captions file doesn't exist
		raise ValueError('VTT file doesn\'t exist!') # Raise a ValueError
