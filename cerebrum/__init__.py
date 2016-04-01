__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import argparse # Makes it easy to write user-friendly command-line interfaces.
import multiprocessing # A package that supports spawning processes using an API similar to the threading module.
from cerebrum.hearing import HearingPerception # Hearing Package
from cerebrum.vision import VisionPerception # Vision Package
from cerebrum.language import LanguageAnalyzer # Language Package
from cerebrum.crossmodal import MapperStarters # Crossmodal Package
#from cerebrum.neuralnet import NeuralWeaver # NeuralNet Package
import time
from distutils.dir_util import mkpath
import os.path
import os
import subprocess
import rethinkdb as r # Rethinkdb Python driver

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

	#args = [os.path.expanduser("--directory ~/ComeOnRethink")]
	#os.execvp("rethinkdb", args)
	subprocess.Popen(['rethinkdb', '--directory', os.path.expanduser('~/Hippocampus')]) # RethinkDB directory to store data and metadata
	time.sleep(3)
	conn = r.connect("localhost", 28015)
	try:
		r.db('test').table_create('hearing_memory').run(conn)
	except:
		pass
	try:
		r.db('test').table_create('hearing_timestamps').run(conn)
	except:
		pass
	try:
		r.db('test').table_create('language_memory').run(conn)
	except:
		pass
	try:
		r.db('test').table_create('language_timestamps').run(conn)
	except:
		pass
	try:
		r.db('test').table_create('vision_memory').run(conn)
	except:
		pass
	try:
		r.db('test').table_create('vision_timestamps').run(conn)
	except:
		pass
	try:
		r.db('test').table_create('crossmodal_mappings').run(conn)
	except:
		pass
	conn.close()
	time.sleep(3)

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

	crossmodal_mapperHV_process = multiprocessing.Process(target=MapperStarters.startHV) # Define crossmodal mapper for hearing & vision process
	crossmodal_mapperHV_process.start() # Start crossmodal mapperHV process

	crossmodal_mapperHL_process = multiprocessing.Process(target=MapperStarters.startHL) # Define crossmodal mapper for hearing & language process
	crossmodal_mapperHL_process.start() # Start crossmodal mapperHL process

	crossmodal_mapperVL_process = multiprocessing.Process(target=MapperStarters.startVL) # Define crossmodal mapper for vision & language process
	crossmodal_mapperVL_process.start() # Start crossmodal mapperVL process

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
				#neuralnet_weaver_process = multiprocessing.Process(target=NeuralWeaver.start) # Define neuralnet weaver process
				#neuralnet_weaver_process.start() # Start neuralnet weaver process
				training = 1
		if training and not neuralnet_weaver_process.is_alive():
			crossmodal_mapper_process.terminate()
			print "EXIT: Training is finished."
			break
