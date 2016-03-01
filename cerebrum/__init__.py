import argparse # Makes it easy to write user-friendly command-line interfaces.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
import hearing.perception # Hearing Package
import vision.perception # Vision Package
import language.analysis # Language Package
import crossmodal.mapper # Crossmodal Package
import neuralnet.trainer # NeuralNet Package
import time
from distutils.dir_util import mkpath
import os.path

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

	HEARING_MEM_DIR_PATH = "~/cerebrumData/hearing/memory/"
	HEARING_TSTP_DIR_PATH = "~/cerebrumData/hearing/memory/"
	VISION_MEM_DIR_PATH = "~/cerebrumData/vision/memory/"
	VISION_TSTP_DIR_PATH = "~/cerebrumData/vision/memory/"
	LANGUAGE_MEM_DIR_PATH = "~/cerebrumData/language/memory/"
	LANGUAGE_TSTP_DIR_PATH = "~/cerebrumData/language/memory/"
	PR_DIR_PATH = "~/cerebrumData/crossmodal/mappings/"

	mkpath(os.path.expanduser(HEARING_MEM_DIR_PATH))
	mkpath(os.path.expanduser(HEARING_TSTP_DIR_PATH))
	mkpath(os.path.expanduser(VISION_MEM_DIR_PATH))
	mkpath(os.path.expanduser(VISION_TSTP_DIR_PATH))
	mkpath(os.path.expanduser(LANGUAGE_MEM_DIR_PATH))
	mkpath(os.path.expanduser(LANGUAGE_TSTP_DIR_PATH))
	mkpath(os.path.expanduser(PR_DIR_PATH))

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

	training = 0

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
		if active_perceptions == 0 and not training:
				neuralnet_trainer_process = multiprocessing.Process(target=neuralnet.trainer.start) # Define neuralnet trainer process
				neuralnet_trainer_process.start() # Start neuralnet trainer process
				training = 1
		if training and not neuralnet_trainer_process.is_alive():
			crossmodal_mapper_process.terminate()
			print "EXIT: Training is finished."
			break
