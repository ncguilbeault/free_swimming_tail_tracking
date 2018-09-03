import free_swimming_tail_tracking as tr

# Create the video path.
video_path = "C:\\Users\\User1\\Desktop\\Video1.avi"

# Create the background path.
background_path = "C:\\Users\\User1\\Desktop\\Video1_background.tif"

# Set the colours to be used for drawing values of interest on the final tracked videos.
colours =    [  (0, 0, 255),     (0, 127, 255),  (0, 255, 255),  (0, 255, 127),  (0, 255, 0),
                (255, 255, 0),  (255, 0, 0),    (255, 0, 127),  (147, 20, 255), (139, 139, 0),
                (49, 191, 114)
            ]

# Set the number of tail points to calculate.
n_tail_points = 7
# Set the distance between tail points.
dist_tail_points = 5
# Set the interpupillary distance.
dist_eyes = 4
# Set the distance between the eyes and the swim bladder.
dist_swim_bladder = 12
# Set the threshold at which to determine whether or not to process the frame (there must be a pixel in the frame that is greater than the threshold in order for the algorithm to process the frame)
pixel_threshold = 80

# Preview the results of the tracking parameters.
tr.preview_tracking_results(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold)

# Track the video. This function will perform tail tracking, annotate the results onto video, and save the results to a .npz file.
tr.track_video(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold)

# Track the video using multiprocessing and return the results.
results = tr.track_tail_in_video_with_multiprocessing(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold)

# Track the video without using multiprocessing.
results = tr.track_tail_in_video_without_multiprocessing(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold)
