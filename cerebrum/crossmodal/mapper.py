__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
from cerebrum.hearing import HearingMemoryUtil # BUILT-IN Hearing Memory operations package
from cerebrum.vision import VisionMemoryUtil # BUILT-IN Vision Memory operations package
import itertools # Implements a number of iterator building blocks inspired by constructs from APL, Haskell, and SML. Each has been recast in a form suitable for Python
from cerebrum.crossmodal.utilities import MapperUtil # BUILT-IN Crossmodal Memory operations package
import time # Provides various time-related functions.

class MapperMain():

	# A function for checking two time intervals are overlapping or not --- http://stackoverflow.com/questions/35644301/checking-two-time-intervals-are-overlapping-or-not
	@staticmethod
	def overlap(first_inter,second_inter):
		for f,s in ((first_inter,second_inter), (second_inter,first_inter)):
			#Will check both ways
			for time in (f["starting_time"], f["ending_time"]):
				if s["starting_time"] < time < s["ending_time"]:
					return True
			return False

	# MAIN CODE BLOCK
	@staticmethod
	def start():
		# Loop over the timestamps coming from HEARING & VISION
		while True:
			time.sleep(5) # Wait 5 seconds to prevent aggressive loop
			hearing_timestamps = HearingMemoryUtil.read_timestamps(str(datetime.date.today()), 0) # Get hearing timestamps starting from 0th line
			if not hearing_timestamps:
				continue
			vision_timestamps = VisionMemoryUtil.read_timestamps(str(datetime.date.today()), 0) # Get vision timestamps starting from 0th line
			if not vision_timestamps:
				continue
			if MapperUtil.read_pair(str(datetime.date.today()), -1): # If Pairs file exists
				last_pair = MapperUtil.read_pair(str(datetime.date.today()), -1) # Get latest pair from file
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
				if MapperMain.overlap(int1,int2): # If interval1 and interval2 is overlapping
					MapperUtil.write_pair(hearing_timestamps[i1]['starting_time'], vision_timestamps[i2]['starting_time'], "hearing to vision") # Write a hearing to vision pair
					MapperUtil.write_pair(vision_timestamps[i2]['starting_time'], hearing_timestamps[i1]['starting_time'], "vision to hearing") # Write a vision to hearing pair
