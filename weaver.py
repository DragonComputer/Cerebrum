import datetime # Supplies classes for manipulating dates and times in both simple and complex ways
import os.path # The path module suitable for the operating system Python is running on, and therefore usable for local paths
import hearing.memops
import vision.memops

hearing_memory = hearing.memops.read_memory(str(datetime.date.today()),-1)
vision_memory = vision.memops.read_memory(str(datetime.date.today()),-1)

print "Hearing Memory:"
print hearing_memory['starting_time']
print hearing_memory['ending_time']

print "Vision Memory:"
print vision_memory['starting_time']
print vision_memory['ending_time']
