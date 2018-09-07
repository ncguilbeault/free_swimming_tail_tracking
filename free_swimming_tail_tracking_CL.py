'''Software Written by Nicholas Guilbeault 2018'''

import free_swimming_tail_tracking as tr
import numpy as np

# Create the video path.
video_path = "C:\\Users\\User1\\Desktop\\Video1.avi"

# Create the background path.
background_path = "C:\\Users\\User1\\Desktop\\Video1_background.tif"

# Set the colours to be used for drawing values of interest on the final tracked videos.
colours =    [  (0, 0, 255),     (0, 127, 255),  (0, 255, 255),  (0, 255, 127),  (0, 255, 0),
                (255, 255, 0),  (255, 0, 0),    (255, 0, 127),  (147, 20, 255), (139, 139, 0),
                (49, 191, 114)
            ]
# If tracking parameters were saved using GUI, load tracking parameters.
tracking_parameters = np.load('tracking_parameters.npy').item()
n_tail_points = tracking_parameters['n_tail_points']
dist_tail_points = tracking_parameters['dist_tail_points']
dist_eyes = tracking_parameters['dist_eyes']
dist_swim_bladder = tracking_parameters['dist_swim_bladder']
frame_batch_size = tracking_parameters['frame_batch_size']
starting_frame = tracking_parameters['starting_frame']
n_frames = tracking_parameters['n_frames']
line_length = tracking_parameters['line_length']
pixel_threshold = tracking_parameters['pixel_threshold']
frame_change_threshold = tracking_parameters['frame_change_threshold']

# Set the number of tail points to calculate.
n_tail_points = 7
# Set the distance between tail points.
dist_tail_points = 5
# Set the interpupillary distance.
dist_eyes = 4
# Set the distance between the eyes and the swim bladder.
dist_swim_bladder = 12
# Set the threshold at which to determine whether or not to process the frame (there must be a pixel in the frame that is greater than the threshold in order for the algorithm to process the frame).
pixel_threshold = 40
# Set the line length that will be used for drawing the heading angle and eye angles.
line_length = 4

# Preview the results of the tracking parameters.
tr.preview_tracking_results(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold, line_length = line_length)

# Track the video. This function will perform tail tracking, annotate the results onto video, and save the results to a .npz file.
tr.track_video(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold, line_length = line_length)

# Track the video using multiprocessing and return the results.
results = tr.track_tail_in_video_with_multiprocessing(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold, line_length = line_length)

# Track the video without using multiprocessing.
results = tr.track_tail_in_video_without_multiprocessing(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold, line_length = line_length)
