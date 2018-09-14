'''Software Written by Nicholas Guilbeault 2018'''

import numpy as np
import matplotlib.pyplot as plt

data_file = "C:\\Users\\Thiele Lab\\Documents\\Sequences\\Camera 1\\17-07-11.550_results.npy"
data = np.load(data_file).item()
# print(data.keys())

# colors = [(0, 0, 255), (0, 127, 255), (0, 255, 255), (0, 255, 127), (0, 255, 0), (255, 255, 0), (255, 0, 0), (255, 0, 127), (147, 20, 255), (139, 139, 0), (49, 191, 114)]
# colors = [[colors[i][2]/255, colors[i][1]/255, colors[i][0]/255] for i in range(len(colors))]

smoothing_factor = 5

heading_angle_array = data['heading_angle_array']
tail_coord_array = data['tail_coord_array']
body_coord_array = data['body_coord_array']
eye_angle_array = data['eye_angle_array']
video_n_frames = data['video_n_frames']
video_fps = data['video_fps']
colours = data['colours']
colors = [[colours[i][2]/255, colours[i][1]/255, colours[i][0]/255] for i in range(len(colours))]
dist_tail_points = data['dist_tail_points']
dist_eyes = data['dist_eyes']
dist_swim_bladder = data['dist_swim_bladder']
eyes_threshold = data['eyes_threshold']
pixel_threshold = data['pixel_threshold']
frame_change_threshold = data['frame_change_threshold']

# [print(i, len(tail_coord_array[i])) for i in range(len(tail_coord_array)) if len(tail_coord_array[i]) != 8]
# print(dist_tail_points,dist_eyes,dist_swim_bladder,eyes_threshold,pixel_threshold,frame_change_threshold)

# tail_angles = [[np.arctan2(tail_coord_array[j][i + 1][0] - tail_coord_array[j][i][0], tail_coord_array[j][i + 1][1] - tail_coord_array[j][i][1]) for i in range(len(tail_coord_array[0]) - 1) if tail_coord_array[j][i + 1][0]] for j in range(len(tail_coord_array))]
tail_angles = [[np.arctan2(tail_coord_array[j][i + 1][0] - tail_coord_array[j][i][0], tail_coord_array[j][i + 1][1] - tail_coord_array[j][i][1]) for i in range(len(tail_coord_array[0]) - 1)] for j in range(len(tail_coord_array))]
body_tail_angles = [np.arctan2(tail_coord_array[j][0][0] - body_coord_array[j][0], tail_coord_array[j][0][1] - body_coord_array[j][1]) for j in range(len(tail_coord_array))]
tail_angles = [[tail_angles[j][i] - body_tail_angles[j] for i in range(len(tail_angles[0]))] for j in range(len(tail_angles))]
tail_angles = [[tail_angles[i][j] for i in range(len(tail_angles))] for j in range(len(tail_angles[0]))]

for i in range(len(tail_angles)):
    for j in range(1, len(tail_angles[i])):
        if tail_angles[i][j] >= 0.9 * np.pi:
            tail_angles[i][j] -= np.pi * 2
        elif tail_angles[i][j] <= 0.9 * -np.pi:
            tail_angles[i][j] += np.pi * 2

sum_tail_angles = [np.sum([abs(tail_angles[i][j]) for i in range(len(tail_angles))]) for j in range(len(tail_angles[0]))]
tail_angle_frames = np.where([sum_tail_angles[i] == sum_tail_angles[i + 1] == sum_tail_angles[i + 2] for i in range(len(sum_tail_angles) - 2)])[0]
# tail_angle_frames = np.where([sum_tail_angles[i] == sum_tail_angles[i + 1] for i in range(len(sum_tail_angles) - 1)])[0]
# for i in range(1, len(tail_angle_frames)):
#     if tail_angle_frames[i] - tail_angle_frames[i - 1] == 2:
#         tail_angle_frames = np.append(tail_angle_frames, tail_angle_frames[i - 1] + 1)
#     elif tail_angle_frames[i] - tail_angle_frames[i - 1] == 3:
#         tail_angle_frames = np.append(tail_angle_frames, tail_angle_frames[i - 1] + 1)
#         tail_angle_frames = np.append(tail_angle_frames, tail_angle_frames[i - 1] + 2)
#
# for i in range(len(tail_angles)):
#     for j in tail_angle_frames:
#         tail_angles[i][j] = 0.0

