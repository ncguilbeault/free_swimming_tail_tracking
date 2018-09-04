# import python modules
import sys
import os
import subprocess
import cv2
import numpy as np
import free_swimming_tail_tracking as tr

from PyQt5.QtWidgets import QColorDialog, QApplication, QSlider, QWidget, QDesktopWidget, QTextEdit, QAction, QFileDialog, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, QCheckBox, QLabel, QStatusBar, QMenuBar, QSizePolicy, QHBoxLayout, QFrame, QScrollArea
from PyQt5.QtGui import QPixmap, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QEvent

class MainWindow(QMainWindow):

    # Defining Initialization Functions
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
    def initUI(self):
        self.initialize_class_variables()
        self.get_main_window_attributes()
        self.add_menubar()
        self.add_options_to_menubar()
        self.add_statusbar()
        self.add_preview_frame_window()
        self.add_descriptors_window()
        self.add_descriptors_to_window()
        self.add_frame_window_slider()
        self.add_preview_frame_number_textbox()
        self.add_update_preview_button()
        self.add_preview_parameters_window()
        self.add_preview_parameters_to_window()
        self.add_tracking_parameters_window()
        self.add_tracking_parameters_to_window()
        self.setMenuBar(self.menubar)
        self.setStatusBar(self.statusbar)
        self.setWindowTitle('Free Swimming Tail Tracking')
        self.setWindowState(Qt.WindowMaximized)
        self.show()
    def initialize_class_variables(self):
        self.video_path = None
        self.video_path_basename = None
        self.video_path_folder = None
        self.video_n_frames = 0
        self.video_fps = 0
        self.video_format = None
        self.video_frame_width = 0
        self.video_frame_height = 0
        self.main_window_width = 0
        self.main_window_height = 0
        self.frame_number = 0
        self.status_bar_message = ''
        self.background_path = None
        self.background_path_basename = None
        self.background_path_folder = None
        self.save_path = None
        self.preview_background = False
        self.preview_background_subtracted_frame = False
        self.n_tail_points = 0
        self.dist_tail_points = 0
        self.dist_eyes = 0
        self.dist_swim_bladder = 0
        self.frame_batch_size = 50
        self.starting_frame = 0
        self.n_frames = None
        self.line_length = 0
        self.pixel_threshold = 100
        self.frame_change_threshold = 10

    # Defining Get Functions
    def get_main_window_attributes(self):
        self.main_window_width = QDesktopWidget().availableGeometry().width()
        self.main_window_height = QDesktopWidget().availableGeometry().height()
    def get_video_attributes(self):
        self.video_path_folder = os.path.dirname(self.video_path)
        self.video_path_basename = os.path.basename(self.video_path)
        self.video_n_frames = tr.get_total_frame_number_from_video(self.video_path)
        self.video_fps = tr.get_fps_from_video(self.video_path)
        self.video_format = tr.get_video_format_from_video(self.video_path)
        self.video_frame_width, self.video_frame_height = tr.get_frame_size_from_video(self.video_path)
    def get_background_attributes(self):
        self.background_path_folder = os.path.dirname(self.background_path)
        self.background_path_basename = os.path.basename(self.background_path)
        self.background_height, self.background_width = self.background.shape

    # Defining Add Functions
    def add_menubar(self):
        self.menubar = QMenuBar()
        self.menubar.resize(self.main_window_width, self.menubar.height())
    def add_statusbar(self):
        self.statusbar = QStatusBar()
        self.statusbar_message = 'Welcome to the free swimming tail tracking GUI. Begin by openning a video.'
        self.statusbar.showMessage(self.statusbar_message)
        self.statusbar.messageChanged.connect(self.update_statusbar_message)
    def add_options_to_menubar(self):
        self.options_menu = self.menubar.addMenu('&Options')

        self.open_video_action = QAction('&Open Video', self)
        self.open_video_action.setShortcut('Ctrl+O')
        self.open_video_action.setStatusTip('Open Video')
        self.open_video_action.triggered.connect(self.trigger_open_video)
        self.options_menu.addAction(self.open_video_action)

        self.select_save_path_action = QAction('&Select Save Path', self)
        self.select_save_path_action.setShortcut('Ctrl+P')
        self.select_save_path_action.setStatusTip('Select Save Path')
        self.select_save_path_action.triggered.connect(self.trigger_select_save_path)
        self.options_menu.addAction(self.select_save_path_action)

        self.load_background_action = QAction('&Load Background', self)
        self.load_background_action.setShortcut('Ctrl+L')
        self.load_background_action.setStatusTip('Load Background')
        self.load_background_action.triggered.connect(self.trigger_load_background)
        self.options_menu.addAction(self.load_background_action)

        self.calculate_background_action = QAction('&Calculate Background', self)
        self.calculate_background_action.setShortcut('Ctrl+B')
        self.calculate_background_action.setStatusTip('Calculate Background')
        self.calculate_background_action.triggered.connect(self.trigger_calculate_background)
        self.options_menu.addAction(self.calculate_background_action)

        self.save_background_action = QAction('&Save Background', self)
        self.save_background_action.setShortcut('Ctrl+S')
        self.save_background_action.setStatusTip('Save Background')
        self.save_background_action.triggered.connect(self.trigger_save_background)
        self.options_menu.addAction(self.save_background_action)
    def add_preview_frame_window(self):
        font = QFont()
        font.setPointSize(18)
        self.preview_frame_window = QLabel(self)
        self.preview_frame_window.setFrameShape(QFrame.Panel)
        self.preview_frame_window.setFrameShadow(QFrame.Sunken)
        self.preview_frame_window.setLineWidth(5)
        self.preview_frame_window.move(5, 25)
        self.preview_frame_window.resize(1000, 1000)
        self.preview_frame_window.setText('Preview Frame Window')
        self.preview_frame_window.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.preview_frame_window.setFont(font)
    def add_descriptors_window(self):
        font = QFont()
        font.setPointSize(18)
        self.descriptors_window = QLabel(self)
        self.descriptors_window.setFrameShape(QFrame.Panel)
        self.descriptors_window.setFrameShadow(QFrame.Sunken)
        self.descriptors_window.setLineWidth(5)
        self.descriptors_window.move(1015, 25)
        self.descriptors_window.resize(500, 1000)
        self.descriptors_window.setText('Descriptors')
        self.descriptors_window.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.descriptors_window.setFont(font)
    def add_descriptors_to_window(self):
        font = QFont()
        font.setPointSize(10)
        self.video_path_folder_descriptor = QLabel(self)
        self.video_path_folder_descriptor.move(1025, 100)
        self.video_path_folder_descriptor.resize(490, 20)
        self.video_path_folder_descriptor.setText('Video Folder: {0}'.format(self.video_path_folder))
        self.video_path_folder_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_path_folder_descriptor.setFont(font)

        self.video_path_basename_descriptor = QLabel(self)
        self.video_path_basename_descriptor.move(1025, 140)
        self.video_path_basename_descriptor.resize(490, 20)
        self.video_path_basename_descriptor.setText('Video Filename: {0}'.format(self.video_path_basename))
        self.video_path_basename_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_path_basename_descriptor.setFont(font)

        self.video_n_frames_descriptor = QLabel(self)
        self.video_n_frames_descriptor.move(1025, 180)
        self.video_n_frames_descriptor.resize(490, 20)
        self.video_n_frames_descriptor.setText('Video Total Frames: {0}'.format(self.video_n_frames))
        self.video_n_frames_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_n_frames_descriptor.setFont(font)

        self.video_fps_descriptor = QLabel(self)
        self.video_fps_descriptor.move(1025, 220)
        self.video_fps_descriptor.resize(490, 20)
        self.video_fps_descriptor.setText('Video FPS: {0}'.format(self.video_fps))
        self.video_fps_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_fps_descriptor.setFont(font)

        self.video_format_descriptor = QLabel(self)
        self.video_format_descriptor.move(1025, 260)
        self.video_format_descriptor.resize(490, 20)
        self.video_format_descriptor.setText('Video Format: {0}'.format(self.video_format))
        self.video_format_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_format_descriptor.setFont(font)

        self.frame_width_descriptor = QLabel(self)
        self.frame_width_descriptor.move(1025, 300)
        self.frame_width_descriptor.resize(490, 20)
        self.frame_width_descriptor.setText('Frame Width: {0}'.format(self.video_frame_width))
        self.frame_width_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.frame_width_descriptor.setFont(font)

        self.frame_height_descriptor = QLabel(self)
        self.frame_height_descriptor.move(1025, 340)
        self.frame_height_descriptor.resize(490, 20)
        self.frame_height_descriptor.setText('Frame Height: {0}'.format(self.video_frame_height))
        self.frame_height_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.frame_height_descriptor.setFont(font)

        self.background_path_folder_descriptor = QLabel(self)
        self.background_path_folder_descriptor.move(1025, 380)
        self.background_path_folder_descriptor.resize(490, 20)
        self.background_path_folder_descriptor.setText('Background Folder: {0}'.format(self.background_path_folder))
        self.background_path_folder_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.background_path_folder_descriptor.setFont(font)

        self.background_path_basename_descriptor = QLabel(self)
        self.background_path_basename_descriptor.move(1025, 420)
        self.background_path_basename_descriptor.resize(490, 20)
        self.background_path_basename_descriptor.setText('Background Filename: {0}'.format(self.background_path_basename))
        self.background_path_basename_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.background_path_basename_descriptor.setFont(font)

        self.save_path_descriptor = QLabel(self)
        self.save_path_descriptor.move(1025, 460)
        self.save_path_descriptor.resize(490, 20)
        self.save_path_descriptor.setText('Save Path: {0}'.format(self.save_path))
        self.save_path_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.save_path_descriptor.setFont(font)
    def add_frame_window_slider(self):
        self.frame_window_slider = QSlider(Qt.Horizontal, self)
        self.frame_window_slider.setToolTip('Move slider to change preview frame number.')
        self.frame_window_slider.move(5, 1040)
        self.frame_window_slider.resize(1000, 10)
        self.frame_window_slider.setEnabled(False)
        self.frame_window_slider.setFocusPolicy(Qt.StrongFocus)
        self.frame_window_slider.setTickPosition(QSlider.TicksBelow)
        self.frame_window_slider.setTickInterval(0)
        self.frame_window_slider.setSingleStep(0)
        self.update_frame_window_slider(activate = False)
        self.frame_window_slider.sliderMoved.connect(self.trigger_moved_frame_window_slider)
    def add_preview_frame_number_textbox(self):
        font = QFont()
        font.setPointSize(10)
        self.preview_frame_number_textbox_label = QLabel(self)
        self.preview_frame_number_textbox_label.move(5, 1060)
        self.preview_frame_number_textbox_label.resize(145, 20)
        self.preview_frame_number_textbox_label.setText('Preview Frame Number: ')
        self.preview_frame_number_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.preview_frame_number_textbox_label.setFont(font)
        self.preview_frame_number_textbox = QLineEdit(self)
        self.preview_frame_number_textbox.move(150, 1060)
        self.preview_frame_number_textbox.resize(100, 20)
        self.preview_frame_number_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.preview_frame_number_textbox.setFont(font)
        self.update_preview_frame_number_textbox(inactivate = True)
        self.preview_frame_number_textbox.returnPressed.connect(self.update_preview_from_button)
    def add_update_preview_button(self):
        self.update_preview_button = QPushButton('Update Preview', self)
        self.update_preview_button.move(5, 1090)
        self.update_preview_button.resize(245, 50)
        self.update_preview_from_button(inactivate = True)
        self.update_preview_button.clicked.connect(self.update_preview_from_button)
    def add_preview_parameters_window(self):
        font = QFont()
        font.setPointSize(18)
        self.preview_parameters_window = QLabel(self)
        self.preview_parameters_window.setFrameShape(QFrame.Panel)
        self.preview_parameters_window.setFrameShadow(QFrame.Sunken)
        self.preview_parameters_window.setLineWidth(5)
        self.preview_parameters_window.move(1015, 1035)
        self.preview_parameters_window.resize(1540, 330)
        self.preview_parameters_window.setText('Preview Parameters')
        self.preview_parameters_window.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.preview_parameters_window.setFont(font)
    def add_preview_parameters_to_window(self):
        font = QFont()
        font.setPointSize(10)
        self.preview_background_checkbox = QCheckBox(self)
        self.preview_background_checkbox.move(1025, 1110)
        self.preview_background_checkbox.setEnabled(False)
        self.preview_background_checkbox.stateChanged.connect(self.trigger_preview_background_checkbox)
        self.preview_background_checkbox_label = QLabel(self)
        self.preview_background_checkbox_label.move(1045, 1113)
        self.preview_background_checkbox_label.resize(500, 20)
        self.preview_background_checkbox_label.setText('Preview background')
        self.preview_background_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_background_checkbox_label.setFont(font)

        self.preview_background_subtracted_frame_checkbox = QCheckBox(self)
        self.preview_background_subtracted_frame_checkbox.move(1025, 1150)
        self.preview_background_subtracted_frame_checkbox.stateChanged.connect(self.trigger_preview_background_subtracted_frame_checkbox)
        self.preview_background_subtracted_frame_checkbox.setEnabled(False)
        self.preview_background_subtracted_frame_checkbox_label = QLabel(self)
        self.preview_background_subtracted_frame_checkbox_label.move(1045, 1153)
        self.preview_background_subtracted_frame_checkbox_label.resize(500, 20)
        self.preview_background_subtracted_frame_checkbox_label.setText('Preview background subtracted frames')
        self.preview_background_subtracted_frame_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_background_subtracted_frame_checkbox_label.setFont(font)
    def add_tracking_parameters_window(self):
        font = QFont()
        font.setPointSize(18)
        self.tracking_parameters_window = QLabel(self)
        self.tracking_parameters_window.setFrameShape(QFrame.Panel)
        self.tracking_parameters_window.setFrameShadow(QFrame.Sunken)
        self.tracking_parameters_window.setLineWidth(5)
        self.tracking_parameters_window.move(1525, 25)
        self.tracking_parameters_window.resize(1030, 1000)
        self.tracking_parameters_window.setText('Tracking Parameters')
        self.tracking_parameters_window.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.tracking_parameters_window.setFont(font)
    def add_tracking_parameters_to_window(self):
        font = QFont()
        font.setPointSize(10)
        self.tracking_n_tail_points_textbox_label = QLabel(self)
        self.tracking_n_tail_points_textbox_label.move(1500, 100)
        self.tracking_n_tail_points_textbox_label.resize(500, 20)
        self.tracking_n_tail_points_textbox_label.setText('Number of Tail Points: ')
        self.tracking_n_tail_points_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_n_tail_points_textbox_label.setFont(font)
        self.tracking_n_tail_points_textbox = QLineEdit(self)
        self.tracking_n_tail_points_textbox.move(2000, 100)
        self.tracking_n_tail_points_textbox.resize(80, 20)
        self.tracking_n_tail_points_textbox.setText('{0}'.format(self.n_tail_points))
        self.tracking_n_tail_points_textbox.setEnabled(False)
        self.tracking_n_tail_points_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_n_tail_points_textbox.setFont(font)
        self.tracking_n_tail_points_textbox.textEdited.connect(self.check_tracking_n_tail_points_textbox)

        self.tracking_dist_tail_points_textbox_label = QLabel(self)
        self.tracking_dist_tail_points_textbox_label.move(1500, 140)
        self.tracking_dist_tail_points_textbox_label.resize(500, 20)
        self.tracking_dist_tail_points_textbox_label.setText('Distance Between Tail Points: ')
        self.tracking_dist_tail_points_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_dist_tail_points_textbox_label.setFont(font)
        self.tracking_dist_tail_points_textbox = QLineEdit(self)
        self.tracking_dist_tail_points_textbox.move(2000, 140)
        self.tracking_dist_tail_points_textbox.resize(80, 20)
        self.tracking_dist_tail_points_textbox.setText('{0}'.format(self.dist_tail_points))
        self.tracking_dist_tail_points_textbox.setEnabled(False)
        self.tracking_dist_tail_points_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_dist_tail_points_textbox.setFont(font)
        self.tracking_dist_tail_points_textbox.textEdited.connect(self.check_tracking_dist_tail_points_textbox)

        self.tracking_dist_eyes_textbox_label = QLabel(self)
        self.tracking_dist_eyes_textbox_label.move(1500, 180)
        self.tracking_dist_eyes_textbox_label.resize(500, 20)
        self.tracking_dist_eyes_textbox_label.setText('Distance Between Eyes: ')
        self.tracking_dist_eyes_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_dist_eyes_textbox_label.setFont(font)
        self.tracking_dist_eyes_textbox = QLineEdit(self)
        self.tracking_dist_eyes_textbox.move(2000, 180)
        self.tracking_dist_eyes_textbox.resize(80, 20)
        self.tracking_dist_eyes_textbox.setText('{0}'.format(self.dist_eyes))
        self.tracking_dist_eyes_textbox.setEnabled(False)
        self.tracking_dist_eyes_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_dist_eyes_textbox.setFont(font)
        self.tracking_dist_eyes_textbox.textEdited.connect(self.check_tracking_dist_eyes_textbox)

        self.tracking_dist_swim_bladder_textbox_label = QLabel(self)
        self.tracking_dist_swim_bladder_textbox_label.move(1500, 220)
        self.tracking_dist_swim_bladder_textbox_label.resize(500, 20)
        self.tracking_dist_swim_bladder_textbox_label.setText('Distance Between Eyes and Swim Bladder: ')
        self.tracking_dist_swim_bladder_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_dist_swim_bladder_textbox_label.setFont(font)
        self.tracking_dist_swim_bladder_textbox = QLineEdit(self)
        self.tracking_dist_swim_bladder_textbox.move(2000, 220)
        self.tracking_dist_swim_bladder_textbox.resize(80, 20)
        self.tracking_dist_swim_bladder_textbox.setText('{0}'.format(self.dist_swim_bladder))
        self.tracking_dist_swim_bladder_textbox.setEnabled(False)
        self.tracking_dist_swim_bladder_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_dist_swim_bladder_textbox.setFont(font)
        self.tracking_dist_swim_bladder_textbox.textEdited.connect(self.check_tracking_dist_swim_bladder_textbox)

        self.tracking_frame_batch_size_textbox_label = QLabel(self)
        self.tracking_frame_batch_size_textbox_label.move(1500, 260)
        self.tracking_frame_batch_size_textbox_label.resize(500, 20)
        self.tracking_frame_batch_size_textbox_label.setText('Frame Batch Size: ')
        self.tracking_frame_batch_size_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_frame_batch_size_textbox_label.setFont(font)
        self.tracking_frame_batch_size_textbox = QLineEdit(self)
        self.tracking_frame_batch_size_textbox.move(2000, 260)
        self.tracking_frame_batch_size_textbox.resize(80, 20)
        self.tracking_frame_batch_size_textbox.setText('{0}'.format(self.frame_batch_size))
        self.tracking_frame_batch_size_textbox.setEnabled(False)
        self.tracking_frame_batch_size_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_frame_batch_size_textbox.setFont(font)
        self.tracking_frame_batch_size_textbox.textEdited.connect(self.check_tracking_frame_batch_size_textbox)

        self.tracking_starting_frame_textbox_label = QLabel(self)
        self.tracking_starting_frame_textbox_label.move(1500, 300)
        self.tracking_starting_frame_textbox_label.resize(500, 20)
        self.tracking_starting_frame_textbox_label.setText('Starting Frame: ')
        self.tracking_starting_frame_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_starting_frame_textbox_label.setFont(font)
        self.tracking_starting_frame_textbox = QLineEdit(self)
        self.tracking_starting_frame_textbox.move(2000, 300)
        self.tracking_starting_frame_textbox.resize(80, 20)
        self.tracking_starting_frame_textbox.setText('{0}'.format(self.starting_frame))
        self.tracking_starting_frame_textbox.setEnabled(False)
        self.tracking_starting_frame_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_starting_frame_textbox.setFont(font)
        self.tracking_starting_frame_textbox.textEdited.connect(self.check_tracking_starting_frame_textbox)

        self.tracking_n_frames_textbox_label = QLabel(self)
        self.tracking_n_frames_textbox_label.move(1500, 340)
        self.tracking_n_frames_textbox_label.resize(500, 20)
        self.tracking_n_frames_textbox_label.setText('Number of Frames to Track: ')
        self.tracking_n_frames_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_n_frames_textbox_label.setFont(font)
        self.tracking_n_frames_textbox = QLineEdit(self)
        self.tracking_n_frames_textbox.move(2000, 340)
        self.tracking_n_frames_textbox.resize(80, 20)
        self.tracking_n_frames_textbox.setText('{0}'.format(self.n_frames))
        self.tracking_n_frames_textbox.setEnabled(False)
        self.tracking_n_frames_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_n_frames_textbox.setFont(font)
        self.tracking_n_frames_textbox.textEdited.connect(self.check_tracking_n_frames_textbox)

        self.tracking_line_length_textbox_label = QLabel(self)
        self.tracking_line_length_textbox_label.move(1500, 380)
        self.tracking_line_length_textbox_label.resize(500, 20)
        self.tracking_line_length_textbox_label.setText('Line Length: ')
        self.tracking_line_length_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_line_length_textbox_label.setFont(font)
        self.tracking_line_length_textbox = QLineEdit(self)
        self.tracking_line_length_textbox.move(2000, 380)
        self.tracking_line_length_textbox.resize(80, 20)
        self.tracking_line_length_textbox.setText('{0}'.format(self.line_length))
        self.tracking_line_length_textbox.setEnabled(False)
        self.tracking_line_length_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_line_length_textbox.setFont(font)
        self.tracking_line_length_textbox.textEdited.connect(self.check_tracking_line_length_textbox)

        self.tracking_pixel_threshold_textbox_label = QLabel(self)
        self.tracking_pixel_threshold_textbox_label.move(1500, 420)
        self.tracking_pixel_threshold_textbox_label.resize(500, 20)
        self.tracking_pixel_threshold_textbox_label.setText('Pixel Threshold: ')
        self.tracking_pixel_threshold_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_pixel_threshold_textbox_label.setFont(font)
        self.tracking_pixel_threshold_textbox = QLineEdit(self)
        self.tracking_pixel_threshold_textbox.move(2000, 420)
        self.tracking_pixel_threshold_textbox.resize(80, 20)
        self.tracking_pixel_threshold_textbox.setText('{0}'.format(self.pixel_threshold))
        self.tracking_pixel_threshold_textbox.setEnabled(False)
        self.tracking_pixel_threshold_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_pixel_threshold_textbox.setFont(font)
        self.tracking_pixel_threshold_textbox.textEdited.connect(self.check_tracking_pixel_threshold_textbox)

        self.tracking_frame_change_threshold_textbox_label = QLabel(self)
        self.tracking_frame_change_threshold_textbox_label.move(1500, 460)
        self.tracking_frame_change_threshold_textbox_label.resize(500, 20)
        self.tracking_frame_change_threshold_textbox_label.setText('Frame Change Threshold: ')
        self.tracking_frame_change_threshold_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_frame_change_threshold_textbox_label.setFont(font)
        self.tracking_frame_change_threshold_textbox = QLineEdit(self)
        self.tracking_frame_change_threshold_textbox.move(2000, 460)
        self.tracking_frame_change_threshold_textbox.resize(80, 20)
        self.tracking_frame_change_threshold_textbox.setText('{0}'.format(self.frame_change_threshold))
        self.tracking_frame_change_threshold_textbox.setEnabled(False)
        self.tracking_frame_change_threshold_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_frame_change_threshold_textbox.setFont(font)
        self.tracking_frame_change_threshold_textbox.textEdited.connect(self.check_tracking_frame_change_threshold_textbox)

    # Defining Update Functions
    def update_statusbar_message(self):
        if self.statusbar.currentMessage() == '':
            self.statusbar.showMessage(self.statusbar_message)
    def update_descriptors(self):
        self.video_path_folder_descriptor.setText('Video Folder: {0}'.format(self.video_path_folder))
        self.video_path_basename_descriptor.setText('Video Filename: {0}'.format(self.video_path_basename))
        self.video_n_frames_descriptor.setText('Video Total Frames: {0}'.format(self.video_n_frames))
        self.video_fps_descriptor.setText('Video FPS: {0}'.format(self.video_fps))
        self.video_format_descriptor.setText('Video Format: {0}'.format(self.video_format))
        self.frame_width_descriptor.setText('Frame Width: {0}'.format(self.video_frame_width))
        self.frame_height_descriptor.setText('Frame Height: {0}'.format(self.video_frame_height))
        self.background_path_folder_descriptor.setText('Background Folder: {0}'.format(self.background_path_folder))
        self.background_path_basename_descriptor.setText('Background Filename: {0}'.format(self.background_path_basename))
        self.save_path_descriptor.setText('Save Path: {0}'.format(self.save_path))
    def update_preview_frame(self, frame, frame_width, frame_height):
        self.preview_frame = QImage(frame.data, frame_width, frame_height, QImage.Format_Indexed8)
        if frame_height > 1000 and frame_height > frame_width:
            self.preview_frame = self.preview_frame.scaledToHeight(1000)
        elif frame_width > 1000:
            self.preview_frame = self.preview_frame.scaledToWidth(1000)
        frame = cv2.resize(frame, dsize=(self.preview_frame.width(), self.preview_frame.height()), interpolation=cv2.INTER_CUBIC).copy()
        self.preview_frame = QImage(frame.data, self.preview_frame.width(), self.preview_frame.height(), QImage.Format_Indexed8)
    def update_preview_frame_window(self):
        self.preview_frame_window.setPixmap(QPixmap.fromImage(self.preview_frame))
    def update_preview_parameters(self, activate = False, inactivate = False):
        if activate:
            if not self.preview_background_checkbox.isEnabled():
                self.preview_background_checkbox.setEnabled(True)
            if not self.preview_background_subtracted_frame_checkbox.isEnabled():
                self.preview_background_subtracted_frame_checkbox.setEnabled(True)
        if inactivate:
            if self.preview_background_checkbox.isEnabled():
                self.preview_background_checkbox.setEnabled(False)
            if self.preview_background_subtracted_frame_checkbox.isEnabled():
                self.preview_background_subtracted_frame_checkbox.setEnabled(False)
    def update_frame_window_slider(self, activate = False, inactivate = False):
        if activate:
            if not self.frame_window_slider.isEnabled():
                self.frame_window_slider.setEnabled(True)
        if inactivate:
            if self.frame_window_slider.isEnabled():
                self.frame_window_slider.setEnabled(False)
        if self.frame_window_slider.isEnabled():
            self.frame_window_slider.setMinimum(1)
            self.frame_window_slider.setMaximum(self.video_n_frames)
            self.frame_window_slider.setValue(self.frame_number)
        else:
            self.frame_window_slider.setMinimum(0)
            self.frame_window_slider.setMaximum(0)
            self.frame_window_slider.setValue(0)
    def update_preview_frame_number_textbox(self, activate = False, inactivate = False):
        if activate:
            if not self.preview_frame_number_textbox.isEnabled():
                self.preview_frame_number_textbox.setEnabled(True)
        if inactivate:
            if self.preview_frame_number_textbox.isEnabled():
                self.preview_frame_number_textbox.setEnabled(False)
        if self.preview_frame_number_textbox.isEnabled():
            self.preview_frame_number_textbox.setText('{0}'.format(self.frame_number))
        else:
            self.preview_frame_number_textbox.setText('{0}'.format(0))
    def update_preview_from_button(self, activate = False, inactivate = False):
        if activate:
            if not self.update_preview_button.isEnabled():
                self.update_preview_button.setEnabled(True)
        if inactivate:
            if self.update_preview_button.isEnabled():
                self.update_preview_button.setEnabled(False)
        if not self.preview_background:
            if self.video_path is not None:
                if self.preview_frame_number_textbox.text().isdigit():
                    if int(self.preview_frame_number_textbox.text()) > self.video_n_frames:
                        self.frame_number = self.video_n_frames
                    else:
                        if int(self.preview_frame_number_textbox.text()) != 0:
                            self.frame_number = int(self.preview_frame_number_textbox.text())
                        else:
                            self.frame_number = 1
                else:
                    self.frame_number = 1
                self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
                if self.frame is not None:
                    if self.preview_background_subtracted_frame:
                        self.frame = tr.subtract_background_from_frame(self.frame, self.background)
                    self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                    self.update_preview_frame_window()
                    self.update_frame_window_slider_position()
                    self.update_preview_frame_number_textbox()
    def update_frame_window_slider_position(self):
        self.frame_window_slider.setValue(self.frame_number)
    def update_tracking_parameters(self, activate = False, inactivate = False):
        if activate:
            if not self.tracking_n_tail_points_textbox.isEnabled():
                self.tracking_n_tail_points_textbox.setEnabled(True)
            if not self.tracking_dist_tail_points_textbox.isEnabled():
                self.tracking_dist_tail_points_textbox.setEnabled(True)
            if not self.tracking_dist_eyes_textbox.isEnabled():
                self.tracking_dist_eyes_textbox.setEnabled(True)
            if not self.tracking_dist_swim_bladder_textbox.isEnabled():
                self.tracking_dist_swim_bladder_textbox.setEnabled(True)
            if not self.tracking_frame_batch_size_textbox.isEnabled():
                self.tracking_frame_batch_size_textbox.setEnabled(True)
            if not self.tracking_starting_frame_textbox.isEnabled():
                self.tracking_starting_frame_textbox.setEnabled(True)
            if not self.tracking_n_frames_textbox.isEnabled():
                self.tracking_n_frames_textbox.setEnabled(True)
            if not self.tracking_line_length_textbox.isEnabled():
                self.tracking_line_length_textbox.setEnabled(True)
            if not self.tracking_pixel_threshold_textbox.isEnabled():
                self.tracking_pixel_threshold_textbox.setEnabled(True)
            if not self.tracking_frame_change_threshold_textbox.isEnabled():
                self.tracking_frame_change_threshold_textbox.setEnabled(True)
        if inactivate:
            if self.tracking_n_tail_points_textbox.isEnabled():
                self.tracking_n_tail_points_textbox.setEnabled(False)
            if self.tracking_dist_tail_points_textbox.isEnabled():
                self.tracking_dist_tail_points_textbox.setEnabled(False)
            if self.tracking_dist_eyes_textbox.isEnabled():
                self.tracking_dist_eyes_textbox.setEnabled(False)
            if self.tracking_dist_swim_bladder_textbox.isEnabled():
                self.tracking_dist_swim_bladder_textbox.setEnabled(False)
            if self.tracking_frame_batch_size_textbox.isEnabled():
                self.tracking_frame_batch_size_textbox.setEnabled(False)
            if self.tracking_starting_frame_textbox.isEnabled():
                self.tracking_starting_frame_textbox.setEnabled(False)
            if self.tracking_n_frames_textbox.isEnabled():
                self.tracking_n_frames_textbox.setEnabled(False)
            if self.tracking_line_length_textbox.isEnabled():
                self.tracking_line_length_textbox.setEnabled(False)
            if self.tracking_pixel_threshold_textbox.isEnabled():
                self.tracking_pixel_threshold_textbox.setEnabled(False)
            if self.tracking_frame_change_threshold_textbox.isEnabled():
                self.tracking_frame_change_threshold_textbox.setEnabled(False)
        if self.tracking_n_tail_points_textbox.isEnabled():
            self.tracking_n_tail_points_textbox.setText('{0}'.format(self.n_tail_points))
        if self.tracking_dist_tail_points_textbox.isEnabled():
            self.tracking_dist_tail_points_textbox.setText('{0}'.format(self.dist_tail_points))
        if self.tracking_dist_eyes_textbox.isEnabled():
            self.tracking_dist_eyes_textbox.setText('{0}'.format(self.dist_eyes))
        if self.tracking_dist_swim_bladder_textbox.isEnabled():
            self.tracking_dist_swim_bladder_textbox.setText('{0}'.format(self.dist_swim_bladder))
        if self.tracking_frame_batch_size_textbox.isEnabled():
            self.tracking_frame_batch_size_textbox.setText('{0}'.format(self.frame_batch_size))
        if self.tracking_starting_frame_textbox.isEnabled():
            self.tracking_starting_frame_textbox.setText('{0}'.format(self.starting_frame))
        if self.tracking_n_frames_textbox.isEnabled():
            self.tracking_n_frames_textbox.setText('{0}'.format(self.n_frames))
        if self.tracking_line_length_textbox.isEnabled():
            self.tracking_line_length_textbox.setText('{0}'.format(self.line_length))
        if self.tracking_pixel_threshold_textbox.isEnabled():
            self.tracking_pixel_threshold_textbox.setText('{0}'.format(self.pixel_threshold))
        if self.tracking_frame_change_threshold_textbox.isEnabled():
            self.tracking_frame_change_threshold_textbox.setText('{0}'.format(self.frame_change_threshold))

    # Defining Trigger Functions
    def trigger_save_background(self):
        if self.save_path is not None:
            if self.background is not None and self.background_path == 'Background calculated and loaded into memory/Background calculated and loaded into memory':
                self.background_path = '{0}/{1}_background.tif'.format(self.save_path, self.video_path_basename[:-4])
                tr.save_background_to_file(self.background, self.background_path)
                self.get_background_attributes()
                self.update_descriptors()
    def trigger_calculate_background(self):
        if self.video_path is not None:
            self.background_path = 'Background calculated and loaded into memory/Background calculated and loaded into memory'
            if self.background_path:
                self.background = tr.calculate_background(self.video_path)[0]
                self.get_background_attributes()
                self.update_descriptors()
                self.update_preview_parameters(activate = True)
    def trigger_select_save_path(self):
        self.save_path = QFileDialog.getExistingDirectory(self, 'Select save path.')
        if self.save_path:
            self.update_descriptors()
    def trigger_load_background(self):
        self.background_path, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Image Files (*.tif)", options=QFileDialog.Options())
        if self.background_path:
            self.background = tr.load_background_into_memory(self.background_path)
            self.get_background_attributes()
            self.update_descriptors()
            self.update_preview_parameters(activate = True)
            if self.video_path:
                self.update_tracking_parameters(activate = True)
    def trigger_open_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Video Files (*.avi)", options=QFileDialog.Options())
        if self.video_path:
            self.get_video_attributes()
            self.update_descriptors()
            self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
            if self.frame is not None:
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_frame_window_slider(activate = True)
                self.update_preview_frame_number_textbox(activate = True)
                self.update_preview_from_button(activate = True)
                if self.background_path:
                    self.update_tracking_parameters(activate = True)
    def trigger_moved_frame_window_slider(self):
        if self.video_path is not None:
            self.frame_number = int(self.frame_window_slider.sliderPosition())
            self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
            if self.frame is not None:
                if self.preview_background_subtracted_frame:
                    self.frame = tr.subtract_background_from_frame(self.frame, self.background)
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_preview_frame_number_textbox()
    def trigger_preview_background_checkbox(self):
        self.preview_background = self.preview_background_checkbox.isChecked()
        if self.preview_background:
            self.update_preview_frame(self.background, self.background_width, self.background_height)
            self.update_preview_frame_window()
            self.update_frame_window_slider(inactivate = True)
            self.update_preview_frame_number_textbox(inactivate = True)
            self.update_preview_from_button(inactivate = True)
        else:
            if self.video_path is not None:
                self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
                if self.frame is not None:
                    if self.preview_background_subtracted_frame:
                        self.frame = tr.subtract_background_from_frame(self.frame, self.background)
                    self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                    self.update_preview_frame_window()
                    self.update_frame_window_slider(activate = True)
                    self.update_preview_frame_number_textbox(activate = True)
                    self.update_preview_from_button(activate = True)
    def trigger_preview_background_subtracted_frame_checkbox(self):
        self.preview_background_subtracted_frame = self.preview_background_subtracted_frame_checkbox.isChecked()
        if not self.preview_background:
            self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
            if self.frame is not None:
                if self.preview_background_subtracted_frame:
                    self.frame = tr.subtract_background_from_frame(self.frame, self.background)
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_frame_window_slider()
                self.update_preview_frame_number_textbox()

    # Defining Check Functions
    def check_tracking_n_tail_points_textbox(self):
        if self.tracking_n_tail_points_textbox.text().isdigit():
            self.n_tail_points = int(self.tracking_n_tail_points_textbox.text())
    def check_tracking_dist_tail_points_textbox(self):
        if self.tracking_n_tail_points_textbox.text().isdigit():
            self.n_tail_points = int(self.tracking_n_tail_points_textbox.text())
    def check_tracking_dist_eyes_textbox(self):
        if self.tracking_dist_eyes_textbox.text().isdigit():
            self.dist_eyes = int(self.tracking_dist_eyes_textbox.text())
    def check_tracking_dist_swim_bladder_textbox(self):
        if self.tracking_dist_swim_bladder_textbox.text().isdigit():
            self.dist_swim_bladder = int(self.tracking_dist_swim_bladder_textbox.text())
    def check_tracking_frame_batch_size_textbox(self):
        if self.tracking_frame_batch_size_textbox.text().isdigit():
            self.frame_batch_size = int(self.tracking_frame_batch_size_textbox.text())
    def check_tracking_starting_frame_textbox(self):
        if self.tracking_starting_frame_textbox.text().isdigit():
            self.starting_frame = int(self.tracking_starting_frame_textbox.text())
    def check_tracking_n_frames_textbox(self):
        if self.tracking_n_frames_textbox.text().isdigit():
            self.n_frames = int(self.tracking_n_frames_textbox.text())
    def check_tracking_line_length_textbox(self):
        if self.tracking_line_length_textbox.text().isdigit():
            self.line_length = int(self.tracking_line_length_textbox.text())
    def check_tracking_pixel_threshold_textbox(self):
        if self.tracking_pixel_threshold_textbox.text().isdigit():
            self.pixel_threshold = int(self.tracking_pixel_threshold_textbox.text())
    def check_tracking_frame_change_threshold_textbox(self):
        if self.tracking_frame_change_threshold_textbox.text().isdigit():
            self.frame_change_threshold = int(self.tracking_frame_change_threshold_textbox.text())

    # Defining Event Functions
    def closeEvent(self, event):
        event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
