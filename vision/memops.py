import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

# Memory class
class Memory(object):
	def __init__(self, starting_time, ending_time, thresh_binary, frame_delta_colored): # Initialize the object
		self.starting_time = starting_time # Starting time attribute
		self.ending_time = ending_time # Ending time attribute
		self.thresh_binary = thresh_binary # Thresh binary frame attribute
		self.frame_delta_colored = frame_delta_colored # Frame delta colored frame attribute

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
def write_memory(thresh_binary, frame_delta_colored, starting_time, ending_time):
	MEM_FILE_PATH = "vision/memory/" +  str(datetime.date.today()) + ".mem" # Path for mem file
	TSTP_FILE_PATH = "vision/memory/" +  str(datetime.date.today()) + ".tstp" # Path for tstp file

	memory = Memory(starting_time.strftime("%Y-%m-%d %H:%M:%S:%f"), ending_time.strftime("%Y-%m-%d %H:%M:%S:%f"), thresh_binary, frame_delta_colored) # Create an object from Memory class
	mode = 'a' if os.path.exists(MEM_FILE_PATH) else 'w' # If memory file exist file open mode is append(a) else write(w)
	with open(MEM_FILE_PATH, mode) as mem_file: # Open file
		mem_file.write(str(makeit_dict(memory)) + '\n') # Write memory in only one line

	timestamp = Timestamp(starting_time.strftime("%Y-%m-%d %H:%M:%S:%f"), ending_time.strftime("%Y-%m-%d %H:%M:%S:%f")) # Create an object from Timestamp class
	mode = 'a' if os.path.exists(TSTP_FILE_PATH) else 'w' # If timestamp file exist file open mode is append(a) else write(w)
	with open(TSTP_FILE_PATH, mode) as tstp_file: # Open file
		tstp_file.write(str(makeit_dict(timestamp)) + '\n') # Write timestamp in only one line

# Read a memory function
def read_memory(date_day,nth_record):
	MEM_FILE_PATH = "vision/memory/" +  date_day + ".mem" # Path for mem file

	if os.path.exists(MEM_FILE_PATH): # If memory file exist
		with open(MEM_FILE_PATH, 'r') as mem_file: # Open file
			memory = eval(mem_file.readlines()[nth_record]) # Evaluate the line, which will return dictionary
			return memory # Return memory to call
	else: # If memory file doesn't exist
		raise ValueError('MEM file doesn\'t exist!') # Raise a ValueError

# Read a timestamp function
def read_timestamp(date_day,nth_record):
	TSTP_FILE_PATH = "vision/memory/" +  date_day + ".mem" # Path for tstp file

	if os.path.exists(TSTP_FILE_PATH): # If timestamp file exist
		with open(TSTP_FILE_PATH, 'r') as tstp_file: # Open file
			timestamp = eval(tstp_file.readlines()[nth_record]) # Evaluate the line, which will return a dictionary
			return timestamp # Return timestamp to call
	else: # If timestamp file doesn't exist
		raise ValueError('TSTP file doesn\'t exist!') # Raise a ValueError

# Example USAGE block. NOT FUNCTIONAL
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
