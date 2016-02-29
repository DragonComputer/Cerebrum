import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

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

# Write a memory function
def write_memory(data, starting_time, ending_time):
	MEM_FILE_PATH = "cerebrum/hearing/memory/" +  str(datetime.date.today()) + ".mem" # Path for mem file
	TSTP_FILE_PATH = "cerebrum/hearing/memory/" +  str(datetime.date.today()) + ".tstp" # Path for tstp file

	memory = Memory(starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"), ending_time.strftime("%Y-%m-%d %H:%M:%S.%f"), data) # Create an object from Memory class
	mode = 'a' if os.path.exists(MEM_FILE_PATH) else 'w' # If memory file exist, file open mode will be append(a) else write(w)
	with open(MEM_FILE_PATH, mode) as mem_file: # Open file
		mem_file.write(str(makeit_dict(memory)) + '\n') # Write memory in only one line

	timestamp = Timestamp(starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"), ending_time.strftime("%Y-%m-%d %H:%M:%S.%f")) # Create an object from Timestamp class
	mode = 'a' if os.path.exists(TSTP_FILE_PATH) else 'w' # If timestamp file exist, file open mode will be append(a) else write(w)
	with open(TSTP_FILE_PATH, mode) as tstp_file: # Open file
		tstp_file.write(str(makeit_dict(timestamp)) + '\n') # Write timestamp in only one line

# Read a memory function
def read_memory(date_day,starting_time):
	MEM_FILE_PATH = "cerebrum/hearing/memory/" +  date_day + ".mem" # Path for mem file
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

# Read timestamps function
def read_timestamps(date_day,from_line=0):
	TSTP_FILE_PATH = "cerebrum/hearing/memory/" +  date_day + ".tstp" # Path for tstp file
	timestamp_list = []
	if os.path.exists(TSTP_FILE_PATH): # If timestamp file exist
		with open(TSTP_FILE_PATH, 'r') as tstp_file: # Open file
			for line in tstp_file.readlines()[from_line:]: # Get whole lines starting from that line, default zero
				timestamp = eval(line) # Evaluate the line, which will return a dictionary
				timestamp_list.append(timestamp) # Append timestamp to list in order
			return timestamp_list # Return timestamp list to call
	else: # If timestamp file doesn't exist
		return False

# Example USAGE block. NOT FUNCTIONAL
if __name__ == "__main__":
	timestamp_list = read_timestamps(str(datetime.date.today()))
	#for timestamp in timestamp_list:
		#print "--------------------------"
		#print timestamp['starting_time']
		#print timestamp['ending_time']
	print len(timestamp_list)
	memory = read_memory(str(datetime.date.today()), timestamp_list[-3]['starting_time'])
	print len(memory['data'])

	#CHUNK = 1024
	#WIDTH = 2
	#CHANNELS = 2
	#RATE = 44100
	#p = pyaudio.PyAudio()
	#stream = p.open(format=p.get_format_from_width(WIDTH), channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
	#for data in memory['data']:
		#stream.write(data)
