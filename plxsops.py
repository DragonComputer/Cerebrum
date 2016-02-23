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
