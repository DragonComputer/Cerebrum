__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import rethinkdb as r # Rethinkdb Python driver

# Pair class
class Pair(object):
	def __init__(self, timestamp1, timestamp2, direction): # Initialize the object
		self.timestamp1 = timestamp1 # Memory starting time of a sense
		self.timestamp2 = timestamp2 # Memory starting time of another sense
		self.direction = direction # Direction. For example H2V, V2H, H2H etc.

# Convert object to dictionary
def makeit_dict(obj):
	if isinstance(obj, set):
		return list(obj)
	return obj.__dict__

class MapperUtil():

	# Add a pair function
	@staticmethod
	def add_pair(timestamp1, timestamp2, direction):
		conn = r.connect("localhost", 28015)
		r.db('test').table("crossmodal_mappings").insert([
			{ "timestamp1": timestamp1,
			  "timestamp2": timestamp2,
			  "direction": direction
			}
		]).run(conn)
		conn.close()

	# Get a pair function
	@staticmethod
	def get_pair_by_direction(direction):
		conn = r.connect("localhost", 28015)
		cursor = r.db('test').table("crossmodal_mappings").filter({'direction': direction}).run(conn)
		r.db('test').table("crossmodal_mappings").filter({'direction': direction}).delete().run(conn)
		conn.close()
		return cursor

	# Get all pairs function
	@staticmethod
	def get_allpairs():
		conn = r.connect("localhost", 28015)
		cursor = r.db('test').table("crossmodal_mappings").run(conn)
		#r.db('test').table("crossmodal_mappings").delete().run(conn)
		conn.close()
		return cursor
