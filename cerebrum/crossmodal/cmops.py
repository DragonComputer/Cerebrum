import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

# Plexus class
class HearingVision(object):
	def __init__(self, hearing, vision): # Initialize the object
		self.hearing = hearing # Hearing memory starting time
		self.vision = vision # Vision memory starting time

# Convert object to dictionary
def makeit_dict(obj):
	if isinstance(obj, set):
		return list(obj)
	return obj.__dict__

# Write a pair function
def write_pair(hearing, vision):
	PR_FILE_PATH = "cerebrum/cossmodal/mappings/" +  str(datetime.date.today()) + ".pr" # Path for pairs file

	pair = HearingVision(hearing, vision) # Create an object from HearingVision class
	mode = 'a' if os.path.exists(PR_FILE_PATH) else 'w' # If pairs file exist, file open mode will be append(a) else write(w)
	with open(PR_FILE_PATH, mode) as pr_file: # Open file
		pr_file.write(str(makeit_dict(pair)) + '\n') # Write pair with only one line

# Read a pair function
def read_link(date_day,nth_record):
	PR_FILE_PATH = "cerebrum/crossmodal/mappings/" +  date_day + ".pr" # Path for pairs file

	if os.path.exists(PR_FILE_PATH): # If pairs file exist
		with open(PR_FILE_PATH, 'r') as pr_file: # Open file
			pair = eval(pr_file.readlines()[nth_record]) # Evaluate the line, which will return a dictionary
			return link # Return pair to call
	else: # If pairs file doesn't exist
		raise ValueError('PR file doesn\'t exist!') # Raise a ValueError
