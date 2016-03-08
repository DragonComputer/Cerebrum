__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import argparse # Makes it easy to write user-friendly command-line interfaces.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
from cerebrum.hearing import HearingPerception # Hearing Package
from cerebrum.vision import VisionPerception # Vision Package
from cerebrum.language import LanguageAnalyzer # Language Package
from cerebrum.crossmodal import MapperMain # Crossmodal Package
from cerebrum.neuralnet import NeuralWeaver # NeuralNet Package
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

	HEARING_MEM_DIR_PATH = "~/Hippocampus/hearing/memory/"
	HEARING_TSTP_DIR_PATH = "~/Hippocampus/hearing/memory/"
	VISION_MEM_DIR_PATH = "~/Hippocampus/vision/memory/"
	VISION_TSTP_DIR_PATH = "~/Hippocampus/vision/memory/"
	LANGUAGE_MEM_DIR_PATH = "~/Hippocampus/language/memory/"
	LANGUAGE_TSTP_DIR_PATH = "~/Hippocampus/language/memory/"
	PR_DIR_PATH = "~/Hippocampus/crossmodal/mappings/"

	mkpath(os.path.expanduser(HEARING_MEM_DIR_PATH))
	mkpath(os.path.expanduser(HEARING_TSTP_DIR_PATH))
	mkpath(os.path.expanduser(VISION_MEM_DIR_PATH))
	mkpath(os.path.expanduser(VISION_TSTP_DIR_PATH))
	mkpath(os.path.expanduser(LANGUAGE_MEM_DIR_PATH))
	mkpath(os.path.expanduser(LANGUAGE_TSTP_DIR_PATH))
	mkpath(os.path.expanduser(PR_DIR_PATH))

	if args["audio"] is None:
		pass
	else:
		hearing_perception_process = multiprocessing.Process(target=HearingPerception.start, args=(args["audio"],hearing_perception_stimulated)) # Define hearing perception process
		hearing_perception_process.start() # Start hearing perception process
		active_perceptions += 1

	if args["video"] is None:
		pass
	else:
		vision_perception_process = multiprocessing.Process(target=VisionPerception.start, args=(args["video"],vision_perception_stimulated)) # Define vision perception process
		vision_perception_process.start() # Start vision perception process
		active_perceptions += 1

	if args["captions"] is None:
		pass
	else:
		language_analysis_process = multiprocessing.Process(target=LanguageAnalyzer.start, args=(args["captions"],language_analysis_stimulated)) # Define language analysis process
		language_analysis_process.start() # Start language analysis process
		active_perceptions += 1

	crossmodal_mapper_process = multiprocessing.Process(target=MapperMain.start) # Define crossmodal mapper process
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
				neuralnet_weaver_process = multiprocessing.Process(target=NeuralWeaver.start) # Define neuralnet weaver process
				neuralnet_weaver_process.start() # Start neuralnet weaver process
				training = 1
		if training and not neuralnet_weaver_process.is_alive():
			crossmodal_mapper_process.terminate()
			print "EXIT: Training is finished."
			break
