import argparse # Makes it easy to write user-friendly command-line interfaces.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import hearing.perception # Hearing Package
import vision.perception # Vision Package
import language.analysis # Language Package
import crossmodal.mapper # Crossmodal Package
import time

def initiate():
	ap = argparse.ArgumentParser() # Define an Argument Parser
	ap.add_argument("-v", "--video", help="path to the video file") # Add --video argument
	ap.add_argument("-a", "--audio", help="path to the audio file") # Add --audio argument
	ap.add_argument("-c", "--captions", help="path to the captios file") # Add --captions argument
	args = vars(ap.parse_args()) # Parse the arguments

	stem_manager = multiprocessing.Manager() # Shared memory space manager
	hearing_perception_stimulated = stem_manager.Value('i', 0) # Define hearing perception stimualted variable in shared memory to get if it's stimulated or not (Integer)
	vision_perception_stimulated = stem_manager.Value('i', 0) # Define vision perception stimualted variable in shared memory to get if it's stimulated or not (Integer)
	language_analysis_stimulated = stem_manager.Value('i', 0) # Define language analysis stimualted variable in shared memory to get if it's stimulated or not (Integer)

	active_perceptions = 0

	if args["audio"] is None:
		pass
	elif args["audio"] == "0":
		hearing_perception_process = multiprocessing.Process(target=hearing.perception.start_mic, args=(hearing_perception_stimulated,)) # Define hearing perception process
		hearing_perception_process.start() # Start hearing perception process
		active_perceptions += 1
	else:
		hearing_perception_process = multiprocessing.Process(target=hearing.perception.start, args=(args["audio"],hearing_perception_stimulated)) # Define hearing perception process
		hearing_perception_process.start() # Start hearing perception process
		active_perceptions += 1

	if args["video"] is None:
		pass
	elif args["video"] == "0":
		vision_perception_process = multiprocessing.Process(target=vision.perception.start_cam, args=(vision_perception_stimulated,)) # Define vision perception process
		vision_perception_process.start() # Start vision perception process
		active_perceptions += 1
	else:
		vision_perception_process = multiprocessing.Process(target=vision.perception.start, args=(args["video"],vision_perception_stimulated)) # Define vision perception process
		vision_perception_process.start() # Start vision perception process
		active_perceptions += 1

	if args["captions"] is None:
		pass
	else:
		language_analysis_process = multiprocessing.Process(target=language.analysis.start, args=(args["captions"],language_analysis_stimulated)) # Define language analysis process
		language_analysis_process.start() # Start language analysis process
		active_perceptions += 1

	crossmodal_mapper_process = multiprocessing.Process(target=crossmodal.mapper.start) # Define crossmodal mapper process
	crossmodal_mapper_process.start() # Start crossmodal mapper process

	while True:
		if args["audio"]:
			if not hearing_perception_process.is_alive():
				active_perceptions -= 1
				args["audio"] = None
				print "WARNING: Hearing Perception process is terminated."
		if args["video"]:
			if not vision_perception_process.is_alive():
				active_perceptions -= 1
				args["video"] = None
				print "WARNING: Vision Perception process is terminated."
		if args["captions"]:
			if not language_analysis_process.is_alive():
				active_perceptions -= 1
				args["captions"] = None
				print "WARNING: Language Analysis process is terminated."
		if active_perceptions == 0:
			print "LEARNING..."
			time.sleep(0.5)
