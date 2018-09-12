'''Software Written by Nicholas Guilbeault 2018'''

# import python modules
import sys
import os
import subprocess
import cv2
import numpy as np
import free_swimming_tail_tracking as tr
import matplotlib.cm as cm
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.get_main_window_attributes()
        self.add_menubar()
        self.add_options_to_menubar()
        self.tracking_tab = TrackingTab()
        self.setCentralWidget(self.tracking_tab)
        self.setMenuBar(self.menubar)
        self.setWindowTitle('Free Swimming Tail Tracking')
        self.setWindowState(Qt.WindowMaximized)
        self.show()
    def add_menubar(self):
        self.menubar = QMenuBar()
        self.menubar.resize(self.main_window_width, self.menubar.height())
    def get_main_window_attributes(self):
        self.main_window_width = QDesktopWidget().availableGeometry().width()
        self.main_window_height = QDesktopWidget().availableGeometry().height()
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

        self.unload_all_action = QAction('&Unload All', self)
        self.unload_all_action.setShortcut('Ctrl+U')
        self.unload_all_action.setStatusTip('Unload All Things From Memory')
        self.unload_all_action.triggered.connect(self.trigger_unload_all)
        self.options_menu.addAction(self.unload_all_action)

    def trigger_save_background(self):
        self.tracking_tab.tracking_tab.tracking_content.trigger_save_background()
    def trigger_calculate_background(self):
        self.tracking_tab.tracking_tab.tracking_content.trigger_calculate_background()
    def trigger_select_save_path(self):
        self.tracking_tab.tracking_tab.tracking_content.trigger_select_save_path()
    def trigger_load_background(self):
        self.tracking_tab.tracking_tab.tracking_content.trigger_load_background()
    def trigger_open_video(self):
        self.tracking_tab.tracking_tab.tracking_content.trigger_open_video()
    def trigger_unload_all(self):
        self.tracking_tab.tracking_tab.tracking_content.trigger_unload_all()

class TrackingTab(QTabWidget):

    def __init__(self, parent = None):
        super(TrackingTab, self).__init__(parent)
        self.tracking_tab = TrackingScroll()
        self.addTab(self.tracking_tab,"Tracking")

