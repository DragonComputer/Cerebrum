__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import rethinkdb as r # Rethinkdb Python driver

# Memory class
class Memory(object):
	def __init__(self, starting_time, ending_time, data): # Initialize the object
		self.starting_time = starting_time # Starting time attribute
		self.ending_time = ending_time # Ending time attribute
		self.data = data # Data attribute

# Timestamp class
class Timestamp(object):
	def __init__(self, starting_time, ending_time): # Initialize the object
		self.starting_time = starting_time # Starting time attribute
		self.ending_time = ending_time # Ending time attribute

# Convert object to dictionary
def makeit_dict(obj):
	if isinstance(obj, set):
		return list(obj)
	return obj.__dict__

class HearingMemoryUtil():

	# Add a memory function
	@staticmethod
	def add_memory(data, starting_time, ending_time):
		conn = r.connect("localhost", 28015)
		r.db('test').table("hearing_memory").insert([
			{ "starting_time": starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "ending_time": ending_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "data": r.binary(data)
			}
		]).run(conn)
		r.db('test').table("hearing_timestamps").insert([
			{ "starting_time": starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "ending_time": ending_time.strftime("%Y-%m-%d %H:%M:%S.%f")
			}
		]).run(conn)
		conn.close()

	# Get a memory function
	@staticmethod
	def get_memory(date_day,starting_time):
		MEM_FILE_PATH = os.path.expanduser("~/Hippocampus/hearing/memory/" +  date_day + ".mem") # Path for mem file
		memory_list = []
		if os.path.exists(MEM_FILE_PATH): # If memory file exist
			with open(MEM_FILE_PATH, 'r') as mem_file: # Open file
				for line in mem_file.readlines(): # Get whole lines
					memory = eval(line) # Evaluate the line, which will return a dictionary
					if memory['starting_time'] == starting_time: # If current memory's starting time is equal to function's parameter
						return memory # Return current memory to call
				return False # Else return False
		else: # If memory file doesn't exist
			raise ValueError('MEM file doesn\'t exist!') # Raise a ValueError

	# Get timestamps function
	@staticmethod
	def get_timestamps():
		conn = r.connect("localhost", 28015)
		cursor = r.db('test').table("hearing_timestamps").run(conn)
		return cursor

# Example USAGE block. NOT FUNCTIONAL
if __name__ == "__main__":
	timestamp_list = HearingMemoryUtil().get_timestamps(str(datetime.date.today()))
	#for timestamp in timestamp_list:
		#print "--------------------------"
		#print timestamp['starting_time']
		#print timestamp['ending_time']
	print len(timestamp_list)
	memory = HearingMemoryUtil().get_memory(str(datetime.date.today()), timestamp_list[-3]['starting_time'])
	print len(memory['data'])

	#CHUNK = 1024
	#WIDTH = 2
	#CHANNELS = 2
	#RATE = 44100
	#p = pyaudio.PyAudio()
	#stream = p.open(format=p.get_format_from_width(WIDTH), channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
	#for data in memory['data']:
		#stream.write(data)
