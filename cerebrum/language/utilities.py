__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

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

class LanguageMemoryUtil():

	# Add a memory function
	@staticmethod
	def add_memory(data, starting_time, ending_time):
		conn = r.connect("localhost", 28015)
		r.db('test').table("language_memory").insert([
			{ "starting_time": starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "ending_time": ending_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "data": r.binary(data)
			}
		]).run(conn)
		r.db('test').table("language_timestamps").insert([
			{ "starting_time": starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "ending_time": ending_time.strftime("%Y-%m-%d %H:%M:%S.%f")
			}
		]).run(conn)
		conn.close()

	# Get a memory function
	@staticmethod
	def get_memory(starting_time):
		conn = r.connect("localhost", 28015)
		cursor = r.db('test').table("language_memory").filter({'starting_time': starting_time}).run(conn)
		conn.close()
		return cursor

	# Get timestamps function
	@staticmethod
	def get_timestamps():
		conn = r.connect("localhost", 28015)
		cursor = r.db('test').table("language_timestamps").run(conn)
		conn.close()
		return cursor

# Example USAGE block. NOT FUNCTIONAL
if __name__ == "__main__":
	timestamp_list = LanguageMemoryUtil.get_timestamps(str(datetime.date.today()))
	#for timestamp in timestamp_list:
		#print "--------------------------"
		#print timestamp['starting_time']
		#print timestamp['ending_time']
	print len(timestamp_list)
	memory = LanguageMemoryUtil.get_memory(str(datetime.date.today()), timestamp_list[-3]['starting_time'])
	print len(memory['data'])

	#CHUNK = 1024
	#WIDTH = 2
	#CHANNELS = 2
	#RATE = 44100
	#p = pyaudio.PyAudio()
	#stream = p.open(format=p.get_format_from_width(WIDTH), channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
	#for data in memory['data']:
		#stream.write(data)
