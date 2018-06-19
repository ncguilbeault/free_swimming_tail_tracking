import free_swimming_tail_tracking
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

# Set the number of tail points to calculate.
n_tail_points = 7
# Set the distance between tail points.
dist_tail_points = 5
# Set the interpupillary distance.
dist_eyes = 4
# Set the distance between the eyes and the swim bladder.
dist_swim_bladder = 12

pixel_threshold = 80

free_swimming_tail_tracking.track_video(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, pixel_threshold = 80, background_path = background_path, extended_eyes_calculation = False)
