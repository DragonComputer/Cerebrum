__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import datetime
import os.path
import os

HEARING_MEM_FILE_PATH = os.path.expanduser("~/Hippocampus/hearing/memory/" +  str(datetime.date.today()) + ".mem") # Path for mem file
HEARING_TSTP_FILE_PATH = os.path.expanduser("~/Hippocampus/hearing/memory/" +  str(datetime.date.today()) + ".tstp") # Path for tstp file
VISION_MEM_FILE_PATH = os.path.expanduser("~/Hippocampus/vision/memory/" +  str(datetime.date.today()) + ".mem") # Path for mem file
VISION_TSTP_FILE_PATH = os.path.expanduser("~/Hippocampus/vision/memory/" +  str(datetime.date.today()) + ".tstp") # Path for tstp file
LANGUAGE_MEM_FILE_PATH = os.path.expanduser("~/Hippocampus/language/memory/" +  str(datetime.date.today()) + ".mem") # Path for mem file
LANGUAGE_TSTP_FILE_PATH = os.path.expanduser("~/Hippocampus/language/memory/" +  str(datetime.date.today()) + ".tstp") # Path for tstp file
PR_FILE_PATH = os.path.expanduser("~/Hippocampus/crossmodal/mappings/" +  str(datetime.date.today()) + ".pr") # Path for pairs file

if os.path.exists(HEARING_MEM_FILE_PATH):
	os.remove(HEARING_MEM_FILE_PATH)
	print HEARING_MEM_FILE_PATH + " is removed"
if os.path.exists(HEARING_TSTP_FILE_PATH):
	os.remove(HEARING_TSTP_FILE_PATH)
	print HEARING_TSTP_FILE_PATH + " is removed"
if os.path.exists(VISION_MEM_FILE_PATH):
	os.remove(VISION_MEM_FILE_PATH)
	print VISION_MEM_FILE_PATH + " is removed"
if os.path.exists(VISION_TSTP_FILE_PATH):
	os.remove(VISION_TSTP_FILE_PATH)
	print VISION_TSTP_FILE_PATH + " is removed"
if os.path.exists(LANGUAGE_MEM_FILE_PATH):
	os.remove(LANGUAGE_MEM_FILE_PATH)
	print LANGUAGE_MEM_FILE_PATH + " is removed"
if os.path.exists(LANGUAGE_TSTP_FILE_PATH):
	os.remove(LANGUAGE_TSTP_FILE_PATH)
	print LANGUAGE_TSTP_FILE_PATH + " is removed"
if os.path.exists(PR_FILE_PATH):
	os.remove(PR_FILE_PATH)
	print PR_FILE_PATH + " is removed"
