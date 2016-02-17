import argparse # Makes it easy to write user-friendly command-line interfaces.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import hearing.perception # Hearing Package
import vision.perception # Vision Package

ap = argparse.ArgumentParser() # Define an Argument Parser
ap.add_argument("-v", "--video", help="path to the video file") # Add --video argument
ap.add_argument("-a", "--audio", help="path to the audio file") # Add --audio argument
args = vars(ap.parse_args()) # Parse the arguments

if args["audio"] is None:
	raise ValueError('Microphone input is not yet available. Please type: python stem.py --help')
if args["video"] is None:
	raise ValueError('Camera input is not yet available. Please type: python stem.py --help')

hearing_perception_process = multiprocessing.Process(target=hearing.perception.start, args=(args["audio"],)) # Define hearing perception process
hearing_perception_process.start() # Start hearing perception process

vision_perception_process = multiprocessing.Process(target=vision.perception.start, args=(args["video"],)) # Define vision perception process
vision_perception_process.start() # Start vision perception process
