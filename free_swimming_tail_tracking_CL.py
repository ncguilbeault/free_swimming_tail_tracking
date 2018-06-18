import free_swimming_tail_tracking
import numpy as np

# Create the video path.
video_path = "C:\\Users\\User1\\Desktop\\Video1.avi"

# Set the colours to be used for drawing values of interest on the final tracked videos.
colours =    [  (0, 0, 255),     (0, 127, 255),  (0, 255, 255),  (0, 255, 127),  (0, 255, 0),
                (255, 255, 0),  (255, 0, 0),    (255, 0, 127),  (147, 20, 255), (139, 139, 0),
                (49, 191, 114)
            ]

# Set the number of tail points to calculate.
n_tail_points = 7

# Set the range of angles to use when defining the length of the arc between tail points.
range_tail_angles = 2.0 * np.pi / 3.0

# Set the distance between tail points.
radius_tail_points = 19

# Set the interpupillary distance.
radius_eyes = 20

# Set the distance between the eyes and the swim bladder.
radius_swim_bladder = 55

# Set the length of the line to use for drawing the annotating the heading angle and eye angles onto the video.
line_length = 20

# Set the eye threshold.
eye_threshold = 75

free_swimming_tail_tracking.track_video(video_path, colours, n_tail_points, range_tail_angles, radius_tail_points, radius_eyes, radius_swim_bladder, line_length, eye_threshold)
