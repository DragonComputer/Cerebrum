__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import rethinkdb as r # Rethinkdb Python driver

# Memory class
class Memory(object):
	def __init__(self, starting_time, ending_time, amodal, color): # Initialize the object
		self.starting_time = starting_time # Starting time attribute
		self.ending_time = ending_time # Ending time attribute
		self.amodal = amodal # Thresh binary frame attribute
		self.color = color # Frame delta colored frame attribute

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

class VisionMemoryUtil():

	# Add a memory function
	@staticmethod
	def add_memory(amodal, color, starting_time, ending_time):
		conn = r.connect("localhost", 28015)
		r.db('test').table("vision_memory").insert([
			{ "starting_time": starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "ending_time": ending_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "amodal": r.binary(''.join(amodal)),
			  "color": r.binary(''.join(color))
			}
		]).run(conn)
		r.db('test').table("vision_timestamps").insert([
			{ "starting_time": starting_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
			  "ending_time": ending_time.strftime("%Y-%m-%d %H:%M:%S.%f")
			}
		]).run(conn)
		conn.close()

	# Get a memory function
	@staticmethod
	def get_memory(starting_time):
		conn = r.connect("localhost", 28015)
		cursor = r.db('test').table("vision_memory").filter({'starting_time': starting_time}).run(conn)
		conn.close()
		return cursor

	# Get timestamps function
	@staticmethod
	def get_timestamps():
		conn = r.connect("localhost", 28015)
		cursor = r.db('test').table("vision_timestamps").run(conn)
		conn.close()
		return cursor
