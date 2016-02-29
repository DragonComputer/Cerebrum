import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import pysrt # SubRip (.srt) subtitle parser and writer
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import time # Provides various time-related functions.
import memops # BUILT-IN Memory operations package

#MAIN CODE BLOCK
def start(text_input,language_analysis_stimulated):
	time.sleep(0.3) # Wait 0.5 seconds for other processes's start
	t0 = time.time() # Initiation time
	if os.path.exists(text_input): # If captions file exist
		subs = pysrt.open(text_input) # Get whole subtitles
		i = 0 # Step counter
		while i < len(subs): # While step counter less than amount of subtitles
			time.sleep(0.5) # Wait 0.5 seconds to prevent aggressive loop
			if (time.time() - t0) > subs[i].start.seconds: # If current time is greater than subtitle's start
				starting_time = datetime.datetime.now() # Starting time of the memory
				language_analysis_stimulated.value = 1 # Language analysis stimulated
				ending_time = starting_time + datetime.timedelta(seconds=(subs[i].end - subs[i].start).seconds) # Calculate the ending time by subtitle's delta
				memory_data = subs[i].text.encode('ascii','ignore') # Encode subtitle's text by ascii and assign to memory data
				print subs[i].text + "\n" # Print subtitle's text
				process5 = multiprocessing.Process(target=memops.write_memory, args=(memory_data, starting_time, ending_time)) # Define write memory process
				process5.start() # Start write memory process
				language_analysis_stimulated.value = 0 # Language analysis NOT stimulated
				i  += 1 # Increase step counter
	else: # If captions file doesn't exist
		raise ValueError('VTT file doesn\'t exist!') # Raise a ValueError
