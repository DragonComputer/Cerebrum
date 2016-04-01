__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

from cerebrum.hearing import HearingMemoryUtil # BUILT-IN Hearing Memory operations package
from cerebrum.vision import VisionMemoryUtil # BUILT-IN Vision Memory operations package
from cerebrum.language import LanguageMemoryUtil
import itertools # Implements a number of iterator building blocks inspired by constructs from APL, Haskell, and SML. Each has been recast in a form suitable for Python
from cerebrum.crossmodal.utilities import MapperUtil # BUILT-IN Crossmodal Memory operations package
import time # Provides various time-related functions.

class MapperStarters():

	# A function for checking two time intervals are overlapping or not --- http://stackoverflow.com/questions/35644301/checking-two-time-intervals-are-overlapping-or-not
	@staticmethod
	def overlap(first_inter,second_inter):
		for f,s in ((first_inter,second_inter), (second_inter,first_inter)):
			#Will check both ways
			for time in (f["starting_time"], f["ending_time"]):
				if s["starting_time"] < time < s["ending_time"]:
					return True
			return False

	@staticmethod
	def startHV():
		# Loop over the timestamps coming from HEARING & VISION
		while True:
			time.sleep(5) # Wait 5 seconds to prevent aggressive loop
			hearing_timestamps = HearingMemoryUtil.get_timestamps() # Get hearing timestamps starting from 0th line
			if not hearing_timestamps:
				continue
			vision_timestamps = VisionMemoryUtil.get_timestamps() # Get vision timestamps starting from 0th line
			if not vision_timestamps:
				continue

			# Cheking all possible combinations for overlapping --- http://stackoverflow.com/questions/35644301/checking-two-time-intervals-are-overlapping-or-not
			for (i1,interval1),(i2,interval2) in itertools.product(enumerate(hearing_timestamps),enumerate(vision_timestamps)): # Cartesian product of enumareted input iterables
				if MapperStarters.overlap(interval1,interval2): # If interval1 and interval2 is overlapping
					MapperUtil.add_pair(interval1['starting_time'], interval2['starting_time'], "H2V") # Write a H2V pair
					MapperUtil.add_pair(interval2['starting_time'], interval1['starting_time'], "V2H") # Write a V2H pair

	@staticmethod
	def startHL():
		# Loop over the timestamps coming from HEARING & LANGUAGE
		while True:
			time.sleep(5) # Wait 5 seconds to prevent aggressive loop
			hearing_timestamps = HearingMemoryUtil.get_timestamps() # Get hearing timestamps starting from 0th line
			if not hearing_timestamps:
				continue
			language_timestamps = LanguageMemoryUtil.get_timestamps() # Get language timestamps starting from 0th line
			if not language_timestamps:
				continue

			# Cheking all possible combinations for overlapping --- http://stackoverflow.com/questions/35644301/checking-two-time-intervals-are-overlapping-or-not
			for (i1,interval1),(i2,interval2) in itertools.product(enumerate(hearing_timestamps),enumerate(language_timestamps)): # Cartesian product of enumareted input iterables
				if MapperStarters.overlap(interval1,interval2): # If interval1 and interval2 is overlapping
					MapperUtil.add_pair(interval1['starting_time'], interval2['starting_time'], "H2L") # Write a H2L pair
					MapperUtil.add_pair(interval2['starting_time'], interval1['starting_time'], "L2H") # Write a L2H pair

	@staticmethod
	def startVL():
		# Loop over the timestamps coming from VISION & LANGUAGE
		while True:
			time.sleep(5) # Wait 5 seconds to prevent aggressive loop
			vision_timestamps = VisionMemoryUtil.get_timestamps() # Get vision timestamps starting from 0th line
			if not vision_timestamps:
				continue
			language_timestamps = LanguageMemoryUtil.get_timestamps() # Get language timestamps starting from 0th line
			if not language_timestamps:
				continue

			# Cheking all possible combinations for overlapping --- http://stackoverflow.com/questions/35644301/checking-two-time-intervals-are-overlapping-or-not
			for (i1,interval1),(i2,interval2) in itertools.product(enumerate(vision_timestamps),enumerate(language_timestamps)): # Cartesian product of enumareted input iterables
				if MapperStarters.overlap(interval1,interval2): # If interval1 and interval2 is overlapping
					MapperUtil.add_pair(interval1['starting_time'], interval2['starting_time'], "V2L") # Write a V2L pair
					MapperUtil.add_pair(interval2['starting_time'], interval1['starting_time'], "L2V") # Write a L2V pair
