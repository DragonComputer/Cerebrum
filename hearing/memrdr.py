import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import json

def read_memory(date_day,nth_record):
	JSON_FILE_PATH = "hearing/memory/" +  date_day + ".json" # Path for json file

	if os.path.exists(JSON_FILE_PATH):
		with open(JSON_FILE_PATH, 'r') as json_file:
			line = json_file.readlines()[-1]
			print line
			d = json.loads(line)
	else:
		raise ValueError('JSON file doesn\'t exist!')

if __name__ == "__main__":
	read_memory(str(datetime.date.today()),5)
