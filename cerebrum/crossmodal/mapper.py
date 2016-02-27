import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import hearing.memops
import vision.memops
import itertools
import cmops
import time

def overlap(first_inter,second_inter):
	for f,s in ((first_inter,second_inter), (second_inter,first_inter)):
		#will check both ways
		for time in (f["starting_time"], f["ending_time"]):
			if s["starting_time"] < time < s["ending_time"]:
				return True
		return False

#hearing_from_line = 0
#vision_from_line = 0
while True:
	time.sleep(5)
	hearing_timestamps = hearing.memops.read_timestamps(str(datetime.date.today()), 0)
	vision_timestamps = vision.memops.read_timestamps(str(datetime.date.today()), 0)
	if cmops.read_pair(str(datetime.date.today()), -1):
		last_pair = cmops.read_pair(str(datetime.date.today()), -1)
	else:
		last_pair = {}
		last_pair['timestamp1'] = 0
		last_pair['timestamp2'] = 0

	#hearing_from_line = len(hearing_timestamps) + hearing_from_line
	#vision_from_line = len(vision_timestamps) + vision_from_line

	#print vision_from_line
	#print datetime.datetime.strptime(hearing_timestamps[0]['starting_time'], "%Y-%m-%d %H:%M:%S.%f")
	#combos = {(i1,i2):overlap(int1,int2)
	#			 for (i1,int1),(i2,int2)
	#				in itertools.product(enumerate(hearing_timestamps),enumerate(vision_timestamps))}
	#overlapped = set(com for com,was_overlapped in combos.items() if was_overlapped)
	#overlapped = sorted(overlapped) #this gives a list
	#print combos.items()
	#print overlapped

	for (i1,int1),(i2,int2) in itertools.product(enumerate(hearing_timestamps),enumerate(vision_timestamps)):
		if hearing_timestamps[i1]['starting_time'] < last_pair['timestamp1'] or hearing_timestamps[i1]['starting_time'] < last_pair['timestamp2']:
			continue
		if vision_timestamps[i2]['starting_time'] < last_pair['timestamp1'] or vision_timestamps[i2]['starting_time'] < last_pair['timestamp2']:
			continue
		if overlap(int1,int2):
			print(i1,i2)
			print hearing_timestamps[i1]
			print vision_timestamps[i2]
			cmops.write_pair(hearing_timestamps[i1]['starting_time'], vision_timestamps[i2]['starting_time'], "hearing to vision")
			cmops.write_pair(vision_timestamps[i2]['starting_time'], hearing_timestamps[i1]['starting_time'], "vision to hearing")
