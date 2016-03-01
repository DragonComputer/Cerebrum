import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys # Provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) # Append parent directory to system path for importing sibling modules in next lines
import crossmodal.cmops # BUILT-IN Crosmodal operations package
import hearing.memops # BUILT-IN Hearing Memory operations package
import vision.memops # BUILT-IN Vision Memory operations package
import time # Provides various time-related functions.


# MAIN CODE BLOCK
def start():
	pairs = crossmodal.cmops.get_pairs(str(datetime.date.today()), 0) # Get pairs starting from 0th line
	if not pairs:
		print "No pairs? BUG?"

	# Loop over the pairs coming from CROSSMODAL
	for pair in pairs:
		   time.sleep(0.5) # Wait 0.5 seconds to prevent aggressive loop
		   print pair
