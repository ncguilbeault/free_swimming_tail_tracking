# Import libraries.
import numpy as np
import cv2

def calculate_brightest_background(video_path, num_backgrounds = 1, save_background = False):

    '''
    Calculate the background of a video as the brightest pixel values throughout the entire video.
    ** Assumes that objects in the foreground are always darker than the background.

    Arguments:
        video_path (str) - Path to the video. Required.
        num_backgrounds (int) - Number of returned backgrounds. Optional. Useful for long videos when the background illumination fluctuates over time. Default = 1.
        save_background (bool) - Saves the background(s) seperately. Optional. Default = False. ** Location of images can be found in path to video.

    Returns:
        background_array (np.array(num_backgrounds, frame width, frame height)) - Array of calculated background images.
    '''

    # Check arguments.
    if not isinstance(video_path, str):
        print('Error: video_path must be formatted as a string.')
        return
    if not isinstance(num_backgrounds, int):
        print('Error: num_backgrounds must be formatted as an integer.')
        return
    if not isinstance(save_background, bool):
        print('Error: save_background must be formatted as a boolean.')
        return

    try:
        # Load the video.
        capture = cv2.VideoCapture(video_path)
        # Initialize background array.
        background_array = []
        # Retrieve total number of frames in video.
        video_total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        # Determine the indices for when to calculate new background.
        background_chunk_index = int(video_total_frames / num_backgrounds)

        # Iterate through each frame in the video.
        for frame_num in range(video_total_frames):
            print('Calculating background. Processing frame number: {0}/{1}.'.format(frame_num + 1, video_total_frames), end = '\r')
            # Load frame into memory.
            success, frame = capture.read()
            # Check if frame was loaded successfully.
            if success:
                # Convert frame to grayscale.
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # Copy frame into background if this is the first frame.
                if frame_num == 0:
                    background = frame.copy().astype(np.float32)
                # Create a mask where the background is compared to the frame in the loop and used to update the background where the frame is.
                mask = np.less(background, frame)
                # Update the background image where all of the pixels in the new frame are brighter than the background image.
                background[mask] = frame[mask]
                # Compare the current number of frames iterated through to the number of backgrounds requested and add the background to the background array.
                if frame_num > 0 and frame_num % background_chunk_index == 0:
                    background_array.append(background)
                elif len(background_array) < num_backgrounds:
                    if (frame_num + 1) == video_total_frames:
                        background_array.append(background)
        print('Calculating background. Processing frame number: {0}/{1}.'.format(frame_num + 1, video_total_frames))
        # Save the background into an external file if requested.
        if save_background:
            if num_backgrounds == 1:
                brightest_background_path = '{0}_brightest_background.tif'.format(video_path[:-4])
                cv2.imwrite(brightest_background_path, background_array[0].astype(np.uint8))
            else:
                for i in range(len(background_array)):
                    brightest_background_path = '{0}_brightest_background{1}.tif'.format(video_path[:-4], i + 1)
                    cv2.imwrite(brightest_background_path, background_array[i].astype(np.uint8))
    except:
        # Errors that may occur during the background calculation are handled.
        print('')
        if capture.isOpened():
            capture.release()
        return [None * num_backgrounds]
    # Unload video from memory.
    capture.release()
    # Return the calculated background(s) as the brightest set of pixels throughout the video. An array is returned to provide the number of backgrounds requested.
    return background_array

