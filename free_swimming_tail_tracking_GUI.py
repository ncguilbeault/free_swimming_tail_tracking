'''Software Written by Nicholas Guilbeault 2018'''

# import python modules
import sys
import os
import cv2
import numpy as np
import free_swimming_tail_tracking_UT as ut
import matplotlib.cm as cm
import time
from functools import partial
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.get_main_window_attributes()
        self.add_menubar()
        self.add_tracking_options_to_menubar()
        self.add_plotting_options_to_menubar()
        self.main_tab = MainTab()
        self.setCentralWidget(self.main_tab)
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
    def add_tracking_options_to_menubar(self):
        self.tracking_options_menu = self.menubar.addMenu('&Tracking Options')

        self.open_video_action = QAction('&Open Video', self)
        self.open_video_action.setShortcut('Ctrl+O')
        self.open_video_action.setStatusTip('Open Video')
        self.open_video_action.triggered.connect(self.trigger_open_video)
        self.tracking_options_menu.addAction(self.open_video_action)

        self.select_save_path_action = QAction('&Select Save Path', self)
        self.select_save_path_action.setShortcut('Ctrl+P')
        self.select_save_path_action.setStatusTip('Select Save Path')
        self.select_save_path_action.triggered.connect(self.trigger_select_save_path)
        self.tracking_options_menu.addAction(self.select_save_path_action)

        self.load_background_action = QAction('&Load Background', self)
        self.load_background_action.setShortcut('Ctrl+L')
        self.load_background_action.setStatusTip('Load Background')
        self.load_background_action.triggered.connect(self.trigger_load_background)
        self.tracking_options_menu.addAction(self.load_background_action)

        self.calculate_background_action = QAction('&Calculate Background', self)
        self.calculate_background_action.setShortcut('Ctrl+B')
        self.calculate_background_action.setStatusTip('Calculate Background')
        self.calculate_background_action.triggered.connect(self.trigger_calculate_background)
        self.tracking_options_menu.addAction(self.calculate_background_action)

        self.save_background_action = QAction('&Save Background', self)
        self.save_background_action.setShortcut('Ctrl+S')
        self.save_background_action.setStatusTip('Save Background')
        self.save_background_action.triggered.connect(self.trigger_save_background)
        self.tracking_options_menu.addAction(self.save_background_action)

        self.unload_all_tracking_action = QAction('&Unload All Tracking', self)
        self.unload_all_tracking_action.setShortcut('Ctrl+U')
        self.unload_all_tracking_action.setStatusTip('Unload All Tracking From Memory')
        self.unload_all_tracking_action.triggered.connect(self.trigger_unload_all_tracking)
        self.tracking_options_menu.addAction(self.unload_all_tracking_action)
    def add_plotting_options_to_menubar(self):
        self.plotting_options_menu = self.menubar.addMenu('&Plotting Options')

        self.load_tracking_results_action = QAction('&Load Tracking Results')
        self.load_tracking_results_action.setStatusTip('Load Tracking Results')
        self.load_tracking_results_action.triggered.connect(self.trigger_load_tracking_results)
        self.plotting_options_menu.addAction(self.load_tracking_results_action)

        self.open_tracked_video_action = QAction('&Open Tracked Video', self)
        self.open_tracked_video_action.setShortcut('Ctrl+T')
        self.open_tracked_video_action.setStatusTip('Open Tracked Video')
        self.open_tracked_video_action.triggered.connect(self.trigger_open_tracked_video)
        self.plotting_options_menu.addAction(self.open_tracked_video_action)

        self.unload_all_plotting_action = QAction('&Unload All Plotting', self)
        self.unload_all_plotting_action.setStatusTip('Unload All Plotting')
        self.unload_all_plotting_action.triggered.connect(self.trigger_unload_all_plotting)
        self.plotting_options_menu.addAction(self.unload_all_plotting_action)

    def trigger_save_background(self):
        self.main_tab.tracking_window.tracking_content.trigger_save_background()
    def trigger_calculate_background(self):
        self.main_tab.tracking_window.tracking_content.trigger_calculate_background()
    def trigger_select_save_path(self):
        self.main_tab.tracking_window.tracking_content.trigger_select_save_path()
    def trigger_load_background(self):
        self.main_tab.tracking_window.tracking_content.trigger_load_background()
    def trigger_open_video(self):
        self.main_tab.tracking_window.tracking_content.trigger_open_video()
    def trigger_open_tracked_video(self):
        self.main_tab.plotting_window.plotting_content.trigger_open_tracked_video()
    def trigger_unload_all_tracking(self):
        self.main_tab.tracking_window.tracking_content.trigger_unload_all_tracking()
    def trigger_load_tracking_results(self):
        self.main_tab.plotting_window.plotting_content.trigger_load_tracking_results()
    def trigger_unload_all_plotting(self):
        self.main_tab.plotting_window.plotting_content.trigger_unload_all_plotting()

    # Defining Event Functions
    def closeEvent(self, event):
        event.accept()

class MainTab(QTabWidget):

    def __init__(self):
        super(MainTab, self).__init__()
        self.tracking_window = TrackingWindow()
        self.addTab(self.tracking_window,"Tracking")
        self.plotting_window = PlottingWindow()
        self.addTab(self.plotting_window, "Plotting")

