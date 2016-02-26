import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import hearing.memops
import vision.memops

def overlap(first_inter,second_inter):
	for f,s in ((first_inter,second_inter), (second_inter,first_inter)):
		#will check both ways
		for time in (f["starting_time"], f["ending_time"]):
			if s["starting_time"] < time < s["ending_time"]:
				return True
		return False


hearing_timestamps = hearing.memops.read_timestamps(str(datetime.date.today()))
vision_timestamps = vision.memops.read_timestamps(str(datetime.date.today()))

print "Hearing Timestamps:"
print hearing_timestamps[0]

#print datetime.datetime.strptime(hearing_timestamps[0]['starting_time'], "%Y-%m-%d %H:%M:%S.%f")

print "--------------------------"

print "Vision Timestamps:"
print vision_timestamps[0]

print overlap(hearing_timestamps[0], vision_timestamps[0])
print overlap(hearing_timestamps[1], vision_timestamps[1])
