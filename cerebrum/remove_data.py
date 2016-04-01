__author__ = 'Mehmet Mert Yildiran, mert.yildiran@bil.omu.edu.tr'

import datetime
import os.path
import os

HIPPOCAMPUS = os.path.expanduser("~/Hippocampus/")

if os.path.exists(HIPPOCAMPUS):
	os.remove(HIPPOCAMPUS)
	print HIPPOCAMPUS + " is removed"
