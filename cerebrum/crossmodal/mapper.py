import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import hearing.memops
import vision.memops
import itertools

def overlap(first_inter,second_inter):
	for f,s in ((first_inter,second_inter), (second_inter,first_inter)):
		#will check both ways
		for time in (f["starting_time"], f["ending_time"]):
			if s["starting_time"] < time < s["ending_time"]:
				return True
		return False


hearing_timestamps = hearing.memops.read_timestamps(str(datetime.date.today()))
vision_timestamps = vision.memops.read_timestamps(str(datetime.date.today()))

#print datetime.datetime.strptime(hearing_timestamps[0]['starting_time'], "%Y-%m-%d %H:%M:%S.%f")
#combos = {(i1,i2):overlap(int1,int2)
#			 for (i1,int1),(i2,int2)
#				in itertools.product(enumerate(hearing_timestamps),enumerate(vision_timestamps))}
#overlapped = set(com for com,was_overlapped in combos.items() if was_overlapped)
#overlapped = sorted(overlapped) #this gives a list
#print combos.items()
#print overlapped

for (i1,int1),(i2,int2) in itertools.product(enumerate(hearing_timestamps),enumerate(vision_timestamps)):
	if overlap(int1,int2):
		print(i1,i2)
		print hearing_timestamps[i1]
		print vision_timestamps[i2]
