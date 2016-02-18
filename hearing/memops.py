import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
#import pyaudio

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

def read_memory(date_day,nth_record):
	MEM_FILE_PATH = "hearing/memory/" +  date_day + ".mem" # Path for mem file

	if os.path.exists(MEM_FILE_PATH):
		with open(MEM_FILE_PATH, 'r') as mem_file:
			memory = eval(mem_file.readlines()[nth_record])
			return memory
	else:
		raise ValueError('MEM file doesn\'t exist!')

if __name__ == "__main__":
	memory = read_memory(str(datetime.date.today()),-1)
	print memory['starting_time']
	print memory['ending_time']

	#CHUNK = 1024
	#WIDTH = 2
	#CHANNELS = 2
	#RATE = 44100
	#p = pyaudio.PyAudio()
	#stream = p.open(format=p.get_format_from_width(WIDTH), channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
	#for data in memory['data']:
		#stream.write(data)
