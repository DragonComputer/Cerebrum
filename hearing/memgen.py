import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

def save_memory(memory):
	JSON_FILE_PATH = "hearing/memory/" +  str(datetime.date.today()) + ".json" # Path for json file
	mode = 'a' if os.path.exists(JSON_FILE_PATH) else 'w'
	with open(JSON_FILE_PATH, mode) as f:
		f.write(str(memory) + "\n")