def calculate_next_coords(init_coords, radius, frame, angle = 0, n_angles = 20, range_angles = 2 * np.pi / 3, tail_calculation = True):
    '''
    Calculates the next coordinate.

    Arguments:
        init_angle (float) - Initial angle that will be used when drawing a line between the inital coordinates and the next coordinates. Required.
            ** Units in radians.
        init_coords (y, x) - Coordinates to use for initializing search of next coordinates. Required.
        radius (float) - Radius to use for calculating potential next coordinates. Required.
        frame (frame width, frame height) - Video frame to search for coordinates. Required. Expects a background subtracted frame where objects are brighter than the background.
        tail_calculation (bool) - Determines which method to use if multiple coordinates are returned. Optional. Default = True. Used
            ** When calculating the tail, compute the angle between each potential next coordinate and the initial coordinate, and take the next coordinates whose angle is closest to the initial search angle.
            ** When not calculating the tail, compute the length between each potential next coordinate and the initial coordinate and take the first set of coordinates whose length is the shortest.
        n_angles (int) - Number of angles used when searching for initial points. Optional. Default = 20.
        range_angles (float) - The entire range of angles with which to look for the next pixel. Optional. Default = 2 / 3 * pi.
            ** Units in radians.

    Returns:
        next_coords (y, x) - The next coordinates in the frame.
    '''
    # Calculate list of angles.
    angles = np.linspace(angle - range_angles / 2, angle + range_angles / 2, n_angles)
    # Calculate list of all potential next coordinates.
    next_coords = [[int(round(init_coords[0] + (radius * np.sin(angles[i])))), int(round(init_coords[1] + (radius * np.cos(angles[i]))))] for i in range(len(angles))]
    # Remove duplicate coordinates.
    next_coords = [next_coords[i] for i in range(len(next_coords)) if next_coords[i][0] != next_coords[i - 1][0] or next_coords[i][1] != next_coords[i - 1][1]]
    # Get the list of coordinates where the potential next coordinates are the brightest pixels in the frame.
    coords = np.transpose(np.where(frame == np.max([frame[i[0]][i[1]] for i in next_coords])))
    # Get only the coordinates that were in the original list.
    next_coords = [[coords[j] for i in range(len(next_coords)) if coords[j][0] == next_coords[i][0] and coords[j][1] == next_coords[i][1]] for j in range(len(coords))]
    # Convert the coordinates to lists.
    next_coords = [next_coords[i][0].tolist() for i in range(len(next_coords)) if len(next_coords[i]) > 0]
    # Checks if more than one set of coordinates was found. This can occur if there are multiple pixels with the same (maximum) value.
    if len(next_coords) > 1:
        # Method to use for finding the next point if it is searching along the tail. For tail calculation, if multiple points are returned, then take the point whose angle is most similar to the previous angle.
        if tail_calculation:
            # Calculate the minimum difference between the angle of the next coordinates and the initial coordinates and the previous angle that was given.
            min_value = np.min([abs(angle - np.arctan2(next_coords[i][0] - init_coords[0], next_coords[i][1] - init_coords[1])) for i in range(len(next_coords))])
            # Take the set of coordinates whose angle matches the minimum difference.
            next_coords = [next_coords[i] for i in range(len(next_coords)) if abs(angle - np.arctan2(next_coords[i][0] - init_coords[0], next_coords[i][1] - init_coords[1])) == min_value]
        else:
            # Calculate the minimum length between the next coordinates and the initial coordinates.
            min_value = np.min([np.hypot(next_coords[i][0] - init_coords[0], next_coords[i][1] - init_coords[1]) for i in range(len(next_coords))])
            # Take the set of coordinates whose length between the next coordinates and previous coordinates matches the minimum length.
            next_coords = [next_coords[i] for i in range(len(next_coords)) if np.hypot(next_coords[i][0] - init_coords[0], next_coords[i][1] - init_coords[1]) == min_value]
    # Return the first set of coordinates.
    return next_coords[0]

