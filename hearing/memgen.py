import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

class Memory(object):
	def __init__(self, starting_time, ending_time, data):
		self.starting_time = starting_time
		self.ending_time = ending_time
		self.data = data

def makeit_dict(obj):
	if isinstance(obj, set):
		return list(obj)
	return obj.__dict__

def write_memory(data, starting_time, ending_time):
	MEM_FILE_PATH = "hearing/memory/" +  str(datetime.date.today()) + ".mem" # Path for mem file

	memory = Memory(starting_time.strftime("%Y-%m-%d %H:%M:%S:%f"), ending_time.strftime("%Y-%m-%d %H:%M:%S:%f"), data)
	mode = 'a' if os.path.exists(MEM_FILE_PATH) else 'w'
	with open(MEM_FILE_PATH, mode) as mem_file:
		mem_file.write(str(makeit_dict(memory)) + '\n')