smoothed_tail_angles = [np.convolve(tail_angles[i], np.ones(smoothing_factor)/smoothing_factor, mode = 'same') for i in range(len(tail_angles))]

j = 0
if np.isnan(heading_angle_array[0]):
    while np.isnan(heading_angle_array[0]):
        if not np.isnan(heading_angle_array[j]):
            heading_angle_array[0] = heading_angle_array[j]
        j += 1

heading_angles = np.array([heading_angle_array[i] - heading_angle_array[0] for i in range(len(heading_angle_array))])

i = 0
for j in range(len(heading_angles)):
    if j not in tail_angle_frames:
        i = j
    else:
        heading_angles[j] = heading_angles[i]

for i in range(1, len(heading_angles)):
    if heading_angles[i] - heading_angles[i - 1] > np.pi:
        heading_angles[i:] -= np.pi * 2
    elif heading_angles[i] - heading_angles[i - 1] < -np.pi:
        heading_angles[i:] += np.pi * 2

smoothed_heading_angles = np.convolve(heading_angles, np.ones(smoothing_factor)/smoothing_factor, mode = 'same')

eye_angles = [[eye_angle_array[i][j] - heading_angle_array[i] for i in range(len(eye_angle_array))] for j in range(len(eye_angle_array[0]))]

i = 0
for k in range(len(eye_angles)):
    for j in range(len(eye_angles[k])):
        if j not in tail_angle_frames:
            i = j
        else:
            eye_angles[k][j] = eye_angles[k][i]

for j in range(len(eye_angles)):
    for i in range(1, len(eye_angles[j])):
        if eye_angles[j][i] - eye_angles[j][i - 1] > np.pi * 0.9:
            eye_angles[j][i] -= np.pi * 2
        elif eye_angles[j][i] - eye_angles[j][i - 1] < -np.pi * 0.9:
            eye_angles[j][i] += np.pi * 2

for j in range(len(eye_angles)):
    for i in range(1, len(eye_angles[j])):
        if eye_angles[j][i] > np.pi:
            eye_angles[j][i] -= np.pi * 2
        elif eye_angles[j][i] < -np.pi:
            eye_angles[j][i] += np.pi * 2

smoothed_eye_angles = [np.convolve(eye_angles[i], np.ones(smoothing_factor)/smoothing_factor, mode = 'same') for i in range(len(eye_angles))]

timepoints = np.linspace(0, video_n_frames / video_fps, video_n_frames)

# [plt.plot(timepoints, tail_angles[i], color = colors[i], lw = 1) for i in range(len(tail_angles))]
[plt.plot(timepoints, smoothed_tail_angles[i], color = colors[i], lw = 1) for i in range(len(smoothed_tail_angles))]
# plt.plot(timepoints, heading_angles, color = colors[-1], lw = 1)
# plt.plot(timepoints, smoothed_heading_angles, color = colors[-1], lw = 1)
# [plt.plot(timepoints, eye_angles[i], color = colors[i - 3], lw = 1) for i in range(len(eye_angles))]
# [plt.plot(timepoints, smoothed_eye_angles[i], color = colors[i - 3], lw = 1) for i in range(len(smoothed_eye_angles))]
plt.xlabel('Time (s)')
plt.ylabel('Angle (radians)')
plt.title('Tail Kinematics Over Time')
# plt.title('Heading Angle Over Time')
# plt.title('Eye Angles Over Time')
plt.show()
# plt.savefig("D:\\Data\\Colour Conditioning\\2018-06-28\\virtual_paramecia_test-1_tail_kinematics_over_time.tif", dpi = 300, bbox_inches = "tight")
