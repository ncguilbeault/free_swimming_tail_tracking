# free_swimming_tail_tracking
[Python](https://www.python.org/) library that can track eyes and tail of a single, free-swimming larval zebrafish.

## Dependencies
Requires pre-installed [Python 3.6.1](https://www.python.org/downloads/release/python-361/) or greater. 
Requires pre-installed [OpenCV](https://opencv.org/).
Requires pre-installed [NumPy](http://www.numpy.org/).

## Usage
The file titled free_swimming_tail_tracking can be imported and used like a python library.
The file titled free_swimming_tail_tracking_CL is an example of a script that runs the track_video function from free_swimming_tail_tracking by giving it the path to a video and a set of parameters.
The track_video function returns a copy of the video with the points of interest (i.e. heading angle, tail points, eye angles, etc.) overlaid ontop of the original video.
The track_video function also returns a npz file that contains the angles and coordinates.
