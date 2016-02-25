import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

# Plexus class
class Plexus(object):
	def __init__(self, end1, end2, weight): # Initialize the object
		self.end1 = end1 # First end of the Plexus link
		self.end2 = end1 # Second end of the Plexus link
		self.weight = weight # Weight of the Plexus link

# Convert object to dictionary
def makeit_dict(obj):
	if isinstance(obj, set):
		return list(obj)
	return obj.__dict__

# Write a link function
def write_link(end1, end2, weight):
	PLXS_FILE_PATH = "plexus/" +  str(datetime.date.today()) + ".plxs" # Path for plxs file

	link = Plexus(end1, end2, weight) # Create an object from Plexus class
	mode = 'a' if os.path.exists(PLXS_FILE_PATH) else 'w' # If plexus file exist file open mode is append(a) else write(w)
	with open(PLXS_FILE_PATH, mode) as plxs_file: # Open file
		plxs_file.write(str(makeit_dict(link)) + '\n') # Write link in only one line

# Read a link function
def read_link(date_day,nth_record):
	PLXS_FILE_PATH = "hearing/memory/" +  date_day + ".plxs" # Path for plxs file

	if os.path.exists(PLXS_FILE_PATH): # If plexus file exist
		with open(PLXS_FILE_PATH, 'r') as plxs_file: # Open file
			link = eval(plxs_file.readlines()[nth_record]) # Evaluate the line, which will return dictionary
			return link # Return memory to call
	else: # If plexus file doesn't exist
		raise ValueError('PLXS file doesn\'t exist!') # Raise a ValueError
