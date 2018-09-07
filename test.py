import free_swimming_tail_tracking as tr
import numpy as np

video_path = "D:\\2018-09-06\\19-26-50.397.avi"

background_path = "D:\\2018-09-06\\19-26-50.397_background.tif"

colours =    [  (0, 0, 255),     (0, 127, 255),  (0, 255, 255),  (0, 255, 127),  (0, 255, 0),
                (255, 255, 0),  (255, 0, 0),    (255, 0, 127),  (147, 20, 255), (139, 139, 0),
                (49, 191, 114)
            ]

tracking_parameters = np.load('tracking_parameters.npy').item()
n_tail_points = tracking_parameters['n_tail_points']
dist_tail_points = tracking_parameters['dist_tail_points']
dist_eyes = tracking_parameters['dist_eyes']
dist_swim_bladder = tracking_parameters['dist_swim_bladder']
pixel_threshold = tracking_parameters['pixel_threshold']

tr.track_video(video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder, background_path = background_path, pixel_threshold = pixel_threshold, frame_change_threshold = 20)
