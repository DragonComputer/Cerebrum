import argparse # Makes it easy to write user-friendly command-line interfaces.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import hearing.perception # Hearing Package
import vision.perception # Vision Package

ap = argparse.ArgumentParser() # Define an Argument Parser
ap.add_argument("-v", "--video", help="path to the video file") # Add --video argument
ap.add_argument("-a", "--audio", help="path to the audio file") # Add --audio argument
args = vars(ap.parse_args()) # Parse the arguments

if args["audio"] is None:
	hearing_perception_process = multiprocessing.Process(target=hearing.perception.start_mic) # Define hearing perception process
	hearing_perception_process.start() # Start hearing perception process
else:
	hearing_perception_process = multiprocessing.Process(target=hearing.perception.start, args=(args["audio"],)) # Define hearing perception process
	hearing_perception_process.start() # Start hearing perception process


if args["video"] is None:
	vision_perception_process = multiprocessing.Process(target=vision.perception.start_cam) # Define vision perception process
	vision_perception_process.start() # Start vision perception process
else:
	vision_perception_process = multiprocessing.Process(target=vision.perception.start, args=(args["video"],)) # Define vision perception process
	vision_perception_process.start() # Start vision perception process
