import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths

def read_memory(date_day,nth_record):
	MEM_FILE_PATH = "hearing/memory/" +  date_day + ".mem" # Path for mem file

	if os.path.exists(MEM_FILE_PATH):
		with open(MEM_FILE_PATH, 'r') as mem_file:
			memory = eval(mem_file.readlines()[-1])
			print memory['starting_time']
			print memory['ending_time']
	else:
		raise ValueError('JSON file doesn\'t exist!')

if __name__ == "__main__":
	read_memory(str(datetime.date.today()),5)
