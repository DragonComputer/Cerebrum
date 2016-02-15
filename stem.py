import argparse
import multiprocessing
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--audio", help="path to the audio file")
args = vars(ap.parse_args())

subprocess.Popen(["python", "hearing/perception.py", args["audio"]])
subprocess.Popen(["python", "vision/perception.py", "--video", args["video"]])