def track_video(video_path, colours, n_tail_points, range_tail_angles, radius_tail_points, radius_eyes, radius_swim_bladder, line_length, eye_threshold, background_path = None, save_background = True, starting_frame = 0, fps = None, n_frames = None, pixel_threshold = 100, frame_change_threshold = 10):

    # Create or load background image.
    if background_path is None:
        background = calculate_brightest_background(video_path, save_background = save_background)[0].astype(np.uint8)
    else:
        background = cv2.imread(background_path, cv2.IMREAD_GRAYSCALE).astype(np.uint8)

    # Open the video path.
    capture = cv2.VideoCapture(video_path)

    # Set the frame position to start.
    capture.set(cv2.CAP_PROP_POS_FRAMES, starting_frame)

    # Create a path for the video once it is tracked.
    save_video_path = "{0}_tracked_new.avi".format(video_path[:-4])

    # Get the fps.
    if fps is None:
        fps = capture.get(cv2.CAP_PROP_FPS)

    # Get the total number of frames.
    if n_frames is None:
        n_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create video writer.
    writer = cv2.VideoWriter(save_video_path, 0, fps, (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    # Initialize variables for data.
    eye_coord_array = []
    eye_angle_array = []
    tail_coord_array = []
    body_coord_array = []
    heading_angle_array = []
    prev_frame = None
    prev_eye_angle = None

    # Iterate through each frame.
    for n in range(n_frames):
        print("Tracking video. Processing frame number: {0} / {1}.".format(n + 1, n_frames), end = '\r')
        # Load a frame into memory.
        success, original_frame = capture.read()
        # Checks if the frame was loaded successfully.
        if success:
            # Initialize variables for each frame.
            first_eye_coords = [np.nan, np.nan]
            second_eye_coords = [np.nan, np.nan]
            first_eye_angle = np.nan
            second_eye_angle = np.nan
            body_coords = [np.nan, np.nan]
            heading_angle = np.nan
            swim_bladder_coords = [np.nan, np.nan]
            tail_point_coords = [[np.nan, np.nan] for m in range(n_tail_points)]
            tail_points = [[np.nan, np.nan] for m in range(n_tail_points + 1)]
            # Convert the original frame to grayscale.
            frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY).astype(np.uint8)
            # Convert the frame into the absolute difference between the frame and the background.
            frame = cv2.absdiff(frame, background)
            # Apply a median blur filter to the frame.
            frame = cv2.medianBlur(frame, 3)
            try:
                # Check to ensure that the maximum pixel value is greater than a certain value. Useful for determining whether or not the at least one of the eyes is present in the frame.
                if np.max(frame) > pixel_threshold:
                    # Check to see if it's not the first frame and check if the sum of the absolute difference between the current frame and the previous frame is greater than a certain threshold. This helps reduce frame to frame noise in the position of the pixels.
                    if prev_frame is not None and np.sum(np.abs(frame.astype(float) - prev_frame.astype(float)) > frame_change_threshold) == 0:
                        # If the difference between the current frame and the previous frame is less than a certain threshold, then use the values that were previously calculated.
                        first_eye_coords, second_eye_coords = eye_coord_array[len(eye_coord_array) - 1]
                        first_eye_angle, second_eye_angle = eye_angle_array[len(eye_angle_array) - 1]
                        body_coords = body_coord_array[len(body_coord_array) - 1]
                        heading_angle = heading_angle_array[len(heading_angle_array) - 1]
                        swim_bladder_coords = tail_coord_array[len(tail_coord_array) - 1][0]
                        tail_point_coords = tail_coord_array[len(tail_coord_array) - 1][1:]
                    else:
                        # Return the coordinate of the brightest pixel.
                        first_eye_coords = [np.where(frame == np.max(frame))[0][0], np.where(frame == np.max(frame))[1][0]]
                        # Calculate the next brightest pixel that lies on the circle drawn around the first eye coordinates and has a radius equal to the distance between the eyes.
                        second_eye_coords = calculate_next_coords(first_eye_coords, radius_eyes, frame, n_angles = 100, range_angles = 2 * np.pi, tail_calculation = False)
                        # Calculate the angle between the two eyes.
                        eye_angle = np.arctan2(second_eye_coords[0] - first_eye_coords[0], second_eye_coords[1] - first_eye_coords[1])
                        # Check if this is the first frame.
                        if prev_eye_angle is not None:
                            # Check if the difference between the current eye angle and previous eye angle is somwehere around pi, meaning the first and second eye coordiantes have reversed. Occasionally, the coordinates of the eyes will switch between one and the other. This method is useful for keeping the positions of the left and right eye the same between frames.
                            if eye_angle - prev_eye_angle > np.pi / 2 or eye_angle - prev_eye_angle < -np.pi / 2:
                                if eye_angle - prev_eye_angle < np.pi * 3 / 2 and eye_angle - prev_eye_angle > -np.pi * 3 / 2:
                                    # Switch the first and second eye coordinates.
                                    coords = first_eye_coords
                                    first_eye_coords = second_eye_coords
                                    second_eye_coords = coords
                                    # Calculate the new eye angle.
                                    eye_angle = np.arctan2(second_eye_coords[0] - first_eye_coords[0], second_eye_coords[1] - first_eye_coords[1])
                        # Apply a threshold to the frame.
                        thresh = cv2.threshold(frame, eye_threshold, 255, cv2.THRESH_BINARY)[1]
                        # Find the contours of the binary regions in the thresholded frame.
                        contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[1]
                        # Iterate through each contour in the list of contours.
                        for i in range(len(contours)):
                            # Check if the first eye coordinate are within the current contour.
                            if cv2.pointPolygonTest(contours[i], (first_eye_coords[1], first_eye_coords[0]), False) == 1:
                                # Set the first eye coordinates to the centroid of the binary region and calculate the first eye angle.
                                M = cv2.moments(contours[i])
                                first_eye_coords = [int(round(M['m01']/M['m00'])), int(round(M['m10']/M['m00']))]
                                first_eye_angle = cv2.fitEllipse(contours[i])[2] * np.pi / 180
                            # Check if the second eye coordinate are within the current contour.
                            if cv2.pointPolygonTest(contours[i], (second_eye_coords[1], second_eye_coords[0]), False) == 1:
                                # Set the second eye coordinates to the centroid of the binary region and calculate the first eye angle.
                                M = cv2.moments(contours[i])
                                second_eye_coords = [int(round(M['m01']/M['m00'])), int(round(M['m10']/M['m00']))]
                                second_eye_angle = cv2.fitEllipse(contours[i])[2] * np.pi / 180
                        # Find the midpoint of the line that connects both eyes.
                        heading_coords = [(first_eye_coords[0] + second_eye_coords[0]) / 2, (first_eye_coords[1] + second_eye_coords[1]) / 2]
                        # Find the swim bladder coordinates by finding the next brightest coordinates that lie on a circle around the heading coordinates with a radius equal to the distance between the eyes and the swim bladder.
                        swim_bladder_coords = calculate_next_coords(heading_coords, radius_swim_bladder, frame, n_angles = 100, range_angles = 2 * np.pi, tail_calculation = False)
                        # Find the body coordinates by finding the center of the triangle that connects the eyes and swim bladder.
                        body_coords = [int(round((swim_bladder_coords[0] + first_eye_coords[0] + second_eye_coords[0]) / 3)), int(round((swim_bladder_coords[1] + first_eye_coords[1] + second_eye_coords[1]) / 3))]
                        # Calculate the heading angle as the angle between the body coordinates and the heading coordinates.
                        heading_angle = np.arctan2(heading_coords[0] - body_coords[0], heading_coords[1] - body_coords[1])
                        # Create an array that acts as a contour for the body and contains the swim bladder coordinates and eye coordinates.
                        body_contour = np.array([np.array([swim_bladder_coords[1], swim_bladder_coords[0]]), np.array([first_eye_coords[1], first_eye_coords[0]]), np.array([second_eye_coords[1], second_eye_coords[0]])])
                        # Check to see if the point that is created by drawing a line from the first eye coordinates with a length equal to half of the distance between the eyes is within the body contour. Occasionally, the angle of the eye is flipped to face towards the body instead of away. This is to check whether or not the eye angle should be flipped.
                        if cv2.pointPolygonTest(body_contour, (first_eye_coords[1] + (radius_eyes / 2 * np.cos(first_eye_angle)), first_eye_coords[0] + (radius_eyes / 2 * np.sin(first_eye_angle))), False) == 1:
                            # Flip the first eye angle.
                            if first_eye_angle > 0:
                                first_eye_angle -= np.pi
                            else:
                                first_eye_angle += np.pi
                        # Check to see if the point that is created by drawing a line from the first eye coordinates with a length equal to half of the distance between the eyes is within the body contour. Occasionally, the angle of the eye is flipped to face towards the body instead of away. This is to check whether or not the eye angle should be flipped.
                        if cv2.pointPolygonTest(body_contour, (second_eye_coords[1] + (radius_eyes / 2 * np.cos(second_eye_angle)), second_eye_coords[0] + (radius_eyes / 2 * np.sin(second_eye_angle))), False) == 1:
                            # Flip the second eye angle.
                            if second_eye_angle > 0:
                                second_eye_angle -= np.pi
                            else:
                                second_eye_angle += np.pi
                        # Calculate the initial tail angle as the angle opposite to the heading angle.
                        if heading_angle > 0:
                            tail_angle = heading_angle - np.pi
                        else:
                            tail_angle = heading_angle + np.pi
                        # Iterate through the number of tail points.
                        for m in range(n_tail_points):
                            # Check if this is the first tail point.
                            if m == 0:
                                # Calculate the first tail point using the swim bladder as the first set of coordinates.
                                tail_point_coords[m] = calculate_next_coords(swim_bladder_coords, radius_tail_points, frame, angle = tail_angle)
                            else:
                                # Check if this is the second tail point.
                                if m == 1:
                                    # Calculate the next tail angle as the angle between the first tail point and the swim bladder.
                                    tail_angle = np.arctan2(tail_point_coords[m - 1][0] - swim_bladder_coords[0], tail_point_coords[m - 1][1] - swim_bladder_coords[1])
                                # Check if the number of tail points calculated is greater than 2.
                                else:
                                    # Calculate the next tail angle as the angle between the last two tail points.
                                    tail_angle = np.arctan2(tail_point_coords[m - 1][0] - tail_point_coords[m - 2][0], tail_point_coords[m - 1][1] - tail_point_coords[m - 2][1])
                                # Calculate the next set of tail coordinates.
                                tail_point_coords[m] = calculate_next_coords(tail_point_coords[m - 1], radius_tail_points, frame, angle = tail_angle)
                        # Set the previous frame to the current frame.
                        prev_frame = frame
                        # Set the previous eye angle to the current eye angle.
                        prev_eye_angle = eye_angle
                    # Draw a circle arround the first eye coordinates.
                    original_frame = cv2.circle(original_frame, (first_eye_coords[1], first_eye_coords[0]), 1, colours[-3], -1)
                    # Draw a line representing the first eye angle.
                    original_frame = cv2.line(original_frame, (first_eye_coords[1], first_eye_coords[0]), (int(round(first_eye_coords[1] + (line_length * np.cos(first_eye_angle)))), int(round(first_eye_coords[0] + (line_length * np.sin(first_eye_angle))))), colours[-3], 1)
                    # Draw a circle around the second eye coordinates.
                    original_frame = cv2.circle(original_frame, (second_eye_coords[1], second_eye_coords[0]), 1, colours[-2], - 1)
                    # Draw a line representing the second eye angle.
                    original_frame = cv2.line(original_frame, (second_eye_coords[1], second_eye_coords[0]), (int(round(second_eye_coords[1] + (line_length * np.cos(second_eye_angle)))), int(round(second_eye_coords[0] + (line_length * np.sin(second_eye_angle))))), colours[-2], 1)
                    # Iterate through each set of tail points.
                    for m in range(n_tail_points):
                        # Check if this is the first tail point
                        if m == 0:
                            # For the first tail point, draw around the midpoint of the line that connects the swim bladder to the first tail point.
                            original_frame = cv2.circle(original_frame, (int(round((swim_bladder_coords[1] + tail_point_coords[m][1]) / 2)), int(round((swim_bladder_coords[0] + tail_point_coords[m][0]) / 2))), 1, colours[m], -1)
                        else:
                            # For all subsequent tail points, draw around the midpoint of the line that connects the previous tail point to the current tail point.
                            original_frame = cv2.circle(original_frame, (int(round((tail_point_coords[m - 1][1] + tail_point_coords[m][1]) / 2)), int(round((tail_point_coords[m - 1][0] + tail_point_coords[m][0]) / 2))), 1, colours[m], -1)
                    # Draw an arrow for the heading angle.
                    original_frame = cv2.arrowedLine(original_frame, (int(round(heading_coords[1] - (line_length / 2 * np.cos(heading_angle)))), int(round(heading_coords[0] - (line_length / 2 * np.sin(heading_angle))))), (int(round(heading_coords[1] + (line_length * np.cos(heading_angle)))), int(round(heading_coords[0] + (line_length * np.sin(heading_angle))))), colours[-1], 1, tipLength = 0.2)
            except:
                # Handles any errors that occur throughout tracking.
                first_eye_coords = [np.nan, np.nan]
                second_eye_coords = [np.nan, np.nan]
                first_eye_angle = np.nan
                second_eye_angle = np.nan
                body_coords = [np.nan, np.nan]
                heading_angle = np.nan
                swim_bladder_coords = [np.nan, np.nan]
                tail_point_coords = [[np.nan, np.nan] for m in range(n_tail_points)]
                tail_points = [[np.nan, np.nan] for m in range(n_tail_points + 1)]
            # Iterate through the number of tail points, including the swim bladder coordinates.
            for m in range(n_tail_points + 1):
                # Check if this is the first tail point.
                if m == 0:
                    # Add the swim bladder to a list that will contain all of the tail points, including the swim bladder.
                    tail_points[m] = swim_bladder_coords
                else:
                    # Add all of the tail points to the list.
                    tail_points[m] = tail_point_coords[m - 1]
            # Add all of the important features that were tracked into lists.
            eye_coord_array.append([first_eye_coords, second_eye_coords])
            eye_angle_array.append([first_eye_angle, second_eye_angle])
            tail_coord_array.append(tail_points)
            body_coord_array.append(body_coords)
            heading_angle_array.append(heading_angle)
            # Write the new frame that contains the annotated frame with tracked points to a new video.
            writer.write(original_frame)

    # Unload the video and writer from memory.
    capture.release()
    writer.release()

    # Create a dictionary that contains all of the results.
    results = { 'eye_coord_array' : eye_coord_array,
                'eye_angle_array' : eye_angle_array,
                'tail_coord_array' : tail_coord_array,
                'body_coord_array' : body_coord_array,
                'heading_angle_array' : heading_angle_array,
                'video_n_frames' : n_frames,
                'video_fps' : fps }

    # Create a path that will contain all of the results from tracking.
    data_path = "{0}_results.npz".format(video_path[:-4])

    # Save the results to a npz file.
    np.savez(data_path, data = results)
