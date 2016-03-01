import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

# Pair class
class Pair(object):
	def __init__(self, timestamp1, timestamp2, direction): # Initialize the object
		self.timestamp1 = timestamp1 # Memory starting time of a sense
		self.timestamp2 = timestamp2 # Memory starting time of another sense
		self.direction = direction # Direction. For example hearing to vision, vision to hearing, hearing to hearing etc.

# Convert object to dictionary
def makeit_dict(obj):
	if isinstance(obj, set):
		return list(obj)
	return obj.__dict__

# Write a pair function
def write_pair(timestamp1, timestamp2, direction):
	PR_FILE_PATH = os.path.expanduser("~/cerebrumData/crossmodal/mappings/" +  str(datetime.date.today()) + ".pr") # Path for pairs file

	pair = Pair(timestamp1, timestamp2, direction) # Create an object from Pair class
	mode = 'a' if os.path.exists(PR_FILE_PATH) else 'w' # If pairs file exist, file open mode will be append(a) else write(w)
	with open(PR_FILE_PATH, mode) as pr_file: # Open file
		pr_file.write(str(makeit_dict(pair)) + '\n') # Write pair with only one line

# Read a pair function
def read_pair(date_day,nth_record):
	PR_FILE_PATH = os.path.expanduser("~/cerebrumData/crossmodal/mappings/" +  date_day + ".pr") # Path for pairs file

	if os.path.exists(PR_FILE_PATH): # If pairs file exist
		with open(PR_FILE_PATH, 'r') as pr_file: # Open file
			pair = eval(pr_file.readlines()[nth_record]) # Evaluate the line, which will return a dictionary
			return pair # Return pair to call
	else: # If pairs file doesn't exist
		#raise ValueError('PR file doesn\'t exist!') # Raise a ValueError
		return False

# Get pairs function
def get_pairs(date_day,from_line=0):
	PR_FILE_PATH = os.path.expanduser("~/cerebrumData/crossmodal/mappings/" +  date_day + ".pr") # Path for pairs file
	pairs = []
	if os.path.exists(PR_FILE_PATH): # If pairs file exist
		with open(PR_FILE_PATH, 'r') as pr_file: # Open file
			for line in pr_file.readlines()[from_line:]: # Get whole lines starting from that line, default zero
				pair = eval(line) # Evaluate the line, which will return a dictionary
				pairs.append(pair) # Append pair to list in order
			return pairs # Return pair list to call
	else: # If pairs file doesn't exist
		#raise ValueError('PR file doesn\'t exist!') # Raise a ValueError
		return False
