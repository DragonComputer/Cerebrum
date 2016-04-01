__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import datetime
import os.path
import shutil

HIPPOCAMPUS = os.path.expanduser("~/Hippocampus/")

if os.path.exists(HIPPOCAMPUS):
	shutil.rmtree(HIPPOCAMPUS)
	print HIPPOCAMPUS + " is removed"
