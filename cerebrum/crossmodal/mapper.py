import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) # Append parent directory to system path for importing sibling modules in next lines
import hearing.memops # BUILT-IN Hearing Memory operations package
import vision.memops # BUILT-IN Vision Memory operations package
import itertools # Implements a number of iterator building blocks inspired by constructs from APL, Haskell, and SML. Each has been recast in a form suitable for Python
import cmops # BUILT-IN Crossmodal Memory operations package
import time # Provides various time-related functions.

# A function for checking two time intervals are overlapping or not --- http://stackoverflow.com/questions/35644301/checking-two-time-intervals-are-overlapping-or-not
def overlap(first_inter,second_inter):
	for f,s in ((first_inter,second_inter), (second_inter,first_inter)):
		#Will check both ways
		for time in (f["starting_time"], f["ending_time"]):
			if s["starting_time"] < time < s["ending_time"]:
				return True
		return False

# MAIN CODE BLOCK
def start():
	# Loop over the timestamps coming from HEARING & VISION
	while True:
		time.sleep(5) # Wait 5 seconds to prevent aggressive loop
		hearing_timestamps = hearing.memops.read_timestamps(str(datetime.date.today()), 0) # Get hearing timestamps starting from 0th line
		if not hearing_timestamps:
			continue
		vision_timestamps = vision.memops.read_timestamps(str(datetime.date.today()), 0) # Get vision timestamps starting from 0th line
		if not vision_timestamps:
			continue
		if cmops.read_pair(str(datetime.date.today()), -1): # If Pairs file exists
			last_pair = cmops.read_pair(str(datetime.date.today()), -1) # Get latest pair from file
		else: # If Pairs file doesn't exist
			last_pair = {} # Create a fake one
			last_pair['timestamp1'] = 0 # Assign lowest values to timestamps
			last_pair['timestamp2'] = 0 # Assign lowest values to timestamps

		# Cheking all possible combinations for overlapping --- http://stackoverflow.com/questions/35644301/checking-two-time-intervals-are-overlapping-or-not
		for (i1,int1),(i2,int2) in itertools.product(enumerate(hearing_timestamps),enumerate(vision_timestamps)): # Cartesian product of enumareted input iterables
			if hearing_timestamps[i1]['starting_time'] < last_pair['timestamp1'] or hearing_timestamps[i1]['starting_time'] < last_pair['timestamp2']: # If current hearing timestamp is earlier than last pair
				continue # Then continue
			if vision_timestamps[i2]['starting_time'] < last_pair['timestamp1'] or vision_timestamps[i2]['starting_time'] < last_pair['timestamp2']: # If current vision timestamp is earlier than last pair
				continue # Then continoue
			if overlap(int1,int2): # If interval1 and interval2 is overlapping
				cmops.write_pair(hearing_timestamps[i1]['starting_time'], vision_timestamps[i2]['starting_time'], "hearing to vision") # Write a hearing to vision pair
				cmops.write_pair(vision_timestamps[i2]['starting_time'], hearing_timestamps[i1]['starting_time'], "vision to hearing") # Write a vision to hearing pair