class TrackingScroll(QScrollArea):

    def __init__(self, parent = None):
        super(TrackingScroll, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tracking_content = TrackingContent()
        self.setWidget(self.tracking_content)
        # self.setWidgetResizable(True)

class TrackingContent(QMainWindow):

    # Defining Initialization Functions
    def __init__(self):
        super(TrackingContent, self).__init__()
        self.initUI()
    def initUI(self):
        self.initialize_class_variables()
        self.get_main_window_attributes()
        self.add_preview_frame_window()
        self.add_descriptors_window()
        self.add_descriptors_to_window()
        self.add_frame_window_slider()
        self.add_preview_frame_number_textbox()
        self.add_update_preview_button()
        self.add_frame_change_buttons()
        self.add_preview_parameters_window()
        self.add_preview_parameters_to_window()
        self.add_tracking_parameters_window()
        self.add_tracking_parameters_to_window()
        self.add_tracking_parameters_buttons()
        self.add_colour_parameters_window()
        self.add_colour_parameters_to_window()
        self.add_colour_parameters_buttons()
        self.setWindowTitle('Free Swimming Tail Tracking')
        self.resize(2560, 1400)
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
        self.frame_number = 1
        self.status_bar_message = ''
        self.background_path = None
        self.background_path_basename = None
        self.background_path_folder = None
        self.save_path = None
        self.preview_background = False
        self.preview_background_subtracted_frame = False
        self.preview_tracking_results = False
        self.n_tail_points = 0
        self.dist_tail_points = 0
        self.dist_eyes = 0
        self.dist_swim_bladder = 0
        self.frame_batch_size = 0
        self.starting_frame = 0
        self.n_frames = None
        self.line_length = 0
        self.pixel_threshold = 0
        self.frame_change_threshold = 0
        self.colours = []

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

        self.unload_all_action = QAction('&Unload All', self)
        self.unload_all_action.setShortcut('Ctrl+U')
        self.unload_all_action.setStatusTip('Unload All Things From Memory')
        self.unload_all_action.triggered.connect(self.trigger_unload_all)
        self.options_menu.addAction(self.unload_all_action)
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
        self.video_path_folder_descriptor.resize(480, 20)
        self.video_path_folder_descriptor.setText('Video Folder: {0}'.format(self.video_path_folder))
        self.video_path_folder_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_path_folder_descriptor.setFont(font)

        self.video_path_basename_descriptor = QLabel(self)
        self.video_path_basename_descriptor.move(1025, 140)
        self.video_path_basename_descriptor.resize(480, 20)
        self.video_path_basename_descriptor.setText('Video Filename: {0}'.format(self.video_path_basename))
        self.video_path_basename_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_path_basename_descriptor.setFont(font)

        self.video_n_frames_descriptor = QLabel(self)
        self.video_n_frames_descriptor.move(1025, 180)
        self.video_n_frames_descriptor.resize(480, 20)
        self.video_n_frames_descriptor.setText('Video Total Frames: {0}'.format(self.video_n_frames))
        self.video_n_frames_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_n_frames_descriptor.setFont(font)

        self.video_fps_descriptor = QLabel(self)
        self.video_fps_descriptor.move(1025, 220)
        self.video_fps_descriptor.resize(480, 20)
        self.video_fps_descriptor.setText('Video FPS: {0}'.format(self.video_fps))
        self.video_fps_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_fps_descriptor.setFont(font)

        self.video_format_descriptor = QLabel(self)
        self.video_format_descriptor.move(1025, 260)
        self.video_format_descriptor.resize(480, 20)
        self.video_format_descriptor.setText('Video Format: {0}'.format(self.video_format))
        self.video_format_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_format_descriptor.setFont(font)

        self.frame_width_descriptor = QLabel(self)
        self.frame_width_descriptor.move(1025, 300)
        self.frame_width_descriptor.resize(480, 20)
        self.frame_width_descriptor.setText('Frame Width: {0}'.format(self.video_frame_width))
        self.frame_width_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.frame_width_descriptor.setFont(font)

        self.frame_height_descriptor = QLabel(self)
        self.frame_height_descriptor.move(1025, 340)
        self.frame_height_descriptor.resize(480, 20)
        self.frame_height_descriptor.setText('Frame Height: {0}'.format(self.video_frame_height))
        self.frame_height_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.frame_height_descriptor.setFont(font)

        self.background_path_folder_descriptor = QLabel(self)
        self.background_path_folder_descriptor.move(1025, 380)
        self.background_path_folder_descriptor.resize(480, 20)
        self.background_path_folder_descriptor.setText('Background Folder: {0}'.format(self.background_path_folder))
        self.background_path_folder_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.background_path_folder_descriptor.setFont(font)

        self.background_path_basename_descriptor = QLabel(self)
        self.background_path_basename_descriptor.move(1025, 420)
        self.background_path_basename_descriptor.resize(480, 20)
        self.background_path_basename_descriptor.setText('Background Filename: {0}'.format(self.background_path_basename))
        self.background_path_basename_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.background_path_basename_descriptor.setFont(font)

        self.save_path_descriptor = QLabel(self)
        self.save_path_descriptor.move(1025, 460)
        self.save_path_descriptor.resize(480, 20)
        self.save_path_descriptor.setText('Save Path: {0}'.format(self.save_path))
        self.save_path_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.save_path_descriptor.setFont(font)
    def add_frame_window_slider(self):
        self.frame_window_slider = QSlider(Qt.Horizontal, self)
        self.frame_window_slider.setToolTip('Move slider to change preview frame number.')
        self.frame_window_slider.move(5, 1035)
        self.frame_window_slider.resize(1000, 20)
        self.frame_window_slider.setEnabled(False)
        self.frame_window_slider.setTickInterval(0)
        self.frame_window_slider.setSingleStep(0)
        self.frame_window_slider.sliderMoved.connect(self.check_frame_window_slider_moved)
        self.update_frame_window_slider(inactivate = True)
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
        self.preview_frame_number_textbox.returnPressed.connect(self.check_preview_frame_number_textbox)
        self.update_preview_frame_number_textbox(inactivate = True)
    def add_update_preview_button(self):
        font = QFont()
        font.setPointSize(10)
        self.update_preview_button = QPushButton('Update Preview', self)
        self.update_preview_button.move(5, 1090)
        self.update_preview_button.resize(245, 50)
        self.update_preview_button.setFont(font)
        self.update_preview_button.clicked.connect(self.check_preview_frame_number_textbox)
        self.update_update_preview_button(inactivate = True)
    def add_frame_change_buttons(self):
        self.large_frame_decrease_button = QPushButton(self)
        self.large_frame_decrease_button.setIcon(QIcon('button_icon_1.png'))
        self.large_frame_decrease_button.setIconSize(QSize(76, 76))
        self.large_frame_decrease_button.move(260, 1060)
        self.large_frame_decrease_button.resize(80, 80)
        self.large_frame_decrease_button.clicked.connect(self.check_large_frame_decrease_button)

        self.medium_frame_decrease_button = QPushButton(self)
        self.medium_frame_decrease_button.setIcon(QIcon('button_icon_2.png'))
        self.medium_frame_decrease_button.setIconSize(QSize(76, 76))
        self.medium_frame_decrease_button.move(345, 1060)
        self.medium_frame_decrease_button.resize(80, 80)
        self.medium_frame_decrease_button.clicked.connect(self.check_medium_frame_decrease_button)

        self.small_frame_decrease_button = QPushButton(self)
        self.small_frame_decrease_button.setIcon(QIcon('button_icon_3.png'))
        self.small_frame_decrease_button.setIconSize(QSize(76, 76))
        self.small_frame_decrease_button.move(430, 1060)
        self.small_frame_decrease_button.resize(80, 80)
        self.small_frame_decrease_button.clicked.connect(self.check_small_frame_decrease_button)

        self.small_frame_increase_button = QPushButton(self)
        self.small_frame_increase_button.setIcon(QIcon('button_icon_4.png'))
        self.small_frame_increase_button.setIconSize(QSize(76, 76))
        self.small_frame_increase_button.move(515, 1060)
        self.small_frame_increase_button.resize(80, 80)
        self.small_frame_increase_button.clicked.connect(self.check_small_frame_increase_button)

        self.medium_frame_increase_button = QPushButton(self)
        self.medium_frame_increase_button.setIcon(QIcon('button_icon_5.png'))
        self.medium_frame_increase_button.setIconSize(QSize(76, 76))
        self.medium_frame_increase_button.move(600, 1060)
        self.medium_frame_increase_button.resize(80, 80)
        self.medium_frame_increase_button.clicked.connect(self.check_medium_frame_increase_button)

        self.large_frame_increase_button = QPushButton(self)
        self.large_frame_increase_button.setIcon(QIcon('button_icon_6.png'))
        self.large_frame_increase_button.setIconSize(QSize(76, 76))
        self.large_frame_increase_button.move(685, 1060)
        self.large_frame_increase_button.resize(80, 80)
        self.large_frame_increase_button.clicked.connect(self.check_large_frame_increase_button)
        self.update_frame_change_buttons(inactivate = True)
    def add_preview_parameters_window(self):
        font = QFont()
        font.setPointSize(18)
        self.preview_parameters_window = QLabel(self)
        self.preview_parameters_window.setFrameShape(QFrame.Panel)
        self.preview_parameters_window.setFrameShadow(QFrame.Sunken)
        self.preview_parameters_window.setLineWidth(5)
        self.preview_parameters_window.move(1015, 1035)
        self.preview_parameters_window.resize(500, 330)
        self.preview_parameters_window.setText('Preview Parameters')
        self.preview_parameters_window.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.preview_parameters_window.setFont(font)
    def add_preview_parameters_to_window(self):
        font = QFont()
        font.setPointSize(10)
        self.preview_background_checkbox = QCheckBox(self)
        self.preview_background_checkbox.move(1025, 1110)
        self.preview_background_checkbox.setEnabled(False)
        self.preview_background_checkbox.stateChanged.connect(self.check_preview_background_checkbox)
        self.preview_background_checkbox_label = QLabel(self)
        self.preview_background_checkbox_label.move(1045, 1113)
        self.preview_background_checkbox_label.resize(500, 20)
        self.preview_background_checkbox_label.setText('Preview Background')
        self.preview_background_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_background_checkbox_label.setFont(font)

        self.preview_background_subtracted_frame_checkbox = QCheckBox(self)
        self.preview_background_subtracted_frame_checkbox.move(1025, 1150)
        self.preview_background_subtracted_frame_checkbox.stateChanged.connect(self.check_preview_background_subtracted_frame_checkbox)
        self.preview_background_subtracted_frame_checkbox_label = QLabel(self)
        self.preview_background_subtracted_frame_checkbox_label.move(1045, 1153)
        self.preview_background_subtracted_frame_checkbox_label.resize(500, 20)
        self.preview_background_subtracted_frame_checkbox_label.setText('Preview Background Subtracted Frames')
        self.preview_background_subtracted_frame_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_background_subtracted_frame_checkbox_label.setFont(font)

        self.preview_tracking_results_checkbox = QCheckBox(self)
        self.preview_tracking_results_checkbox.move(1025, 1190)
        self.preview_tracking_results_checkbox.stateChanged.connect(self.check_preview_tracking_results_checkbox)
        self.preview_tracking_results_checkbox.setEnabled(False)
        self.preview_tracking_results_checkbox_label = QLabel(self)
        self.preview_tracking_results_checkbox_label.move(1045, 1193)
        self.preview_tracking_results_checkbox_label.resize(500, 20)
        self.preview_tracking_results_checkbox_label.setText('Preview Tracking Results')
        self.preview_tracking_results_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_tracking_results_checkbox_label.setFont(font)
        self.update_preview_parameters(inactivate = True)
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
        self.tracking_n_tail_points_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_n_tail_points_textbox.setFont(font)
        # self.tracking_n_tail_points_textbox.returnPressed.connect(self.check_tracking_n_tail_points_textbox)
        self.tracking_n_tail_points_textbox.textChanged.connect(self.check_tracking_n_tail_points_textbox)

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
        self.tracking_dist_tail_points_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_dist_tail_points_textbox.setFont(font)
        self.tracking_dist_tail_points_textbox.returnPressed.connect(self.check_tracking_dist_tail_points_textbox)

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
        self.tracking_dist_eyes_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_dist_eyes_textbox.setFont(font)
        self.tracking_dist_eyes_textbox.returnPressed.connect(self.check_tracking_dist_eyes_textbox)

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
        self.tracking_dist_swim_bladder_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_dist_swim_bladder_textbox.setFont(font)
        self.tracking_dist_swim_bladder_textbox.returnPressed.connect(self.check_tracking_dist_swim_bladder_textbox)

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
        self.tracking_frame_batch_size_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_frame_batch_size_textbox.setFont(font)
        self.tracking_frame_batch_size_textbox.returnPressed.connect(self.check_tracking_frame_batch_size_textbox)

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
        self.tracking_starting_frame_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_starting_frame_textbox.setFont(font)
        self.tracking_starting_frame_textbox.returnPressed.connect(self.check_tracking_starting_frame_textbox)

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
        self.tracking_n_frames_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_n_frames_textbox.setFont(font)
        self.tracking_n_frames_textbox.returnPressed.connect(self.check_tracking_n_frames_textbox)

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
        self.tracking_line_length_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_line_length_textbox.setFont(font)
        self.tracking_line_length_textbox.returnPressed.connect(self.check_tracking_line_length_textbox)

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
        self.tracking_pixel_threshold_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_pixel_threshold_textbox.setFont(font)
        self.tracking_pixel_threshold_textbox.returnPressed.connect(self.check_tracking_pixel_threshold_textbox)

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
        self.tracking_frame_change_threshold_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.tracking_frame_change_threshold_textbox.setFont(font)
        self.tracking_frame_change_threshold_textbox.returnPressed.connect(self.check_tracking_frame_change_threshold_textbox)
        self.trigger_load_default_tracking_parameters()
        self.update_tracking_parameters(inactivate = True)
    def add_tracking_parameters_buttons(self):
        font = QFont()
        font.setPointSize(10)
        self.load_default_tracking_parameters_button = QPushButton('Load Default Tracking Parameters', self)
        self.load_default_tracking_parameters_button.move(1800, 500)
        self.load_default_tracking_parameters_button.resize(400, 100)
        self.load_default_tracking_parameters_button.setFont(font)
        self.load_default_tracking_parameters_button.clicked.connect(self.trigger_load_default_tracking_parameters)

        self.load_previous_tracking_parameters_button = QPushButton('Load Previous Tracking Parameters', self)
        self.load_previous_tracking_parameters_button.move(1800, 610)
        self.load_previous_tracking_parameters_button.resize(400, 100)
        self.load_previous_tracking_parameters_button.setFont(font)
        self.load_previous_tracking_parameters_button.clicked.connect(self.trigger_load_previous_tracking_parameters)

        self.save_current_tracking_parameters_button = QPushButton('Save Current Tracking Parameters', self)
        self.save_current_tracking_parameters_button.move(1800, 720)
        self.save_current_tracking_parameters_button.resize(400, 100)
        self.save_current_tracking_parameters_button.setFont(font)
        self.save_current_tracking_parameters_button.clicked.connect(self.trigger_save_current_tracking_parameters)

        font.setPointSize(12)

        self.track_video_button = QPushButton('Track Video', self)
        self.track_video_button.move(1700, 830)
        self.track_video_button.resize(600, 150)
        self.track_video_button.setFont(font)
        self.track_video_button.clicked.connect(self.trigger_track_video)
        self.update_tracking_parameters_buttons(inactivate = True)
    def add_colour_parameters_window(self):
        font = QFont()
        font.setPointSize(18)
        self.colour_parameters_window = QLabel(self)
        self.colour_parameters_window.setFrameShape(QFrame.Panel)
        self.colour_parameters_window.setFrameShadow(QFrame.Sunken)
        self.colour_parameters_window.setLineWidth(5)
        self.colour_parameters_window.move(1525, 1035)
        self.colour_parameters_window.resize(1030, 330)
        self.colour_parameters_window.setText('Colour Parameters')
        self.colour_parameters_window.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.colour_parameters_window.setFont(font)
    def add_colour_parameters_to_window(self):
        self.colour_label_list = []
        self.colour_textbox_list = []
        self.colour_button_list = []
        font = QFont()
        font.setPointSize(10)
        self.use_same_colour_for_eyes = True
        # count = 0
        for i in range(len(self.colours)):
            count = int(i / 6)
            # if i % 6 == 0 and i > 0:
            #     count += 1
            colour_label_pos = [1565 + count * 250, 1100 + (i * 45) - (count * 270)]
            colour_label = QLabel(self)
            if i == len(self.colours) - 1:
                colour_label.setText('Heading Angle: ')
            if i == len(self.colours) - 2:
                colour_label.setText('First Eye: ')
            if i == len(self.colours) - 3:
                if self.use_same_colour_for_eyes:
                    colour_label.setText('Second Eye: ')
                else:
                    colour_label.setText('Second Eye: ')
            if i < len(self.colours) - 3 :
                colour_label.setText('Tail Point {0}: '.format(i + 1))
            colour_label.move(colour_label_pos[0], colour_label_pos[1])
            colour_label.resize(100, 20)
            colour_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            colour_label.setFont(font)
            self.colour_label_list.append(colour_label)
            colour_textbox_pos = [1665 + count * 250, 1100 + (i * 45) - (count * 270)]
            colour_textbox = QLineEdit(self)
            colour_textbox.setText('{0}'.format(self.colours[i]))
            colour_textbox.move(colour_textbox_pos[0], colour_textbox_pos[1])
            colour_textbox.resize(120, 20)
            colour_textbox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            colour_textbox.setFont(font)
            colour_textbox.setEnabled(False)
            self.colour_textbox_list.append(colour_textbox)
            colour_button_pos = [1795 + count * 250, 1100 + (i * 45) - (count * 270)]
            colour_button = QPushButton(self)
            colour_button.setIcon(QIcon('colour_wheel.jpg'))
            colour_button.setIconSize(QSize(18, 18))
            colour_button.move(colour_button_pos[0], colour_button_pos[1])
            colour_button.resize(20, 20)
            colour_button.clicked.connect(partial(self.trigger_update_single_colour, i))
            self.colour_button_list.append(colour_button)
        self.update_colour_parameters(inactivate = True)
        self.update_colours()
    def add_colour_parameters_buttons(self):
        self.load_default_colours_button = QPushButton('Load Default Colours', self)
        self.load_default_colours_button.move(2395, 1100)
        self.load_default_colours_button.resize(150, 40)
        self.load_default_colours_button.clicked.connect(self.check_load_default_colours_button)
        self.update_colour_parameters_buttons(inactivate = True)

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
    def update_preview_frame(self, frame, frame_width, frame_height, inactivate = False, grayscale = True):
        if grayscale:
            format = QImage.Format_Indexed8
        else:
            format = QImage.Format_RGB888
        self.preview_frame = QImage(frame.data, frame_width, frame_height, format)
        if frame_height > 1000 and frame_height > frame_width:
           self.preview_frame = self.preview_frame.scaledToHeight(1000)
        elif frame_width > 1000:
           self.preview_frame = self.preview_frame.scaledToWidth(1000)
        frame = cv2.resize(frame, dsize=(self.preview_frame.width(), self.preview_frame.height()), interpolation=cv2.INTER_CUBIC).copy()
        self.preview_frame = QImage(frame.data, self.preview_frame.width(), self.preview_frame.height(), format)
    def update_preview_frame_window(self, clear = False):
        if not clear:
            self.preview_frame_window.setPixmap(QPixmap.fromImage(self.preview_frame))
        else:
            self.preview_frame_window.clear()
    def update_preview_parameters(self, activate = False, inactivate = False, activate_preview_background = False):
        if activate_preview_background:
            if not self.preview_background_checkbox.isEnabled():
                self.preview_background_checkbox.setEnabled(True)
        if activate:
            if not self.preview_background_checkbox.isEnabled():
                self.preview_background_checkbox.setEnabled(True)
            if not self.preview_background_subtracted_frame_checkbox.isEnabled():
                self.preview_background_subtracted_frame_checkbox.setEnabled(True)
            if not self.preview_tracking_results_checkbox.isEnabled():
                self.preview_tracking_results_checkbox.setEnabled(True)
        if inactivate:
            if self.preview_background_checkbox.isEnabled():
                self.preview_background_checkbox.setEnabled(False)
            if self.preview_background_subtracted_frame_checkbox.isEnabled():
                self.preview_background_subtracted_frame_checkbox.setEnabled(False)
            if self.preview_tracking_results_checkbox.isEnabled():
                self.preview_tracking_results_checkbox.setEnabled(False)
    def update_frame_window_slider(self, activate = False, inactivate = False):
        if activate:
            if not self.frame_window_slider.isEnabled():
                self.frame_window_slider.setEnabled(True)
                self.frame_window_slider.setTickPosition(QSlider.TicksBelow)
        if inactivate:
            if self.frame_window_slider.isEnabled():
                self.frame_window_slider.setEnabled(False)
                self.frame_window_slider.setTickPosition(QSlider.NoTicks)
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
    def update_update_preview_button(self, activate = False, inactivate = False):
        if activate:
            if not self.update_preview_button.isEnabled():
                self.update_preview_button.setEnabled(True)
        if inactivate:
            if self.update_preview_button.isEnabled():
                self.update_preview_button.setEnabled(False)
    def update_frame_change_buttons(self, activate = False, inactivate = False):
        if activate:
            if not self.large_frame_decrease_button.isEnabled():
                self.large_frame_decrease_button.setEnabled(True)
            if not self.medium_frame_decrease_button.isEnabled():
                self.medium_frame_decrease_button.setEnabled(True)
            if not self.small_frame_decrease_button.isEnabled():
                self.small_frame_decrease_button.setEnabled(True)
            if not self.small_frame_increase_button.isEnabled():
                self.small_frame_increase_button.setEnabled(True)
            if not self.medium_frame_increase_button.isEnabled():
                self.medium_frame_increase_button.setEnabled(True)
            if not self.large_frame_increase_button.isEnabled():
                self.large_frame_increase_button.setEnabled(True)
        if inactivate:
            if self.large_frame_decrease_button.isEnabled():
                self.large_frame_decrease_button.setEnabled(False)
            if self.medium_frame_decrease_button.isEnabled():
                self.medium_frame_decrease_button.setEnabled(False)
            if self.small_frame_decrease_button.isEnabled():
                self.small_frame_decrease_button.setEnabled(False)
            if self.small_frame_increase_button.isEnabled():
                self.small_frame_increase_button.setEnabled(False)
            if self.medium_frame_increase_button.isEnabled():
                self.medium_frame_increase_button.setEnabled(False)
            if self.large_frame_increase_button.isEnabled():
                self.large_frame_increase_button.setEnabled(False)
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
    def update_tracking_parameters_buttons(self, activate = False, inactivate = False):
        if activate:
            if not self.load_default_tracking_parameters_button.isEnabled():
                self.load_default_tracking_parameters_button.setEnabled(True)
            if not self.load_previous_tracking_parameters_button.isEnabled():
                self.load_previous_tracking_parameters_button.setEnabled(True)
            if not self.save_current_tracking_parameters_button.isEnabled():
                self.save_current_tracking_parameters_button.setEnabled(True)
            if not self.track_video_button.isEnabled():
                self.track_video_button.setEnabled(True)
        if inactivate:
            if self.load_default_tracking_parameters_button.isEnabled():
                self.load_default_tracking_parameters_button.setEnabled(False)
            if self.load_previous_tracking_parameters_button.isEnabled():
                self.load_previous_tracking_parameters_button.setEnabled(False)
            if self.save_current_tracking_parameters_button.isEnabled():
                self.save_current_tracking_parameters_button.setEnabled(False)
            if self.track_video_button.isEnabled():
                self.track_video_button.setEnabled(False)
    def update_colour_parameters(self, activate = False, inactivate = False):
        if inactivate:
            for i in range(len(self.colour_button_list)):
                if self.colour_button_list[i].isEnabled():
                    self.colour_button_list[i].setEnabled(False)
        if activate:
            for i in range(len(self.colour_button_list)):
                if not self.colour_button_list[i].isEnabled():
                    self.colour_button_list[i].setEnabled(True)
    def update_colour_parameters_buttons(self, activate = False, inactivate = False):
        if activate:
            if not self.load_default_colours_button.isEnabled():
                self.load_default_colours_button.setEnabled(True)
        if inactivate:
            if self.load_default_colours_button.isEnabled():
                self.load_default_colours_button.setEnabled(False)
    def update_colours(self):
        if self.n_tail_points < len(self.colours) - 3:
            for i in range(len(self.colours) - 3 - self.n_tail_points):
                self.colour_label_list[len(self.colour_label_list) - 1].deleteLater()
                self.colour_textbox_list[len(self.colour_textbox_list) - 1].deleteLater()
                self.colour_button_list[len(self.colour_button_list) - 1].deleteLater()
                del(self.colour_label_list[len(self.colour_label_list) - 1])
                del(self.colour_textbox_list[len(self.colour_textbox_list) - 1])
                del(self.colour_button_list[len(self.colour_button_list) - 1])
                del(self.colours[self.n_tail_points])
            for i in range(len(self.colours)):
                if i == len(self.colours) - 1:
                    self.colour_label_list[i].setText('Heading Angle: ')
                if i == len(self.colours) - 2:
                    self.colour_label_list[i].setText('First Eye: ')
                if i == len(self.colours) - 3:
                    if self.use_same_colour_for_eyes:
                        self.colour_label_list[i].setText('Second Eye: ')
                    else:
                        self.colour_label_list[i].setText('Second Eye: ')
                if i < len(self.colours) - 3 :
                    self.colour_label_list[i].setText('Tail Point {0}: '.format(i + 1))
                self.colour_textbox_list[i].setText('{0}'.format(self.colours[i]))
        elif self.n_tail_points > len(self.colours) - 3:
            font = QFont()
            font.setPointSize(10)
            for i in range(self.n_tail_points + 3 - len(self.colours)):
                self.colours.insert(i + self.n_tail_points - 1, (0, 0, 0))
                count = int((i + len(self.colours) - 1) / 6)
                colour_label_pos = [1565 + count * 250, 1100 + ((i + len(self.colours) - 1) * 45) - (count * 270)]
                colour_label = QLabel(self)
                colour_label.move(colour_label_pos[0], colour_label_pos[1])
                colour_label.resize(100, 20)
                colour_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                colour_label.setText('sdfsdf')
                colour_label.setFont(font)
                colour_label.show()
                self.colour_label_list.append(colour_label)
                colour_textbox_pos = [1665 + count * 250, 1100 + ((i + len(self.colours) - 1) * 45) - (count * 270)]
                colour_textbox = QLineEdit(self)
                colour_textbox.move(colour_textbox_pos[0], colour_textbox_pos[1])
                colour_textbox.resize(120, 20)
                colour_textbox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                colour_textbox.setFont(font)
                colour_textbox.setEnabled(False)
                colour_textbox.show()
                self.colour_textbox_list.append(colour_textbox)
                colour_button_pos = [1795 + count * 250, 1100 + ((i + len(self.colours) - 1) * 45) - (count * 270)]
                colour_button = QPushButton(self)
                colour_button.setIcon(QIcon('colour_wheel.jpg'))
                colour_button.setIconSize(QSize(18, 18))
                colour_button.move(colour_button_pos[0], colour_button_pos[1])
                colour_button.resize(20, 20)
                colour_button.clicked.connect(partial(self.trigger_update_single_colour, i + self.n_tail_points - 1))
                colour_button.show()
                self.colour_button_list.append(colour_button)
            for i in range(len(self.colours)):
                if i == len(self.colours) - 1:
                    self.colour_label_list[i].setText('Heading Angle: ')
                if i == len(self.colours) - 2:
                    self.colour_label_list[i].setText('First Eye: ')
                if i == len(self.colours) - 3:
                    if self.use_same_colour_for_eyes:
                        self.colour_label_list[i].setText('Second Eye: ')
                    else:
                        self.colour_label_list[i].setText('Second Eye: ')
                if i < len(self.colours) - 3 :
                    self.colour_label_list[i].setText('Tail Point {0}: '.format(i + 1))
                self.colour_textbox_list[i].setText('{0}'.format(self.colours[i]))
        else:
            for i in range(len(self.colours)):
                if i == len(self.colours) - 1:
                    self.colour_label_list[i].setText('Heading Angle: ')
                if i == len(self.colours) - 2:
                    self.colour_label_list[i].setText('First Eye: ')
                if i == len(self.colours) - 3:
                    if self.use_same_colour_for_eyes:
                        self.colour_label_list[i].setText('Second Eye: ')
                    else:
                        self.colour_label_list[i].setText('Second Eye: ')
                if i < len(self.colours) - 3 :
                    self.colour_label_list[i].setText('Tail Point {0}: '.format(i + 1))
                self.colour_textbox_list[i].setText('{0}'.format(self.colours[i]))

    # Defining Trigger Functions
    def trigger_save_background(self):
        if self.save_path is not None:
            if self.background is not None and self.background_path == 'Background calculated and loaded into memory/Background calculated and loaded into memory':
                self.background_path = '{0}/{1}_background.tif'.format(self.save_path, self.video_path_basename[:-4])
                tr.save_background_to_file(self.background, self.background_path)
                self.get_background_attributes()
                self.update_descriptors()
        else:
            self.save_path = self.video_path_folder
            self.background_path = '{0}/{1}_background.tif'.format(self.save_path, self.video_path_basename[:-4])
            tr.save_background_to_file(self.background, self.background_path)
            self.get_background_attributes()
            self.update_descriptors()
    def trigger_calculate_background(self):
        if self.video_path is not None:
            self.background_path = 'Background calculated and loaded into memory/Background calculated and loaded into memory'
            self.background = tr.calculate_background(self.video_path)[0]
            self.get_background_attributes()
            self.update_descriptors()
            self.update_preview_parameters(activate = True)
            self.update_tracking_parameters(activate = True)
            self.update_tracking_parameters_buttons(activate = True)
            self.update_colour_parameters(activate = True)
            self.update_colour_parameters_buttons(activate = True)
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
            if self.video_path:
                self.update_preview_parameters(activate = True)
                self.update_tracking_parameters(activate = True)
                self.update_tracking_parameters_buttons(activate = True)
                self.update_colour_parameters(activate = True)
                self.update_colour_parameters_buttons(activate = True)
            else:
                self.update_preview_parameters(activate_preview_background = True)
    def trigger_open_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self,"Open Video File", "","Video Files (*.avi)", options=QFileDialog.Options())
        if self.video_path:
            self.get_video_attributes()
            self.update_descriptors()
            success, self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
            if success and self.frame is not None:
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_frame_window_slider(activate = True)
                self.update_preview_frame_number_textbox(activate = True)
                self.update_update_preview_button(activate = True)
                self.update_frame_change_buttons(activate = True)
                if self.background_path:
                    self.update_tracking_parameters(activate = True)
                    self.update_preview_parameters(activate = True)
                    self.update_tracking_parameters_buttons(activate = True)
                    self.update_colour_parameters(activate = True)
                    self.update_colour_parameters_buttons(activate = True)
    def trigger_update_preview(self):
        if self.preview_background:
            self.update_preview_frame(self.background, self.background_width, self.background_height)
            self.update_preview_frame_window()
            self.update_frame_window_slider(inactivate = True)
            self.update_preview_frame_number_textbox(inactivate = True)
            self.update_update_preview_button(inactivate = True)
            self.update_frame_change_buttons(inactivate = True)
        else:
            if self.video_path is not None:
                success, self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
                if success and self.frame is not None:
                    use_grayscale = True
                    if self.preview_background_subtracted_frame:
                        self.frame = tr.subtract_background_from_frame(self.frame, self.background)
                        if self.preview_tracking_results:
                            results = tr.track_tail_in_frame([tr.apply_median_blur_to_frame(self.frame), success, self.n_tail_points, self.dist_tail_points, self.dist_eyes, self.dist_swim_bladder, self.pixel_threshold])
                            if results is not None:
                                self.frame = tr.annotate_tracking_results_onto_frame(self.frame, results, self.colours, self.line_length)
                                use_grayscale = False
                    elif self.preview_tracking_results:
                        results = tr.track_tail_in_frame([tr.apply_median_blur_to_frame(tr.subtract_background_from_frame(self.frame, self.background)), success, self.n_tail_points, self.dist_tail_points, self.dist_eyes, self.dist_swim_bladder, self.pixel_threshold])
                        if results is not None:
                            self.frame = tr.annotate_tracking_results_onto_frame(self.frame, results, self.colours, self.line_length)
                            use_grayscale = False
                    self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height, grayscale = use_grayscale)
                    self.update_preview_frame_window()
                    self.update_frame_window_slider(activate = True)
                    self.update_preview_frame_number_textbox(activate = True)
                    self.update_update_preview_button(activate = True)
                    self.update_frame_change_buttons(activate = True)
            else:
                self.update_preview_frame_window(clear = True)
    def trigger_load_default_tracking_parameters(self):
        self.n_tail_points = 7
        self.dist_tail_points = 5
        self.dist_eyes = 4
        self.dist_swim_bladder = 12
        self.frame_batch_size = 50
        self.starting_frame = 0
        self.n_frames = None
        self.line_length = 5
        self.pixel_threshold = 40
        self.frame_change_threshold = 10
        self.trigger_load_default_colours()
        self.update_tracking_parameters()
        self.trigger_update_preview()
    def trigger_load_previous_tracking_parameters(self):
        try:
            tracking_parameters = np.load('tracking_parameters.npy').item()
            self.n_tail_points = tracking_parameters['n_tail_points']
            self.dist_tail_points = tracking_parameters['dist_tail_points']
            self.dist_eyes = tracking_parameters['dist_eyes']
            self.dist_swim_bladder = tracking_parameters['dist_swim_bladder']
            self.frame_batch_size = tracking_parameters['frame_batch_size']
            self.starting_frame = tracking_parameters['starting_frame']
            self.n_frames = tracking_parameters['n_frames']
            self.line_length = tracking_parameters['line_length']
            self.pixel_threshold = tracking_parameters['pixel_threshold']
            self.frame_change_threshold = tracking_parameters['frame_change_threshold']
            self.update_tracking_parameters()
            self.trigger_update_preview()
        except:
            print('Error: tracking parameters not found.')
            self.trigger_load_default_tracking_parameters()
    def trigger_save_current_tracking_parameters(self):
        tracking_parameters = {'n_tail_points' : self.n_tail_points, 'dist_tail_points' : self.dist_tail_points,
            'dist_eyes' : self.dist_eyes, 'dist_swim_bladder' : self.dist_swim_bladder,
            'frame_batch_size' : self.frame_batch_size, 'starting_frame' : self.starting_frame,
            'n_frames' : self.n_frames, 'line_length' : self.line_length,
            'pixel_threshold' : self.pixel_threshold, 'frame_change_threshold' : self.frame_change_threshold}
        np.save('tracking_parameters.npy', tracking_parameters)
    def trigger_track_video(self):
        # video_path, colours, n_tail_points, dist_tail_points, dist_eyes, dist_swim_bladder = self.video_path.copy(), self.colours.copy(), self.n_tail_points.copy(), self.dist_tail_points.copy(), self.dist_eyes.copy(), self.dist_swim_bladder.copy()
        # self.trigger_unload_all()
        tr.track_video(self.video_path, self.colours, self.n_tail_points, self.dist_tail_points, self.dist_eyes, self.dist_swim_bladder, n_frames = self.n_frames, starting_frame = self.starting_frame, save_path = self.save_path, background_path = self.background_path, line_length = self.line_length, video_fps = self.video_fps, pixel_threshold = self.pixel_threshold, frame_change_threshold = self.frame_change_threshold)
    def trigger_unload_all(self):
        if self.preview_background_checkbox.isChecked():
            self.preview_background_checkbox.setChecked(False)
        if self.preview_background_subtracted_frame_checkbox.isChecked():
            self.preview_background_subtracted_frame_checkbox.setChecked(False)
        if self.preview_tracking_results_checkbox.isChecked():
            self.preview_tracking_results_checkbox.setChecked(False)
        self.initialize_class_variables()
        self.trigger_load_default_tracking_parameters()
        self.update_descriptors()
        self.update_preview_frame_window(clear = True)
        self.update_preview_parameters(inactivate = True)
        self.update_frame_window_slider(inactivate = True)
        self.update_preview_frame_number_textbox(inactivate = True)
        self.update_update_preview_button(inactivate = True)
        self.update_frame_change_buttons(inactivate = True)
        self.update_frame_window_slider_position()
        self.update_tracking_parameters(inactivate = True)
        self.update_tracking_parameters_buttons(inactivate = True)
        self.update_colour_parameters(inactivate = True)
        self.update_colour_parameters_buttons(inactivate = True)
    def trigger_update_single_colour(self, id):
        colour = QColorDialog.getColor().getRgb()[0:3]
        colour = (colour[0], colour[1], colour[2])
        self.colours[id] = colour
        self.colour_textbox_list[id].setText('{0}'.format(colour))
        self.trigger_update_preview()
    def trigger_load_default_colours(self):
        self.colours = [[] for i in range(self.n_tail_points + 3)]
        colour_map = cm.jet
        self.colours[-1] = (49, 191, 114)
        self.colours[-2] = (139, 139, 0)
        self.colours[-3] = (139, 139, 0)
        for i in range(self.n_tail_points):
            colour = colour_map(i / (self.n_tail_points - 1))[:3]
            self.colours[i] = (int(colour[0] * 255), int(colour[1] * 255), int(colour[2] * 255))

    # Defining Check Functions
    def check_preview_frame_number_textbox(self):
        if self.preview_frame_number_textbox.text().isdigit():
            if int(self.preview_frame_number_textbox.text()) > self.video_n_frames:
                self.frame_number = self.video_n_frames
            else:
                if int(self.preview_frame_number_textbox.text()) != 0:
                    self.frame_number = int(self.preview_frame_number_textbox.text())
                else:
                    self.frame_number = 1
        self.trigger_update_preview()
    def check_frame_window_slider_moved(self):
        self.frame_number = int(self.frame_window_slider.sliderPosition())
        self.trigger_update_preview()
    def check_preview_background_checkbox(self):
        self.preview_background = self.preview_background_checkbox.isChecked()
        self.trigger_update_preview()
    def check_preview_background_subtracted_frame_checkbox(self):
        self.preview_background_subtracted_frame = self.preview_background_subtracted_frame_checkbox.isChecked()
        self.trigger_update_preview()
    def check_large_frame_decrease_button(self):
        self.frame_number -= 100
        if self.frame_number < 1:
            self.frame_number = 1
        self.trigger_update_preview()
    def check_medium_frame_decrease_button(self):
        self.frame_number -= 10
        if self.frame_number < 1:
            self.frame_number = 1
        self.trigger_update_preview()
    def check_small_frame_decrease_button(self):
        self.frame_number -= 1
        if self.frame_number < 1:
            self.frame_number = 1
        self.trigger_update_preview()
    def check_small_frame_increase_button(self):
        self.frame_number += 1
        if self.frame_number > self.video_n_frames:
            self.frame_number = self.video_n_frames
        self.trigger_update_preview()
    def check_medium_frame_increase_button(self):
        self.frame_number += 10
        if self.frame_number > self.video_n_frames:
            self.frame_number = self.video_n_frames
        self.trigger_update_preview()
    def check_large_frame_increase_button(self):
        self.frame_number += 100
        if self.frame_number > self.video_n_frames:
            self.frame_number = self.video_n_frames
        self.trigger_update_preview()
    def check_preview_tracking_results_checkbox(self):
        self.preview_tracking_results = self.preview_tracking_results_checkbox.isChecked()
        self.trigger_update_preview()
    def check_tracking_n_tail_points_textbox(self):
        if self.tracking_n_tail_points_textbox.text().isdigit():
            self.n_tail_points = int(self.tracking_n_tail_points_textbox.text())
            if self.n_tail_points != len(self.colours) - 3:
                self.update_colours()
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_dist_tail_points_textbox(self):
        if self.tracking_dist_tail_points_textbox.text().isdigit():
            self.dist_tail_points = int(self.tracking_dist_tail_points_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_dist_eyes_textbox(self):
        if self.tracking_dist_eyes_textbox.text().isdigit():
            self.dist_eyes = int(self.tracking_dist_eyes_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_dist_swim_bladder_textbox(self):
        if self.tracking_dist_swim_bladder_textbox.text().isdigit():
            self.dist_swim_bladder = int(self.tracking_dist_swim_bladder_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_frame_batch_size_textbox(self):
        if self.tracking_frame_batch_size_textbox.text().isdigit():
            self.frame_batch_size = int(self.tracking_frame_batch_size_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_starting_frame_textbox(self):
        if self.tracking_starting_frame_textbox.text().isdigit():
            self.starting_frame = int(self.tracking_starting_frame_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_n_frames_textbox(self):
        if self.tracking_n_frames_textbox.text().isdigit():
            self.n_frames = int(self.tracking_n_frames_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_line_length_textbox(self):
        if self.tracking_line_length_textbox.text().isdigit():
            self.line_length = int(self.tracking_line_length_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_pixel_threshold_textbox(self):
        if self.tracking_pixel_threshold_textbox.text().isdigit():
            self.pixel_threshold = int(self.tracking_pixel_threshold_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_tracking_frame_change_threshold_textbox(self):
        if self.tracking_frame_change_threshold_textbox.text().isdigit():
            self.frame_change_threshold = int(self.tracking_frame_change_threshold_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
    def check_load_default_colours_button(self):
        self.trigger_load_default_colours()
        self.update_colours()
        self.trigger_update_preview()

    # Defining Event Functions
    def closeEvent(self, event):
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
