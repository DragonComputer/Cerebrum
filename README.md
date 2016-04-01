# Cerebrum

Crossmodal Supervised Learning Toolkit with Classification & Regression on Time Series Memory

![Parts of The Human Brain (Psychology)](https://raw.githubusercontent.com/mertyildiran/Cerebrum/master/docs/img/areas-of-memory.jpg)

Parts of The Cerebrum:

 - Cerebrum

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
	- Emotion (Not Yet Available)
		- Activation - Pleasant : Alerted, Excited, Elated, Happy
		- Pleasant - Deactivation : Contented, Serene, Relaxed, Calm
		- Deactivation - Unpleasant : Fatigued, Bored, Depressed, Sad
		- Unpleasant - Activation : Upset, Stressed, Nervous, Tense
 - Crossmodal: Defines time based relations between the types of perceptions
 - NeuralNet: Multiple Neural Network interconnects the parts of The Cerebrum
	 - Current Speech Sequence to Current Visual Sequence
	 - Current Speech Sequence to Next Speech Sequence
	 - Current Visual Sequence to Current Speech Sequence
	 - Current Vİsual Sequence to Next Visual Sequence
	 - Current Speech Sequence to Text Sequence

*For Multisensorial Part technological advancements are insufficient, currently. Because of this deficiency, there should be a False Reward & Punishment Mechanism for Reinforcement Learning*

![Mapping Morphometry and Connectedness of the Human Brain](https://raw.githubusercontent.com/mertyildiran/Cerebrum/master/docs/img/connectedness-of-brain.png)


> Cerebrum's purpose is getting continuous data inputs from different types of perceptions in real time as
> memory sequences that triggered according to predefined threshold values and creating complex time
> based relations between those memories by Crossmodal logic and training multiple Artificial
> Neural Networks with this extracted data. Lastly creating outputs triggered by a stimuli, using
> pre-trained Artificial Neural Networks. - *Mehmet Mert Yıldıran*

### Hebbian Theory

![Experience-dependent spine formation and elimination.](https://raw.githubusercontent.com/mertyildiran/Cerebrum/master/docs/img/hebbian.jpg)

### Classification

![Image Captioning.](https://raw.githubusercontent.com/mertyildiran/Cerebrum/master/docs/img/classification.jpg)

### Regression

![Activation Functions.](https://raw.githubusercontent.com/mertyildiran/Cerebrum/master/docs/img/regression.png)

### Version
0.1.66

### Installation

Install RethinkDB:

```Shell
source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
wget -qO- https://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install rethinkdb
```

Watch data flow (optional) - <http://localhost:8080>

Install Cerebrum:

```Shell
sudo apt-get install python-pyaudio python-opencv python-scipy python-qt4
sudo pip install cerebrum
```

### Usage

Train with files:

```Shell
cerebrum --video PATH_TO_VIDEO_FILE --audio PATH_TO_AUDIO_FILE --captions PATH_TO_CAPTIONS_FILE
```

Example:

```Shell
cerebrum --video trainingData/Can\ You\ Make\ Someone\ Fall\ In\ Love\ With\ You-7_w_EA4u6oQ.mp4 --audio trainingData/Can\ You\ Make\ Someone\ Fall\ In\ Love\ With\ You-7_w_EA4u6oQ.wav --captions trainingData/Can\ You\ Make\ Someone\ Fall\ In\ Love\ With\ You-7_w_EA4u6oQ.en.vtt
```

Train with your cam (Not recommended):

```Shell
cerebrum --video 0 --audio 0
```

### Dependencies

Cerebrum uses a number of open source libraries to do the job:

* [Python 2.7] - a widely used general-purpose, high-level programming language.
* [PyAudio] - provides Python bindings for PortAudio, the cross platform audio API.
* [OpenCV] - (Open Source Computer Vision) is a library of programming functions mainly aimed at real-time computer vision.
* [wave Module] - provides a convenient interface to the WAV sound format.
* [datetime Module] - supplies classes for manipulating dates and times in both simple and complex ways.
* [os.path Module] - the path module suitable for the operating system Python is running on, and therefore usable for local paths.
* [sys Module] - provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.
* [audioop Module] - operates on sound fragments consisting of signed integer samples 8, 16 or 32 bits wide, stored in Python strings.
* [NumPy] - the fundamental package for scientific computing with Python.
* [multiprocessing Module] - a package that supports spawning processes using an API similar to the threading module.
* [imutils Module] - a series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization etc.
* [PyQtGraph] - a pure-python graphics and GUI library built on PyQt4 / PySide and numpy
* [PyQt4] - a comprehensive set of Python bindings for Digia's Qt cross platform GUI toolkit.
* [time Module] - provides various time-related functions.
* [argparse Module] - makes it easy to write user-friendly command-line interfaces.
* [os Module] - provides a portable way of using operating system dependent functionality.
* [subprocess Module] - allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes.
* [random Module] - pseudo-random number generators for various distributions.
* [pysrt Module] - SubRip (.srt) subtitle parser and writer
* [itertools Module] - implements a number of iterator building blocks inspired by constructs from APL, Haskell, and SML. Each has been recast in a form suitable for Python

[Python 2.7]: <https://www.python.org/download/releases/2.7/>
[PyAudio]: <https://people.csail.mit.edu/hubert/pyaudio/r>
[OpenCV]: <http://opencv.org/r>
[wave Module]: <https://docs.python.org/2/library/wave.html>
[datetime Module]: <https://docs.python.org/2/library/datetime.html>
[os.path Module]: <https://docs.python.org/2/library/os.path.html>
[sys Module]: <https://docs.python.org/2/library/sys.html>
[audioop Module]: <https://docs.python.org/2/library/audioop.html>
[NumPy]: <http://www.numpy.org/>
[multiprocessing Module]: <https://docs.python.org/2/library/multiprocessing.html>
[imutils Module]: <https://pypi.python.org/pypi/imutils/0.2>
[PyQtGraph]: <http://www.pyqtgraph.org/>
[PyQt4]: <https://pypi.python.org/pypi/PyQt4>
[time Module]: <https://docs.python.org/2/library/time.html>
[argparse Module]: <https://docs.python.org/2.7/library/argparse.html>
[os Module]: <https://docs.python.org/2/library/os.html>
[subprocess Module]: <https://docs.python.org/2/library/subprocess.html>
[random Module]: <https://docs.python.org/2/library/random.html>
[pysrt Module]: <https://pypi.python.org/pypi/pysrt>
[itertools Module]: <https://docs.python.org/2/library/itertools.html>

### License

The MIT License (MIT)

Copyright (c) 2016 Mehmet Mert Yıldıran mert.yildiran@bil.omu.edu.tr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
