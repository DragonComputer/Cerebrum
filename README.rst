Cerebrum
========

An implementation of "Crossmodal Supervised Learning Algorithm with Time
Series Memory Recording & Long Short-Term Memory Networks"

Parts of The Cerebrum:

::

		- Vision
				- Amodal Perception
				- Color Perception
				- Depth Perception (in Future) (needs Stereoscopic Vision)
				- Form Perception (in Future) (needs Stereoscopic Vision)
				- Relative Velocity Perception (in Future) (needs Stereoscopic Vision)
		- Hearing
				- Speech Perception
				- Rhythmic Perception
				- Harmonic Perception (in Future) (WARNING: High Complexity)
				- Acceleration Perception (in Future) (needs 2 units of Triple Axis Accelerometer)
		- Language
				- Speech Analysis
				- Speech Synthesis
		- Multisensorial (Not Yet Available)
				- Touching (Not Yet Available)
						- Mechanic Perception (in Future) (needs lots of Pressure Sensors)
						- Heat & Cooling Perception (in Future) (needs lots of Temperature Sensors)
				- Tasting (Not Yet Available)
						- Solid/Fluid State Chemical Perception (in Future) (WARNING: Sensor Technology Not Available)
				- Smelling (Not Yet Available)
						- Gas State Chemical Perception (in Future) (WARNING: Sensor Technology Not Available)

*Multisensorial Part (Touching, Tasting and Smelling) is not yet
available. Because of their absence there should be a False Reward &
Punishment Mechanism for Reinforcement Learning*

		Cerebrum's purpose is getting continuous data inputs from different
		types of sensors as events, depending on the predefined threshold
		values and creating a complex time based relations between those
		events in memory by Long Short-Term Memory Networks. Lastly creating
		outputs triggered by stimuli, using already trained Artificial
		Neural Networks.

Version
~~~~~~~

0.1.21

Dependencies
~~~~~~~~~~~~

Cerebrum uses a number of open source libraries to do the job:

-  `Python 2.7 <https://www.python.org/download/releases/2.7/>`__ -
	 a widely used general-purpose, high-level programming language.
-  `PyAudio <https://people.csail.mit.edu/hubert/pyaudio/r>`__ -
	 provides Python bindings for PortAudio, the cross platform audio API.
-  `OpenCV <http://opencv.org/r>`__ - (Open Source Computer Vision)
	 is a library of programming functions mainly aimed at real-time
	 computer vision.
-  `wave Module <https://docs.python.org/2/library/wave.html>`__ -
	 provides a convenient interface to the WAV sound format.
-  `datetime Module <https://docs.python.org/2/library/datetime.html>`__
	 supplies classes for manipulating dates and times in both simple
	 and complex ways.
-  `os.path Module <https://docs.python.org/2/library/os.path.html>`__ -
	 the path module suitable for the operating system Python is running
	 on, and therefore usable for local paths.
-  `sys Module <https://docs.python.org/2/library/sys.html>`__ -
	 provides access to some variables used or maintained by the
	 interpreter and to functions that interact strongly with the
	 interpreter. It is always available.
-  `audioop Module <https://docs.python.org/2/library/audioop.html>`__ -
	 operates on sound fragments consisting of signed integer samples 8,
	 16 or 32 bits wide, stored in Python strings.
-  `NumPy <http://www.numpy.org/>`__ -
	 the fundamental package for scientific computing with Python.
-  `multiprocessing Module <https://docs.python.org/2/library/multiprocessing.html>`__ -
	 a package that supports spawning processes using an API similar to
	 the threading module.
-  `imutils Module <https://pypi.python.org/pypi/imutils/0.2>`__ -
	 a series of convenience functions to make basic image processing
	 functions such as translation, rotation, resizing, skeletonization
	 etc.
-  `PyQtGraph <http://www.pyqtgraph.org/>`__ -
	 a pure-python graphics and GUI library built on PyQt4 / PySide and numpy
-  `PyQt4 <https://pypi.python.org/pypi/PyQt4>`__ -
	 a comprehensive set of Python bindings for Digia's Qt cross platform GUI toolkit.
-  `time Module <https://docs.python.org/2/library/time.html>`__ -
	 provides various time-related functions.
-  `argparse Module <https://docs.python.org/2.7/library/argparse.html>`__ -
	 makes it easy to write user-friendly command-line interfaces.
-  `os Module <https://docs.python.org/2/library/os.html>`__ -
	 provides a portable way of using operating system dependent functionality.
-  `subprocess Module <https://docs.python.org/2/library/subprocess.html>`__ -
	 allows you to spawn new processes, connect to their
	 input/output/error pipes, and obtain their return codes.
-  `random Module <https://docs.python.org/2/library/random.html>`__ -
	 pseudo-random number generators for various distributions.
-  `pysrt Module <https://pypi.python.org/pypi/pysrt>`__ -
	 SubRip (.srt) subtitle parser and writer
-  `itertools Module <https://docs.python.org/2/library/itertools.html>`__ -
	 implements a number of iterator building blocks inspired by
	 constructs from APL, Haskell, and SML. Each has been recast in a form
	 suitable for Python
