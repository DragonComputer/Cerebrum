import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import json

class Memory(object):
	def __init__(self, starting_time, ending_time, data):
		self.starting_time = starting_time
		self.ending_time = ending_time
		self.data = data

def jdefault(o):
	if isinstance(o, set):
		return list(o)
	return o.__dict__

def save_memory(data, starting_time, ending_time):
	JSON_FILE_PATH = "hearing/memory/" +  str(datetime.date.today()) + ".json" # Path for json file

	memory = Memory(starting_time.strftime("%Y-%m-%d %H:%M:%S"), ending_time.strftime("%Y-%m-%d %H:%M:%S"), data.decode('ISO-8859-1'))
	mode = 'a' if os.path.exists(JSON_FILE_PATH) else 'w'
	with open(JSON_FILE_PATH, mode) as json_file:
		#f.write(memory_data + "\n")
		json.dump(memory, json_file, default=jdefault)
		#pass
