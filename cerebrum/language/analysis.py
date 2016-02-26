import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import pysrt
import multiprocessing
import time
import memops

def start(text_input,language_analysis_stimulated):
	time.sleep(0.5)
	t0 = time.time()
	if os.path.exists(text_input): # If captions file exist
		subs = pysrt.open(text_input)
		i = 0
		while i < len(subs):
			time.sleep(0.5)
			if (time.time() - t0) > subs[i].start.seconds:
				starting_time = datetime.datetime.now() # Starting time of the memory
				language_analysis_stimulated.value = 1 # Language analysis stimulated
				ending_time = starting_time + datetime.timedelta(seconds=(subs[i].end - subs[i].start).seconds)
				memory_data = subs[i].text.encode('ascii','ignore')
				print subs[i].text + "\n"
				process5 = multiprocessing.Process(target=memops.write_memory, args=(memory_data, starting_time, ending_time)) # Define write memory process
				process5.start() # Start write memory process
				language_analysis_stimulated.value = 0 # Language analysis NOT stimulated
				i  += 1
	else: # If captions file doesn't exist
		raise ValueError('VTT file doesn\'t exist!') # Raise a ValueError