class TrackingWindow(QScrollArea):

    def __init__(self):
        super(TrackingWindow, self).__init__()
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
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
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
        self.background_path = None
        self.background_path_basename = None
        self.background_path_folder = None
        self.save_path = None
        self.preview_background = False
        self.preview_background_subtracted_frame = False
        self.preview_tracking_results = False
        self.preview_eyes_threshold = False
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
        self.eyes_threshold = 0
        self.eyes_line_length = 0
        self.preview_frame = None
        self.colours = []
        self.save_video = False
        self.extended_eyes_calculation = False

    # Defining Get Functions
    def get_main_window_attributes(self):
        self.main_window_width = QDesktopWidget().availableGeometry().width()
        self.main_window_height = QDesktopWidget().availableGeometry().height()
    def get_video_attributes(self):
        self.video_path_folder = os.path.dirname(self.video_path)
        self.video_path_basename = os.path.basename(self.video_path)
        self.video_n_frames = ut.get_total_frame_number_from_video(self.video_path)
        self.video_fps = ut.get_fps_from_video(self.video_path)
        self.video_format = ut.get_video_format_from_video(self.video_path)
        self.video_frame_width, self.video_frame_height = ut.get_frame_size_from_video(self.video_path)
    def get_background_attributes(self):
        self.background_path_folder = os.path.dirname(self.background_path)
        self.background_path_basename = os.path.basename(self.background_path)
        self.background_height, self.background_width = self.background.shape

    # Defining Add Functions
    # def add_options_to_menubar(self):
        # self.options_menu = self.menubar.addMenu('&Options')
        #
        # self.open_video_action = QAction('&Open Video', self)
        # self.open_video_action.setShortcut('Ctrl+O')
        # self.open_video_action.setStatusTip('Open Video')
        # self.open_video_action.triggered.connect(self.trigger_open_video)
        # self.options_menu.addAction(self.open_video_action)
        #
        # self.select_save_path_action = QAction('&Select Save Path', self)
        # self.select_save_path_action.setShortcut('Ctrl+P')
        # self.select_save_path_action.setStatusTip('Select Save Path')
        # self.select_save_path_action.triggered.connect(self.trigger_select_save_path)
        # self.options_menu.addAction(self.select_save_path_action)
        #
        # self.load_background_action = QAction('&Load Background', self)
        # self.load_background_action.setShortcut('Ctrl+L')
        # self.load_background_action.setStatusTip('Load Background')
        # self.load_background_action.triggered.connect(self.trigger_load_background)
        # self.options_menu.addAction(self.load_background_action)
        #
        # self.calculate_background_action = QAction('&Calculate Background', self)
        # self.calculate_background_action.setShortcut('Ctrl+B')
        # self.calculate_background_action.setStatusTip('Calculate Background')
        # self.calculate_background_action.triggered.connect(self.trigger_calculate_background)
        # self.options_menu.addAction(self.calculate_background_action)
        #
        # self.save_background_action = QAction('&Save Background', self)
        # self.save_background_action.setShortcut('Ctrl+S')
        # self.save_background_action.setStatusTip('Save Background')
        # self.save_background_action.triggered.connect(self.trigger_save_background)
        # self.options_menu.addAction(self.save_background_action)
        #
        # self.unload_all_action = QAction('&Unload All', self)
        # self.unload_all_action.setShortcut('Ctrl+U')
        # self.unload_all_action.setStatusTip('Unload All Things From Memory')
        # self.unload_all_action.triggered.connect(self.trigger_unload_all)
        # self.options_menu.addAction(self.unload_all_action)
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
        self.preview_frame_number_textbox_label.resize(145, 25)
        self.preview_frame_number_textbox_label.setText('Frame Number: ')
        self.preview_frame_number_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.preview_frame_number_textbox_label.setFont(font)
        self.preview_frame_number_textbox = QLineEdit(self)
        self.preview_frame_number_textbox.move(150, 1060)
        self.preview_frame_number_textbox.resize(100, 25)
        self.preview_frame_number_textbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
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

        # self.preview_extended_eyes_calculation_checkbox = QCheckBox(self)
        # self.preview_extended_eyes_calculation_checkbox.move(1025, 1230)
        # self.preview_extended_eyes_calculation_checkbox.stateChanged.connect(self.check_preview_extended_eyes_calculation_checkbox)
        # self.preview_extended_eyes_calculation_checkbox.setEnabled(False)
        # self.preview_extended_eyes_calculation_checkbox_label = QLabel(self)
        # self.preview_extended_eyes_calculation_checkbox_label.move(1045, 1233)
        # self.preview_extended_eyes_calculation_checkbox_label.resize(500, 20)
        # self.preview_extended_eyes_calculation_checkbox_label.setText('Preview Extended Eyes Calculation')
        # self.preview_extended_eyes_calculation_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        # self.preview_extended_eyes_calculation_checkbox_label.setFont(font)

        self.preview_eyes_threshold_checkbox = QCheckBox(self)
        self.preview_eyes_threshold_checkbox.move(1025, 1230)
        self.preview_eyes_threshold_checkbox.stateChanged.connect(self.check_preview_eyes_threshold_checkbox)
        self.preview_eyes_threshold_checkbox.setEnabled(False)
        self.preview_eyes_threshold_checkbox_label = QLabel(self)
        self.preview_eyes_threshold_checkbox_label.move(1045, 1233)
        self.preview_eyes_threshold_checkbox_label.resize(500, 20)
        self.preview_eyes_threshold_checkbox_label.setText('Preview Eyes Threshold')
        self.preview_eyes_threshold_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_eyes_threshold_checkbox_label.setFont(font)
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
        self.tracking_n_tail_points_textbox.returnPressed.connect(self.check_tracking_n_tail_points_textbox)

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

        self.eyes_threshold_textbox_label = QLabel(self)
        self.eyes_threshold_textbox_label.move(1500, 500)
        self.eyes_threshold_textbox_label.resize(500, 20)
        self.eyes_threshold_textbox_label.setText('Eyes Threshold: ')
        self.eyes_threshold_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.eyes_threshold_textbox_label.setFont(font)
        self.eyes_threshold_textbox = QLineEdit(self)
        self.eyes_threshold_textbox.move(2000, 500)
        self.eyes_threshold_textbox.resize(80, 20)
        self.eyes_threshold_textbox.setText('{0}'.format(self.eyes_threshold))
        self.eyes_threshold_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.eyes_threshold_textbox.setFont(font)
        self.eyes_threshold_textbox.returnPressed.connect(self.check_eyes_threshold_textbox)

        self.eyes_line_length_textbox_label = QLabel(self)
        self.eyes_line_length_textbox_label.move(1500, 540)
        self.eyes_line_length_textbox_label.resize(500, 20)
        self.eyes_line_length_textbox_label.setText('Eyes Line Length: ')
        self.eyes_line_length_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.eyes_line_length_textbox_label.setFont(font)
        self.eyes_line_length_textbox = QLineEdit(self)
        self.eyes_line_length_textbox.move(2000, 540)
        self.eyes_line_length_textbox.resize(80, 20)
        self.eyes_line_length_textbox.setText('{0}'.format(self.eyes_threshold))
        self.eyes_line_length_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.eyes_line_length_textbox.setFont(font)
        self.eyes_line_length_textbox.returnPressed.connect(self.check_eyes_line_length_textbox)

        self.save_tracked_video_combobox_label = QLabel(self)
        self.save_tracked_video_combobox_label.move(1500, 580)
        self.save_tracked_video_combobox_label.resize(500, 20)
        self.save_tracked_video_combobox_label.setText('Save Tracked Video: ')
        self.save_tracked_video_combobox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.save_tracked_video_combobox_label.setFont(font)
        self.save_tracked_video_combobox = QComboBox(self)
        self.save_tracked_video_combobox.addItem('True')
        self.save_tracked_video_combobox.addItem('False')
        self.save_tracked_video_combobox.move(2000, 580)
        self.save_tracked_video_combobox.resize(80, 20)
        self.save_tracked_video_combobox.setCurrentIndex(1)
        self.save_tracked_video_combobox.currentIndexChanged.connect(self.check_save_tracked_video_combobox)

        self.extended_eyes_calculation_combobox_label = QLabel(self)
        self.extended_eyes_calculation_combobox_label.move(1500, 620)
        self.extended_eyes_calculation_combobox_label.resize(500, 20)
        self.extended_eyes_calculation_combobox_label.setText('Extended Eyes Calculation: ')
        self.extended_eyes_calculation_combobox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.extended_eyes_calculation_combobox_label.setFont(font)
        self.extended_eyes_calculation_combobox = QComboBox(self)
        self.extended_eyes_calculation_combobox.addItem('True')
        self.extended_eyes_calculation_combobox.addItem('False')
        self.extended_eyes_calculation_combobox.move(2000, 620)
        self.extended_eyes_calculation_combobox.resize(80, 20)
        self.extended_eyes_calculation_combobox.setCurrentIndex(1)
        self.extended_eyes_calculation_combobox.currentIndexChanged.connect(self.check_extended_eyes_calculation_combobox)

        self.trigger_load_default_tracking_parameters()
        self.trigger_load_default_colours()
        self.update_tracking_parameters(inactivate = True)
    def add_tracking_parameters_buttons(self):
        font = QFont()
        font.setPointSize(10)
        self.load_default_tracking_parameters_button = QPushButton('Load Default Tracking Parameters', self)
        self.load_default_tracking_parameters_button.move(1800, 660)
        self.load_default_tracking_parameters_button.resize(400, 80)
        self.load_default_tracking_parameters_button.setFont(font)
        self.load_default_tracking_parameters_button.clicked.connect(self.check_load_default_tracking_parameters_button)

        self.load_previous_tracking_parameters_button = QPushButton('Load Previous Tracking Parameters', self)
        self.load_previous_tracking_parameters_button.move(1800, 750)
        self.load_previous_tracking_parameters_button.resize(400, 80)
        self.load_previous_tracking_parameters_button.setFont(font)
        self.load_previous_tracking_parameters_button.clicked.connect(self.trigger_load_previous_tracking_parameters)

        self.save_current_tracking_parameters_button = QPushButton('Save Current Tracking Parameters', self)
        self.save_current_tracking_parameters_button.move(1800, 840)
        self.save_current_tracking_parameters_button.resize(400, 80)
        self.save_current_tracking_parameters_button.setFont(font)
        self.save_current_tracking_parameters_button.clicked.connect(self.trigger_save_current_tracking_parameters)

        self.track_video_button = QPushButton('Track Video', self)
        self.track_video_button.move(1800, 930)
        self.track_video_button.resize(400, 80)
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
        for i in range(len(self.colours)):
            count = int(i / 6)
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

        self.load_previous_colours_button = QPushButton('Load Previous Colours', self)
        self.load_previous_colours_button.move(2395, 1150)
        self.load_previous_colours_button.resize(150, 40)
        self.load_previous_colours_button.clicked.connect(self.trigger_load_previous_colours)

        self.save_current_colours_button = QPushButton('Save Current Colours', self)
        self.save_current_colours_button.move(2395, 1200)
        self.save_current_colours_button.resize(150, 40)
        self.save_current_colours_button.clicked.connect(self.trigger_save_current_colours)
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
    def update_preview_frame(self, frame, frame_width, frame_height, grayscale = True):
        if grayscale:
            format = QImage.Format_Indexed8
        else:
            format = QImage.Format_RGB888
        self.preview_frame = QImage(frame.data, frame_width, frame_height, format)
        if frame_height > 1000 and frame_height > frame_width:
           self.preview_frame = self.preview_frame.scaledToHeight(1000)
        elif frame_width > 1000:
           self.preview_frame = self.preview_frame.scaledToWidth(1000)
        elif frame_height > frame_width:
           self.preview_frame = self.preview_frame.scaledToHeight(1000)
        else:
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
            if not self.preview_eyes_threshold_checkbox.isEnabled():
                self.preview_eyes_threshold_checkbox.setEnabled(True)
        if inactivate:
            if self.preview_background_checkbox.isEnabled():
                self.preview_background_checkbox.setEnabled(False)
            if self.preview_background_subtracted_frame_checkbox.isEnabled():
                self.preview_background_subtracted_frame_checkbox.setEnabled(False)
            if self.preview_tracking_results_checkbox.isEnabled():
                self.preview_tracking_results_checkbox.setEnabled(False)
            if self.preview_eyes_threshold_checkbox.isEnabled():
                self.preview_eyes_threshold_checkbox.setEnabled(False)
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
            if not self.eyes_threshold_textbox.isEnabled():
                self.eyes_threshold_textbox.setEnabled(True)
            if not self.eyes_line_length_textbox.isEnabled():
                self.eyes_line_length_textbox.setEnabled(True)
            if not self.save_tracked_video_combobox.isEnabled():
                self.save_tracked_video_combobox.setEnabled(True)
            if not self.extended_eyes_calculation_combobox.isEnabled():
                self.extended_eyes_calculation_combobox.setEnabled(True)
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
            if self.eyes_threshold_textbox.isEnabled():
                self.eyes_threshold_textbox.setEnabled(False)
            if self.eyes_line_length_textbox.isEnabled():
                self.eyes_line_length_textbox.setEnabled(False)
            if self.save_tracked_video_combobox.isEnabled():
                self.save_tracked_video_combobox.setEnabled(False)
            if self.extended_eyes_calculation_combobox.isEnabled():
                self.extended_eyes_calculation_combobox.setEnabled(False)
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
        if self.eyes_threshold_textbox.isEnabled():
            self.eyes_threshold_textbox.setText('{0}'.format(self.eyes_threshold))
        if self.eyes_line_length_textbox.isEnabled():
            self.eyes_line_length_textbox.setText('{0}'.format(self.eyes_line_length))
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
            if not self.load_previous_colours_button.isEnabled():
                self.load_previous_colours_button.setEnabled(True)
            if not self.save_current_colours_button.isEnabled():
                self.save_current_colours_button.setEnabled(True)
        if inactivate:
            if self.load_default_colours_button.isEnabled():
                self.load_default_colours_button.setEnabled(False)
            if self.load_previous_colours_button.isEnabled():
                self.load_previous_colours_button.setEnabled(False)
            if self.save_current_colours_button.isEnabled():
                self.save_current_colours_button.setEnabled(False)
    def update_colours(self):
        if self.n_tail_points < len(self.colours) - 3 and len(self.colours) == len(self.colour_label_list):
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
        elif self.n_tail_points > len(self.colours) - 3 and len(self.colours) == len(self.colour_label_list):
            font = QFont()
            font.setPointSize(10)
            for i in range(self.n_tail_points + 3 - len(self.colours)):
                self.colours.insert(i + self.n_tail_points - 1, (0, 0, 0))
                count = int((len(self.colours) - 1) / 6)
                colour_label_pos = [1565 + count * 250, 1100 + ((len(self.colours) - 1) * 45) - (count * 270)]
                colour_label = QLabel(self)
                colour_label.move(colour_label_pos[0], colour_label_pos[1])
                colour_label.resize(100, 20)
                colour_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                colour_label.setFont(font)
                colour_label.show()
                self.colour_label_list.append(colour_label)
                colour_textbox_pos = [1665 + count * 250, 1100 + ((len(self.colours) - 1) * 45) - (count * 270)]
                colour_textbox = QLineEdit(self)
                colour_textbox.move(colour_textbox_pos[0], colour_textbox_pos[1])
                colour_textbox.resize(120, 20)
                colour_textbox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                colour_textbox.setFont(font)
                colour_textbox.setEnabled(False)
                colour_textbox.show()
                self.colour_textbox_list.append(colour_textbox)
                colour_button_pos = [1795 + count * 250, 1100 + ((len(self.colours) - 1) * 45) - (count * 270)]
                colour_button = QPushButton(self)
                colour_button.setIcon(QIcon('colour_wheel.jpg'))
                colour_button.setIconSize(QSize(18, 18))
                colour_button.move(colour_button_pos[0], colour_button_pos[1])
                colour_button.resize(20, 20)
                colour_button.clicked.connect(partial(self.trigger_update_single_colour, len(self.colours) - 1))
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
                ut.save_background_to_file(self.background, self.background_path)
                self.get_background_attributes()
                self.update_descriptors()
        else:
            self.save_path = self.video_path_folder
            self.background_path = '{0}/{1}_background.tif'.format(self.save_path, self.video_path_basename[:-4])
            ut.save_background_to_file(self.background, self.background_path)
            self.get_background_attributes()
            self.update_descriptors()
    def trigger_calculate_background(self):
        if self.video_path is not None:
            self.background_path = 'Background calculated and loaded into memory/Background calculated and loaded into memory'
            self.background = ut.calculate_background(self.video_path)[0]
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
            self.background = ut.load_background_into_memory(self.background_path)
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
        self.video_path, _ = QFileDialog.getOpenFileName(self,"Open Video File", "","Video Files (*.avi; *.mp4)", options=QFileDialog.Options())
        if self.video_path:
            self.get_video_attributes()
            self.update_descriptors()
            success, self.frame = ut.load_frame_into_memory(self.video_path, self.frame_number - 1)
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
        elif self.preview_eyes_threshold:
            if self.video_path is not None:
                success, self.frame = ut.load_frame_into_memory(self.video_path, self.frame_number - 1)
                if success and self.frame is not None:
                    use_grayscale = True
                    self.frame = ut.apply_threshold_to_frame(ut.apply_median_blur_to_frame(ut.subtract_background_from_frame(self.frame, self.background)), self.eyes_threshold)
                    self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height, grayscale = use_grayscale)
                    self.update_preview_frame_window()
                    self.update_frame_window_slider(activate = True)
                    self.update_preview_frame_number_textbox(activate = True)
                    self.update_update_preview_button(activate = True)
                    self.update_frame_change_buttons(activate = True)
        else:
            if self.video_path is not None:
                success, self.frame = ut.load_frame_into_memory(self.video_path, self.frame_number - 1)
                if success and self.frame is not None:
                    use_grayscale = True
                    if self.preview_background_subtracted_frame:
                        self.frame = ut.subtract_background_from_frame(self.frame, self.background)
                        if self.preview_tracking_results:
                            results = ut.track_tail_in_frame([ut.apply_median_blur_to_frame(self.frame), success, self.n_tail_points, self.dist_tail_points, self.dist_eyes, self.dist_swim_bladder, self.pixel_threshold, self.extended_eyes_calculation, self.eyes_threshold])
                            if results is not None:
                                self.frame = ut.annotate_tracking_results_onto_frame(self.frame, results, self.colours, self.line_length, self.extended_eyes_calculation, self.eyes_line_length)
                                use_grayscale = False
                    elif self.preview_tracking_results:
                        results = ut.track_tail_in_frame([ut.apply_median_blur_to_frame(ut.subtract_background_from_frame(self.frame, self.background)), success, self.n_tail_points, self.dist_tail_points, self.dist_eyes, self.dist_swim_bladder, self.pixel_threshold, self.extended_eyes_calculation, self.eyes_threshold])
                        if results is not None:
                            self.frame = ut.annotate_tracking_results_onto_frame(self.frame, results, self.colours, self.line_length, self.extended_eyes_calculation, self.eyes_line_length)
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
        self.eyes_threshold = 100
        self.eyes_line_length = 5
        self.save_video = False
        self.save_tracked_video_combobox.setCurrentIndex(1)
        self.extended_eyes_calculation = False
        self.extended_eyes_calculation_combobox.setCurrentIndex(1)
        self.update_tracking_parameters()
        if self.preview_frame:
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
            self.eyes_threshold = tracking_parameters['eyes_threshold']
            self.eyes_line_length = tracking_parameters['eyes_line_length']
            self.save_video = tracking_parameters['save_video']
            self.extended_eyes_calculation = tracking_parameters['extended_eyes_calculation']
            self.update_colours()
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
            'pixel_threshold' : self.pixel_threshold, 'frame_change_threshold' : self.frame_change_threshold,
            'eyes_threshold' : self.eyes_threshold, 'eyes_line_length' : self.eyes_line_length,
            'save_video' : self.save_video, 'extended_eyes_calculation' : self.extended_eyes_calculation}
        np.save('tracking_parameters.npy', tracking_parameters)
    def trigger_track_video(self):
        self.track_video_thread = TrackVideoThread()
        self.track_video_thread.video_path = self.video_path
        self.track_video_thread.n_tail_points = self.n_tail_points
        self.track_video_thread.dist_tail_points = self.dist_tail_points
        self.track_video_thread.dist_eyes = self.dist_eyes
        self.track_video_thread.dist_swim_bladder = self.dist_swim_bladder
        self.track_video_thread.n_frames = self.n_frames
        self.track_video_thread.starting_frame = self.starting_frame
        self.track_video_thread.save_path = self.save_path
        self.track_video_thread.background_path = self.background_path
        self.track_video_thread.line_length = self.line_length
        self.track_video_thread.video_fps = self.video_fps
        self.track_video_thread.pixel_threshold = self.pixel_threshold
        self.track_video_thread.frame_change_threshold = self.frame_change_threshold
        self.track_video_thread.colours = [(self.colours[i][2], self.colours[i][1], self.colours[i][0]) for i in range(len(self.colours))]
        self.track_video_thread.save_video = self.save_video
        self.track_video_thread.extended_eyes_calculation = self.extended_eyes_calculation
        self.track_video_thread.eyes_threshold = self.eyes_threshold
        self.track_video_thread.start()
    def trigger_unload_all_tracking(self):
        if self.preview_background_checkbox.isChecked():
            self.preview_background_checkbox.setChecked(False)
        if self.preview_background_subtracted_frame_checkbox.isChecked():
            self.preview_background_subtracted_frame_checkbox.setChecked(False)
        if self.preview_tracking_results_checkbox.isChecked():
            self.preview_tracking_results_checkbox.setChecked(False)
        if self.save_tracked_video_combobox.currentIndex() == 0:
            self.save_tracked_video_combobox.setCurrentIndex(1)
        if self.extended_eyes_calculation_combobox.currentIndex() == 0:
            self.extended_eyes_calculation_combobox.setCurrentIndex(1)
        for i in range(len(self.colours)):
            self.colour_label_list[-1].deleteLater()
            self.colour_textbox_list[-1].deleteLater()
            self.colour_button_list[-1].deleteLater()
            del(self.colour_label_list[-1])
            del(self.colour_textbox_list[-1])
            del(self.colour_button_list[-1])
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
        self.update_colours()
        self.trigger_load_default_colours()
        self.update_colours()
    def trigger_update_single_colour(self, id):
        colour = QColorDialog.getColor().getRgb()[0:3]
        colour = (colour[0], colour[1], colour[2])
        self.colours[id] = colour
        self.colour_textbox_list[id].setText('{0}'.format(colour))
        self.trigger_update_preview()
    def trigger_load_default_colours(self):
        self.colours = [[] for i in range(self.n_tail_points + 3)]
        colour_map = cm.gnuplot2
        self.colours[-1] = (0, 255, 255)
        self.colours[-2] = (255, 0, 127)
        self.colours[-3] = (0, 255, 0)
        for i in range(self.n_tail_points):
            colour = colour_map(i / (self.n_tail_points - 1))[:3]
            self.colours[i] = (int(colour[0] * 255), int(colour[1] * 255), int(colour[2] * 255))
    def trigger_load_previous_colours(self):
        try:
            colours = np.load('colours.npy').item()
            self.colours = colours['colours']
            self.update_colours()
            if self.preview_frame:
                self.trigger_update_preview()
        except:
            print('Error: colour parameters not found.')
            self.trigger_load_default_colours()
            self.update_colours()
            if self.preview_frame:
                self.trigger_update_preview()
    def trigger_save_current_colours(self):
        colours = {'colours' : self.colours}
        np.save('colours.npy', colours)

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
    def check_preview_eyes_threshold_checkbox(self):
        self.preview_eyes_threshold = self.preview_eyes_threshold_checkbox.isChecked()
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
            if int(self.tracking_n_tail_points_textbox.text()) > 0 and int(self.tracking_n_tail_points_textbox.text()) < 15:
                self.n_tail_points = int(self.tracking_n_tail_points_textbox.text())
            elif int(self.tracking_n_tail_points_textbox.text()) >= 15:
                self.n_tail_points = 15
                self.tracking_n_tail_points_textbox.setText('15')
            if self.n_tail_points != len(self.colours) - 3:
                self.update_colours()
            self.trigger_update_preview()
        else:
            self.tracking_n_tail_points_textbox.setText(str(self.n_tail_points))
    def check_tracking_dist_tail_points_textbox(self):
        if self.tracking_dist_tail_points_textbox.text().isdigit():
            self.dist_tail_points = int(self.tracking_dist_tail_points_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_dist_tail_points_textbox.setText(str(self.dist_tail_points))
    def check_tracking_dist_eyes_textbox(self):
        if self.tracking_dist_eyes_textbox.text().isdigit():
            self.dist_eyes = int(self.tracking_dist_eyes_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_dist_eyes_textbox.setText(str(self.dist_eyes))
    def check_tracking_dist_swim_bladder_textbox(self):
        if self.tracking_dist_swim_bladder_textbox.text().isdigit():
            self.dist_swim_bladder = int(self.tracking_dist_swim_bladder_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_dist_swim_bladder_textbox.setText(str(self.dist_swim_bladder))
    def check_tracking_frame_batch_size_textbox(self):
        if self.tracking_frame_batch_size_textbox.text().isdigit():
            self.frame_batch_size = int(self.tracking_frame_batch_size_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_frame_batch_size_textbox.setText(str(self.frame_batch_size))
    def check_tracking_starting_frame_textbox(self):
        if self.tracking_starting_frame_textbox.text().isdigit():
            self.starting_frame = int(self.tracking_starting_frame_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_starting_frame_textbox.setText(str(self.starting_frame))
    def check_tracking_n_frames_textbox(self):
        if self.tracking_n_frames_textbox.text().isdigit():
            self.n_frames = int(self.tracking_n_frames_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_n_frames_textbox.setText(str(self.n_frames))
    def check_tracking_line_length_textbox(self):
        if self.tracking_line_length_textbox.text().isdigit():
            self.line_length = int(self.tracking_line_length_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_line_length_textbox.setText(str(self.line_length))
    def check_tracking_pixel_threshold_textbox(self):
        if self.tracking_pixel_threshold_textbox.text().isdigit():
            self.pixel_threshold = int(self.tracking_pixel_threshold_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_pixel_threshold_textbox.setText(str(self.pixel_threshold))
    def check_tracking_frame_change_threshold_textbox(self):
        if self.tracking_frame_change_threshold_textbox.text().isdigit():
            self.frame_change_threshold = int(self.tracking_frame_change_threshold_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.tracking_frame_change_threshold_textbox.setText(str(self.frame_change_threshold))
    def check_eyes_threshold_textbox(self):
        if self.eyes_threshold_textbox.text().isdigit():
            if int(self.eyes_threshold_textbox.text()) > 0 and int(self.eyes_threshold_textbox.text()) <= 255:
                self.eyes_threshold = int(self.eyes_threshold_textbox.text())
            elif int(self.eyes_threshold_textbox.text()) > 255:
                self.eyes_threshold = 255
                self.eyes_threshold_textbox.setText('255')
            if self.preview_tracking_results or self.preview_eyes_threshold:
                self.trigger_update_preview()
        else:
            self.eyes_threshold_textbox.setText(str(self.frame_change_threshold))
    def check_eyes_line_length_textbox(self):
        if self.eyes_line_length_textbox.text().isdigit():
            self.eyes_line_length = int(self.eyes_line_length_textbox.text())
            if self.preview_tracking_results:
                self.trigger_update_preview()
        else:
            self.eyes_line_length_textbox.setText(str(self.eyes_line_length))
    def check_load_default_tracking_parameters_button(self):
        self.trigger_load_default_tracking_parameters()
        self.update_colours()
    def check_load_default_colours_button(self):
        self.trigger_load_default_colours()
        self.update_colours()
        self.trigger_update_preview()
    def check_save_tracked_video_combobox(self):
        current_index = self.save_tracked_video_combobox.currentIndex()
        if current_index == 0:
            self.save_video = True
        if current_index == 1:
            self.save_video = False
    def check_extended_eyes_calculation_combobox(self):
        current_index = self.extended_eyes_calculation_combobox.currentIndex()
        if current_index == 0:
            self.extended_eyes_calculation = True
        if current_index == 1:
            self.extended_eyes_calculation = False
        if self.preview_tracking_results:
            self.trigger_update_preview()

class TrackVideoThread(QThread):

    def __init__(self):
        super(TrackVideoThread, self).__init__()
        self.video_path = None
        self.colours = None
        self.n_tail_points = None
        self.dist_tail_points = None
        self.dist_eyes = None
        self.dist_swim_bladder = None
        self.n_frames = None
        self.starting_frame = None
        self.save_path = None
        self.background_path = None
        self.line_length = None
        self.video_fps = None
        self.pixel_threshold = None
        self.frame_change_threshold = None
        self.save_video = None
        self.extended_eyes_calculation = None
        self.eyes_threshold = None

    def run(self):
        if self.background_path == 'Background calculated and loaded into memory/Background calculated and loaded into memory':
            self.background_path = None
        ut.track_video(self.video_path, self.colours, self.n_tail_points, self.dist_tail_points, self.dist_eyes, self.dist_swim_bladder, save_video = self.save_video, extended_eyes_calculation = self.extended_eyes_calculation, n_frames = self.n_frames, starting_frame = self.starting_frame, save_path = self.save_path, background_path = self.background_path, line_length = self.line_length, video_fps = self.video_fps, pixel_threshold = self.pixel_threshold, frame_change_threshold = self.frame_change_threshold, eyes_threshold = self.eyes_threshold)
        # ut.track_tail_in_video_without_multiprocessing(self.video_path, self.colours, self.n_tail_points, self.dist_tail_points, self.dist_eyes, self.dist_swim_bladder, init_frame_batch_size = 50, init_starting_frame = 0, save_path = self.save_path, background_path = self.background_path, line_length = self.line_length, video_fps = self.video_fps, n_frames = self.n_frames, pixel_threshold = self.pixel_threshold, frame_change_threshold = self.frame_change_threshold)

class PlottingWindow(QScrollArea):

    def __init__(self):
        super(PlottingWindow, self).__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.plotting_content = PlottingContent()
        self.setWidget(self.plotting_content)

class PlottingContent(QMainWindow):

    # Defining Initialization Functions
    def __init__(self):
        super(PlottingContent, self).__init__()
        self.initUI()
    def initUI(self):
        self.initialize_class_variables()
        self.add_tracking_preview_frame_window()
        self.add_frame_window_slider()
        self.add_tracking_video_time_textbox()
        self.add_update_preview_button()
        self.add_frame_change_buttons()
        self.add_video_playback_buttons()
        self.add_data_plot_window()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.resize(2560, 1400)
    def initialize_class_variables(self):
        self.frame_number = 1
        self.video_path = None
        self.play_video_slow_speed = False
        self.play_video_medium_speed = False
        self.play_video_max_speed = False

    def get_video_attributes(self):
        self.video_path_folder = os.path.dirname(self.video_path)
        self.video_path_basename = os.path.basename(self.video_path)
        self.video_n_frames = ut.get_total_frame_number_from_video(self.video_path)
        self.video_fps = ut.get_fps_from_video(self.video_path)
        self.video_format = ut.get_video_format_from_video(self.video_path)
        self.video_frame_width, self.video_frame_height = ut.get_frame_size_from_video(self.video_path)

    def add_tracking_preview_frame_window(self):
        font = QFont()
        font.setPointSize(18)
        self.preview_frame_window = QLabel(self)
        self.preview_frame_window.setFrameShape(QFrame.Panel)
        self.preview_frame_window.setFrameShadow(QFrame.Sunken)
        self.preview_frame_window.setLineWidth(5)
        self.preview_frame_window.move(5, 25)
        self.preview_frame_window.resize(1000, 1000)
        self.preview_frame_window.setText('Tracked Frame Window')
        self.preview_frame_window.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.preview_frame_window.setFont(font)
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
    def add_tracking_video_time_textbox(self):
        font = QFont()
        font.setPointSize(10)
        self.tracking_video_time_textbox_label = QLabel(self)
        self.tracking_video_time_textbox_label.move(5, 1060)
        self.tracking_video_time_textbox_label.resize(145, 25)
        self.tracking_video_time_textbox_label.setText('Time (seconds): ')
        self.tracking_video_time_textbox_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tracking_video_time_textbox_label.setFont(font)
        self.tracking_video_time_textbox = QLineEdit(self)
        self.tracking_video_time_textbox.move(150, 1060)
        self.tracking_video_time_textbox.resize(100, 25)
        self.tracking_video_time_textbox.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tracking_video_time_textbox.setFont(font)
        self.tracking_video_time_textbox.returnPressed.connect(self.check_tracking_video_time_textbox)
        self.update_tracking_video_time_textbox(inactivate = True)
    def add_update_preview_button(self):
        font = QFont()
        font.setPointSize(10)
        self.update_preview_button = QPushButton('Update Preview', self)
        self.update_preview_button.move(5, 1090)
        self.update_preview_button.resize(245, 50)
        self.update_preview_button.setFont(font)
        self.update_preview_button.clicked.connect(self.check_tracking_video_time_textbox)
        self.update_update_preview_button(inactivate = True)
    def add_frame_change_buttons(self):
        self.large_frame_decrease_button = QPushButton(self)
        self.large_frame_decrease_button.setIcon(QIcon('button_icon_1.png'))
        self.large_frame_decrease_button.setIconSize(QSize(46, 46))
        self.large_frame_decrease_button.move(635, 1060)
        self.large_frame_decrease_button.resize(50, 50)
        self.large_frame_decrease_button.clicked.connect(self.check_large_frame_decrease_button)

        self.medium_frame_decrease_button = QPushButton(self)
        self.medium_frame_decrease_button.setIcon(QIcon('button_icon_2.png'))
        self.medium_frame_decrease_button.setIconSize(QSize(46, 46))
        self.medium_frame_decrease_button.move(690, 1060)
        self.medium_frame_decrease_button.resize(50, 50)
        self.medium_frame_decrease_button.clicked.connect(self.check_medium_frame_decrease_button)

        self.small_frame_decrease_button = QPushButton(self)
        self.small_frame_decrease_button.setIcon(QIcon('button_icon_3.png'))
        self.small_frame_decrease_button.setIconSize(QSize(46, 46))
        self.small_frame_decrease_button.move(745, 1060)
        self.small_frame_decrease_button.resize(50, 50)
        self.small_frame_decrease_button.clicked.connect(self.check_small_frame_decrease_button)

        self.small_frame_increase_button = QPushButton(self)
        self.small_frame_increase_button.setIcon(QIcon('button_icon_4.png'))
        self.small_frame_increase_button.setIconSize(QSize(46, 46))
        self.small_frame_increase_button.move(800, 1060)
        self.small_frame_increase_button.resize(50, 50)
        self.small_frame_increase_button.clicked.connect(self.check_small_frame_increase_button)

        self.medium_frame_increase_button = QPushButton(self)
        self.medium_frame_increase_button.setIcon(QIcon('button_icon_5.png'))
        self.medium_frame_increase_button.setIconSize(QSize(46, 46))
        self.medium_frame_increase_button.move(855, 1060)
        self.medium_frame_increase_button.resize(50, 50)
        self.medium_frame_increase_button.clicked.connect(self.check_medium_frame_increase_button)

        self.large_frame_increase_button = QPushButton(self)
        self.large_frame_increase_button.setIcon(QIcon('button_icon_6.png'))
        self.large_frame_increase_button.setIconSize(QSize(46, 46))
        self.large_frame_increase_button.move(910, 1060)
        self.large_frame_increase_button.resize(50, 50)
        self.large_frame_increase_button.clicked.connect(self.check_large_frame_increase_button)
        self.update_frame_change_buttons(inactivate = True)
    def add_video_playback_buttons(self):
        self.pause_video_button = QPushButton(self)
        self.pause_video_button.setIcon(QIcon('button_icon_7.png'))
        self.pause_video_button.setIconSize(QSize(76, 76))
        self.pause_video_button.move(275, 1060)
        self.pause_video_button.resize(80, 80)
        self.pause_video_button.clicked.connect(self.check_pause_video_button)

        self.play_video_slow_speed_button = QPushButton(self)
        self.play_video_slow_speed_button.setIcon(QIcon('button_icon_8.png'))
        self.play_video_slow_speed_button.setIconSize(QSize(76, 76))
        self.play_video_slow_speed_button.move(360, 1060)
        self.play_video_slow_speed_button.resize(80, 80)
        self.play_video_slow_speed_button.clicked.connect(self.check_play_video_slow_speed_button)

        self.play_video_medium_speed_button = QPushButton(self)
        self.play_video_medium_speed_button.setIcon(QIcon('button_icon_9.png'))
        self.play_video_medium_speed_button.setIconSize(QSize(76, 76))
        self.play_video_medium_speed_button.move(445, 1060)
        self.play_video_medium_speed_button.resize(80, 80)
        self.play_video_medium_speed_button.clicked.connect(self.check_play_video_medium_speed_button)

        self.play_video_max_speed_button = QPushButton(self)
        self.play_video_max_speed_button.setIcon(QIcon('button_icon_10.png'))
        self.play_video_max_speed_button.setIconSize(QSize(76, 76))
        self.play_video_max_speed_button.move(530, 1060)
        self.play_video_max_speed_button.resize(80, 80)
        self.play_video_max_speed_button.clicked.connect(self.check_play_video_max_speed_button)
        self.update_video_playback_buttons(inactivate = True)
    def add_data_plot_window(self):
        self.data_plot_window = QScrollArea(self)
        self.data_plot_window.move(1015, 25)
        self.data_plot_window.resize(1000, 1000)
        self.data_plot_window.setFrameShape(QFrame.Panel)
        self.data_plot_window.setFrameShadow(QFrame.Sunken)
        self.data_plot_window.setLineWidth(5)

    def update_preview_frame(self, frame, frame_width, frame_height):
        format = QImage.Format_RGB888
        self.preview_frame = QImage(frame.data, frame_width, frame_height, format)
        if frame_height > 1000 and frame_height > frame_width:
           self.preview_frame = self.preview_frame.scaledToHeight(1000)
        elif frame_width > 1000:
           self.preview_frame = self.preview_frame.scaledToWidth(1000)
        elif frame_height > frame_width:
           self.preview_frame = self.preview_frame.scaledToHeight(1000)
        else:
            self.preview_frame = self.preview_frame.scaledToWidth(1000)
        frame = cv2.resize(frame, dsize=(self.preview_frame.width(), self.preview_frame.height()), interpolation=cv2.INTER_CUBIC).copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.preview_frame = QImage(frame.data, self.preview_frame.width(), self.preview_frame.height(), format)
    def update_preview_frame_window(self, clear = False):
        if not clear:
            self.preview_frame_window.setPixmap(QPixmap.fromImage(self.preview_frame))
        else:
            self.preview_frame_window.clear()
    def update_data_plot_window(self, clear = False):
        if not clear:
            self.data_plot_window.setWidget(self.data_plot)
        else:
            self.data_plot.deleteLater()
            self.data_plot.setGeometry(0, 0, 0, 0)
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
    def update_tracking_video_time_textbox(self, activate = False, inactivate = False):
        if activate:
            if not self.tracking_video_time_textbox.isEnabled():
                self.tracking_video_time_textbox.setEnabled(True)
        if inactivate:
            if self.tracking_video_time_textbox.isEnabled():
                self.tracking_video_time_textbox.setEnabled(False)
        if self.tracking_video_time_textbox.isEnabled():
            self.tracking_video_time_textbox.setText('{0}'.format(round(self.frame_number / self.video_fps, 2)))
        else:
            self.tracking_video_time_textbox.setText('{0}'.format(0))
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
    def update_video_playback_buttons(self, activate = False, inactivate = False):
        if activate:
            if not self.pause_video_button.isEnabled():
                self.pause_video_button.setEnabled(True)
            if not self.play_video_slow_speed_button.isEnabled():
                self.play_video_slow_speed_button.setEnabled(True)
            if not self.play_video_medium_speed_button.isEnabled():
                self.play_video_medium_speed_button.setEnabled(True)
            if not self.play_video_max_speed_button.isEnabled():
                self.play_video_max_speed_button.setEnabled(True)
        if inactivate:
            if self.pause_video_button.isEnabled():
                self.pause_video_button.setEnabled(False)
            if self.play_video_slow_speed_button.isEnabled():
                self.play_video_slow_speed_button.setEnabled(False)
            if self.play_video_medium_speed_button.isEnabled():
                self.play_video_medium_speed_button.setEnabled(False)
            if self.play_video_max_speed_button.isEnabled():
                self.play_video_max_speed_button.setEnabled(False)

    def trigger_open_tracked_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "","Video Files (*.avi; *.mp4)", options = QFileDialog.Options())
        if self.video_path:
            self.get_video_attributes()
            success, self.frame = ut.load_frame_into_memory(self.video_path, self.frame_number - 1, convert_to_grayscale = False)
            if success and self.frame is not None:
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_frame_window_slider(activate = True)
                self.update_tracking_video_time_textbox(activate = True)
                self.update_update_preview_button(activate = True)
                self.update_frame_change_buttons(activate = True)
                self.update_video_playback_buttons(activate = True)
    def trigger_update_preview(self):
        if self.video_path is not None:
            success, self.frame = ut.load_frame_into_memory(self.video_path, self.frame_number - 1, convert_to_grayscale = False)
            if success and self.frame is not None:
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_frame_window_slider(activate = True)
                self.update_tracking_video_time_textbox(activate = True)
                self.update_update_preview_button(activate = True)
                self.update_frame_change_buttons(activate = True)
    def trigger_load_tracking_results(self):
        self.tracking_data_path, _ = QFileDialog.getOpenFileName(self, "Open Tracking Data", "","Tracking Data (*.npy)", options = QFileDialog.Options())
        if self.tracking_data_path:
            data = np.load(self.tracking_data_path).item()
            self.data_plot = DataPlot()
            self.data_plot.initialize_class_variables(data = data)
            self.data_plot.calculate_variables()
            self.data_plot.update_plots()
            self.update_data_plot_window()
    def trigger_unload_all_plotting(self):
        self.initialize_class_variables()
        self.update_preview_frame_window(clear = True)
        self.update_frame_window_slider(inactivate = True)
        self.update_tracking_video_time_textbox(inactivate = True)
        self.update_update_preview_button(inactivate = True)
        self.update_frame_change_buttons(inactivate = True)
        self.update_video_playback_buttons(inactivate = True)
        self.update_frame_window_slider_position()
        self.update_data_plot_window(clear = True)
    def trigger_pause_video(self):
        if self.video_playback_thread:
            self.video_playback_thread.close()
        if self.play_video_slow_speed:
            self.play_video_slow_speed = False
        if self.play_video_max_speed:
            self.play_video_max_speed = False
    def trigger_play_video_slow_speed(self):
        if self.play_video_slow_speed:
            self.frame_number += 1
            if self.frame_number <= self.video_n_frames:
                self.trigger_update_preview()
            else:
                self.video_playback_thread.close()
                self.frame_number = 1
                self.trigger_update_preview()
                self.video_playback_thread.start_thread = True
                self.video_playback_thread.start()
    def trigger_play_video_medium_speed(self):
        if self.play_video_medium_speed:
            self.frame_number += 10
            if self.frame_number <= self.video_n_frames:
                self.trigger_update_preview()
            else:
                self.video_playback_thread.close()
                self.frame_number = 1
                self.trigger_update_preview()
                self.video_playback_thread.start_thread = True
                self.video_playback_thread.start()
    def trigger_play_video_max_speed(self):
        if self.play_video_max_speed:
            self.frame_number += 50
            if self.frame_number <= self.video_n_frames:
                self.trigger_update_preview()
            else:
                self.video_playback_thread.close()
                self.frame_number = 1
                self.trigger_update_preview()
                self.video_playback_thread.start_thread = True
                self.video_playback_thread.start()

    def check_tracking_video_time_textbox(self):
        try:
            time = float(self.tracking_video_time_textbox.text())
            if time > self.video_n_frames / self.video_fps:
                self.frame_number = self.video_n_frames
            else:
                if time > 0:
                    self.frame_number = int(time * self.video_fps)
                else:
                    self.frame_number = 1
        except:
            pass
        self.trigger_update_preview()
    def check_frame_window_slider_moved(self):
        self.frame_number = int(self.frame_window_slider.sliderPosition())
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
    def check_pause_video_button(self):
        self.trigger_pause_video()
    def check_play_video_slow_speed_button(self):
        if not self.play_video_slow_speed:
            if self.play_video_medium_speed:
                self.play_video_medium_speed = False
                self.video_playback_thread.close()
            if self.play_video_max_speed:
                self.play_video_max_speed = False
                self.video_playback_thread.close()
            self.video_playback_thread = VideoPlaybackThread()
            self.video_playback_thread.start()
            self.video_playback_thread.time_signal.connect(self.trigger_play_video_slow_speed)
            self.play_video_slow_speed = True
    def check_play_video_medium_speed_button(self):
        if not self.play_video_medium_speed:
            if self.play_video_slow_speed:
                self.play_video_slow_speed = False
                self.video_playback_thread.close()
            if self.play_video_max_speed:
                self.play_video_max_speed = False
                self.video_playback_thread.close()
            self.video_playback_thread = VideoPlaybackThread()
            self.video_playback_thread.start()
            self.video_playback_thread.time_signal.connect(self.trigger_play_video_medium_speed)
            self.play_video_medium_speed = True
    def check_play_video_max_speed_button(self):
        if not self.play_video_max_speed:
            if self.play_video_slow_speed:
                self.play_video_slow_speed = False
                self.video_playback_thread.close()
            if self.play_video_medium_speed:
                self.play_video_medium_speed = False
                self.video_playback_thread.close()
            self.video_playback_thread = VideoPlaybackThread()
            self.video_playback_thread.video_fps = self.video_fps
            self.video_playback_thread.start()
            self.video_playback_thread.time_signal.connect(self.trigger_play_video_max_speed)
            self.play_video_max_speed = True

class DataPlot(QMainWindow):

    def __init__(self):
        super(DataPlot, self).__init__()
        self.initUI()

    def initUI(self):
        # self.initialize_class_variables()

        self.data_plots = QWidget()
        self.setCentralWidget(self.data_plots)
        layout = QVBoxLayout(self.data_plots)

        self.tail_angle_plot = FigureCanvas(Figure(figsize=(9, 5)))
        self.tail_angle_plot_toolbar = NavigationToolbar(self.tail_angle_plot, self.tail_angle_plot)
        layout.addWidget(self.tail_angle_plot)

        self.heading_angle_plot = FigureCanvas(Figure(figsize=(9, 5)))
        self.heading_angle_plot_toolbar = NavigationToolbar(self.heading_angle_plot, self.heading_angle_plot)
        layout.addWidget(self.heading_angle_plot)

    def initialize_class_variables(self, data):
        self.heading_angle_array = data['heading_angle_array']
        self.tail_coord_array = data['tail_coord_array']
        self.body_coord_array = data['body_coord_array']
        self.eye_angle_array = data['eye_angle_array']
        self.video_n_frames = data['video_n_frames']
        self.video_fps = data['video_fps']
        self.colours = data['colours']
        self.colours = [[self.colours[i][2]/255, self.colours[i][1]/255, self.colours[i][0]/255] for i in range(len(self.colours))]
        self.dist_tail_points = data['dist_tail_points']
        self.dist_eyes = data['dist_eyes']
        self.dist_swim_bladder = data['dist_swim_bladder']
        self.eyes_threshold = data['eyes_threshold']
        self.pixel_threshold = data['pixel_threshold']
        self.frame_change_threshold = data['frame_change_threshold']

    def calculate_variables(self):
        self.smoothing_factor = 3

        self.tail_angles = [[np.arctan2(self.tail_coord_array[j][i + 1][0] - self.tail_coord_array[j][i][0], self.tail_coord_array[j][i + 1][1] - self.tail_coord_array[j][i][1]) for i in range(len(self.tail_coord_array[0]) - 1)] for j in range(len(self.tail_coord_array))]
        self.body_tail_angles = [np.arctan2(self.tail_coord_array[j][0][0] - self.body_coord_array[j][0], self.tail_coord_array[j][0][1] - self.body_coord_array[j][1]) for j in range(len(self.tail_coord_array))]
        self.tail_angles = [[self.tail_angles[j][i] - self.body_tail_angles[j] for i in range(len(self.tail_angles[0]))] for j in range(len(self.tail_angles))]
        self.tail_angles = [[self.tail_angles[i][j] for i in range(len(self.tail_angles))] for j in range(len(self.tail_angles[0]))]

        for i in range(len(self.tail_angles)):
            for j in range(1, len(self.tail_angles[i])):
                if self.tail_angles[i][j] >= 0.9 * np.pi:
                    self.tail_angles[i][j] -= np.pi * 2
                elif self.tail_angles[i][j] <= 0.9 * -np.pi:
                    self.tail_angles[i][j] += np.pi * 2

        self.sum_tail_angles = [np.sum([abs(self.tail_angles[i][j]) for i in range(len(self.tail_angles))]) for j in range(len(self.tail_angles[0]))]
        self.tail_angle_frames = np.where([self.sum_tail_angles[i] == self.sum_tail_angles[i + 1] == self.sum_tail_angles[i + 2] for i in range(len(self.sum_tail_angles) - 2)])[0]
        self.tail_angle_frames = np.where([self.sum_tail_angles[i] == self.sum_tail_angles[i + 1] for i in range(len(self.sum_tail_angles) - 1)])[0]
        for i in range(1, len(self.tail_angle_frames)):
            if self.tail_angle_frames[i] - self.tail_angle_frames[i - 1] == 2:
                self.tail_angle_frames = np.append(self.tail_angle_frames, self.tail_angle_frames[i - 1] + 1)
            elif self.tail_angle_frames[i] - self.tail_angle_frames[i - 1] == 3:
                self.tail_angle_frames = np.append(self.tail_angle_frames, self.tail_angle_frames[i - 1] + 1)
                self.tail_angle_frames = np.append(self.tail_angle_frames, self.tail_angle_frames[i - 1] + 2)

        for i in range(len(self.tail_angles)):
            for j in self.tail_angle_frames:
                self.tail_angles[i][j] = 0.0
        self.smoothed_tail_angles = [np.convolve(self.tail_angles[i], np.ones(self.smoothing_factor)/self.smoothing_factor, mode = 'same') for i in range(len(self.tail_angles))]

        j = 0
        if np.isnan(self.heading_angle_array[0]):
            while np.isnan(self.heading_angle_array[0]):
                if not np.isnan(self.heading_angle_array[j]):
                    self.heading_angle_array[0] = self.heading_angle_array[j]
                j += 1

        self.heading_angles = np.array([self.heading_angle_array[i] - self.heading_angle_array[0] for i in range(len(self.heading_angle_array))])

        i = 0
        for j in range(len(self.heading_angles)):
            if j not in self.tail_angle_frames:
                i = j
            else:
                self.heading_angles[j] = self.heading_angles[i]

        for i in range(1, len(self.heading_angles)):
            if self.heading_angles[i] - self.heading_angles[i - 1] > np.pi:
                self.heading_angles[i:] -= np.pi * 2
            elif self.heading_angles[i] - self.heading_angles[i - 1] < -np.pi:
                self.heading_angles[i:] += np.pi * 2

        self.smoothed_heading_angles = np.convolve(self.heading_angles, np.ones(self.smoothing_factor)/self.smoothing_factor, mode = 'same')

        self.eye_angles = [[self.eye_angle_array[i][j] - self.heading_angle_array[i] for i in range(len(self.eye_angle_array))] for j in range(len(self.eye_angle_array[0]))]

        i = 0
        for k in range(len(self.eye_angles)):
            for j in range(len(self.eye_angles[k])):
                if j not in self.tail_angle_frames:
                    i = j
                else:
                    self.eye_angles[k][j] = self.eye_angles[k][i]

        for j in range(len(self.eye_angles)):
            for i in range(1, len(self.eye_angles[j])):
                if self.eye_angles[j][i] - self.eye_angles[j][i - 1] > np.pi * 0.9:
                    self.eye_angles[j][i] -= np.pi * 2
                elif self.eye_angles[j][i] - self.eye_angles[j][i - 1] < -np.pi * 0.9:
                    self.eye_angles[j][i] += np.pi * 2

        for j in range(len(self.eye_angles)):
            for i in range(1, len(self.eye_angles[j])):
                if self.eye_angles[j][i] > np.pi:
                    self.eye_angles[j][i] -= np.pi * 2
                elif self.eye_angles[j][i] < -np.pi:
                    self.eye_angles[j][i] += np.pi * 2

        self.smoothed_eye_angles = [np.convolve(self.eye_angles[i], np.ones(self.smoothing_factor)/self.smoothing_factor, mode = 'same') for i in range(len(self.eye_angles))]

        self.timepoints = np.linspace(0, self.video_n_frames / self.video_fps, self.video_n_frames)

    def update_plots(self):

        self.tail_angle_plot_axis = self.tail_angle_plot.figure.subplots()
        [self.tail_angle_plot_axis.plot(self.timepoints, self.smoothed_tail_angles[i], color = self.colours[i], lw = 1) for i in range(len(self.smoothed_tail_angles))]
        self.tail_angle_plot_axis.set_xlabel('Time (s)')
        self.tail_angle_plot_axis.set_ylabel('Angle (radians)')
        self.tail_angle_plot_axis.set_title('Tail Kinematics Over Time')

        self.heading_angle_plot_axis = self.heading_angle_plot.figure.subplots()
        self.heading_angle_plot_axis.plot(self.timepoints, self.smoothed_heading_angles, color = self.colours[-1], lw = 1)
        self.heading_angle_plot_axis.set_xlabel('Time (s)')
        self.heading_angle_plot_axis.set_ylabel('Angle (radians)')
        self.heading_angle_plot_axis.set_title('Heading Angle Over Time')

        # xlim_start = -100/video_fps
        # xlim_end = 100/video_fps

class VideoPlaybackThread(QThread):

    time_signal = pyqtSignal(float)

    def __init__(self):
        super(VideoPlaybackThread, self).__init__()
        self.start_thread = True
        # self.video_fps = 1

    def run(self):
        while self.start_thread:
            time_now = time.perf_counter()
            self.time_signal.emit(time_now)
            time.sleep(0.1)

    def close(self):
        self.start_thread = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
