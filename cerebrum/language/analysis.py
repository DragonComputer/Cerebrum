__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import pysrt # SubRip (.srt) subtitle parser and writer
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import time # Provides various time-related functions.
from cerebrum.language.utilities import LanguageMemoryUtil # BUILT-IN Memory operations package

class LanguageAnalyzer():

	@staticmethod
	def word_to_phones(word):
		with open("cerebrum/language/dictionaries/en/cmudict-0.7b.txt") as infile:
			for row in infile:
				if row.split()[0] == word.upper():
					return " ".join(row.split()[1:])
			return ""

	#MAIN CODE BLOCK
	@staticmethod
	def start(text_input,language_analysis_stimulated):
		time.sleep(0.3) # Wait 0.5 seconds for other processes's start
		t0 = time.time() # Initiation time
		if os.path.exists(text_input): # If captions file exist
			subs = pysrt.open(text_input) # Get whole subtitles
			i = 0 # Step counter
			while i < len(subs): # While step counter less than amount of subtitles
				time.sleep(0.5) # Wait 0.5 seconds to prevent aggressive loop
				if (time.time() - t0) > subs[i].start.seconds: # If current time is greater than subtitle's start
					sub_starting_time = datetime.datetime.now() # Starting time of the memory
					language_analysis_stimulated.value = 1 # Language analysis stimulated
					sub_ending_time = sub_starting_time + datetime.timedelta(seconds=(subs[i].end - subs[i].start).seconds) # Calculate the ending time by subtitle's delta
					sub = subs[i].text.encode('ascii','ignore') # Encode subtitle's text by ascii and assign to sub variable
					sub = sub.translate(None, '!@#$?,')
					words = sub.split()
					phone_groups = []
					for word in words:
						phone_groups.append(LanguageAnalyzer.word_to_phones(word))
					phones = " ".join(phone_groups)
					phone_duration = datetime.timedelta(seconds=(subs[i].end - subs[i].start).seconds) / len(phones)
					starting_time = sub_starting_time
					for word_inphones in phone_groups:
						ending_time = starting_time + phone_duration * len(word_inphones.split())
						if ending_time <= sub_ending_time and word_inphones != "":
							process5 = multiprocessing.Process(target=LanguageMemoryUtil.add_memory, args=(word_inphones, starting_time, ending_time)) # Define write memory process
							process5.start() # Start write memory process
						starting_time = ending_time + datetime.timedelta(milliseconds=50)
					print subs[i].text + "\n" # Print subtitle's text
					print phones + "\n"
					print "-------------------------------------------------------------\n"

					language_analysis_stimulated.value = 0 # Language analysis NOT stimulated
					i  += 1 # Increase step counter
		else: # If captions file doesn't exist
			raise ValueError('VTT file doesn\'t exist!') # Raise a ValueError
