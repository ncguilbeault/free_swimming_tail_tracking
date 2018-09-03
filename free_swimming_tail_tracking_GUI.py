# import python modules
import sys
import os
import subprocess
import cv2
import numpy as np
import free_swimming_tail_tracking as tr
# import psutil

from PyQt5.QtWidgets import QColorDialog, QApplication, QSlider, QWidget, QDesktopWidget, QTextEdit, QAction, QFileDialog, QMainWindow, QPushButton, QVBoxLayout, QLineEdit, QCheckBox, QLabel, QStatusBar, QMenuBar, QSizePolicy, QHBoxLayout, QFrame, QScrollArea
from PyQt5.QtGui import QPixmap, QColor, QFont, QImage
from PyQt5.QtCore import Qt, QEvent

class MainWindow(QMainWindow):

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
        self.add_preview_frame_number_textbox_label()
        self.add_update_preview_button()
        self.add_preview_parameters_window()
        self.add_preview_parameters_to_window()

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

    def get_main_window_attributes(self):
        self.main_window_width = QDesktopWidget().availableGeometry().width()
        self.main_window_height = QDesktopWidget().availableGeometry().height()

    def add_menubar(self):
        self.menubar = QMenuBar()
        self.menubar.resize(self.main_window_width, self.menubar.height())

    def add_statusbar(self):
        self.statusbar = QStatusBar()
        self.statusbar_message = 'Welcome to the free swimming tail tracking GUI. Begin by openning a video.'
        self.statusbar.showMessage(self.statusbar_message)
        self.statusbar.messageChanged.connect(self.update_statusbar_message)

    def update_statusbar_message(self):
        if self.statusbar.currentMessage() == '':
            self.statusbar.showMessage(self.statusbar_message)

    def add_options_to_menubar(self):
        self.options_menu = self.menubar.addMenu('&Options')
        self.add_open_video_action_to_options_menu()
        self.add_select_save_path_action_to_options_menu()
        self.add_load_background_action_to_options_menu()
        self.add_calculate_background_action_to_options_menu()

    def add_open_video_action_to_options_menu(self):
        self.open_video_action = QAction('&Open Video', self)
        self.open_video_action.setShortcut('Ctrl+O')
        self.open_video_action.setStatusTip('Open Video')
        self.open_video_action.triggered.connect(self.open_video)
        self.options_menu.addAction(self.open_video_action)

    def add_select_save_path_action_to_options_menu(self):
        self.select_save_path_action = QAction('&Select Save Path', self)
        self.select_save_path_action.setShortcut('Ctrl+S')
        self.select_save_path_action.setStatusTip('Select Save Path')
        self.select_save_path_action.triggered.connect(self.select_save_path)
        self.options_menu.addAction(self.select_save_path_action)

    def add_load_background_action_to_options_menu(self):
        self.load_background_action = QAction('&Load Background', self)
        self.load_background_action.setShortcut('Ctrl+L')
        self.load_background_action.setStatusTip('Load Background')
        self.load_background_action.triggered.connect(self.load_background)
        self.options_menu.addAction(self.load_background_action)

    def add_calculate_background_action_to_options_menu(self):
        self.calculate_background_action = QAction('&Calculate Background', self)
        self.calculate_background_action.setShortcut('Ctrl+B')
        self.calculate_background_action.setStatusTip('Calculate Background')
        self.calculate_background_action.triggered.connect(self.calculate_background)
        self.options_menu.addAction(self.calculate_background_action)

    def calculate_background(self):
        if self.video_path is not None:
            self.background_path = 'Background calculated and loaded into memory/Background calculated and loaded into memory'
            if self.background_path:
                self.background = tr.calculate_background(self.video_path)[0]
                self.get_background_attributes()
                self.update_descriptors()
                self.preview_background_checkbox.setEnabled(True)

    def select_save_path(self):
        self.save_path = QFileDialog.getExistingDirectory(self, 'Select save path.')
        if self.save_path:
            self.update_descriptors()

    def load_background(self):
        self.background_path, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Image Files (*.tif)", options=QFileDialog.Options())
        if self.background_path:
            self.background = tr.load_background_into_memory(self.background_path)
            self.get_background_attributes()
            self.update_descriptors()
            self.preview_background_checkbox.setEnabled(True)

    def open_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Video Files (*.avi)", options=QFileDialog.Options())
        if self.video_path:
            self.get_video_attributes()
            self.update_descriptors()
            self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
            if self.frame is not None:
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_frame_window_slider()
                self.update_preview_frame_number_textbox()

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

    def update_frame_window_slider(self):
        self.frame_window_slider.setMinimum(1)
        self.frame_window_slider.setMaximum(self.video_n_frames)
        self.frame_window_slider.setValue(self.frame_number)

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
        self.video_path_folder_descriptor.move(1020, 100)
        self.video_path_folder_descriptor.resize(490, 20)
        self.video_path_folder_descriptor.setText('Video Folder: {0}'.format(self.video_path_folder))
        self.video_path_folder_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_path_folder_descriptor.setFont(font)

        self.video_path_basename_descriptor = QLabel(self)
        self.video_path_basename_descriptor.move(1020, 140)
        self.video_path_basename_descriptor.resize(490, 20)
        self.video_path_basename_descriptor.setText('Video Filename: {0}'.format(self.video_path_basename))
        self.video_path_basename_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_path_basename_descriptor.setFont(font)

        self.video_n_frames_descriptor = QLabel(self)
        self.video_n_frames_descriptor.move(1020, 180)
        self.video_n_frames_descriptor.resize(490, 20)
        self.video_n_frames_descriptor.setText('Video Total Frames: {0}'.format(self.video_n_frames))
        self.video_n_frames_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_n_frames_descriptor.setFont(font)

        self.video_fps_descriptor = QLabel(self)
        self.video_fps_descriptor.move(1020, 220)
        self.video_fps_descriptor.resize(490, 20)
        self.video_fps_descriptor.setText('Video FPS: {0}'.format(self.video_fps))
        self.video_fps_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_fps_descriptor.setFont(font)

        self.video_format_descriptor = QLabel(self)
        self.video_format_descriptor.move(1020, 260)
        self.video_format_descriptor.resize(490, 20)
        self.video_format_descriptor.setText('Video Format: {0}'.format(self.video_format))
        self.video_format_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.video_format_descriptor.setFont(font)

        self.frame_width_descriptor = QLabel(self)
        self.frame_width_descriptor.move(1020, 300)
        self.frame_width_descriptor.resize(490, 20)
        self.frame_width_descriptor.setText('Frame Width: {0}'.format(self.video_frame_width))
        self.frame_width_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.frame_width_descriptor.setFont(font)

        self.frame_height_descriptor = QLabel(self)
        self.frame_height_descriptor.move(1020, 340)
        self.frame_height_descriptor.resize(490, 20)
        self.frame_height_descriptor.setText('Frame Height: {0}'.format(self.video_frame_height))
        self.frame_height_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.frame_height_descriptor.setFont(font)

        self.background_path_folder_descriptor = QLabel(self)
        self.background_path_folder_descriptor.move(1020, 380)
        self.background_path_folder_descriptor.resize(490, 20)
        self.background_path_folder_descriptor.setText('Background Folder: {0}'.format(self.background_path_folder))
        self.background_path_folder_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.background_path_folder_descriptor.setFont(font)

        self.background_path_basename_descriptor = QLabel(self)
        self.background_path_basename_descriptor.move(1020, 420)
        self.background_path_basename_descriptor.resize(490, 20)
        self.background_path_basename_descriptor.setText('Background Filename: {0}'.format(self.background_path_basename))
        self.background_path_basename_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.background_path_basename_descriptor.setFont(font)

        self.save_path_descriptor = QLabel(self)
        self.save_path_descriptor.move(1020, 460)
        self.save_path_descriptor.resize(490, 20)
        self.save_path_descriptor.setText('Save Path: {0}'.format(self.save_path))
        self.save_path_descriptor.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.save_path_descriptor.setFont(font)

    def add_frame_window_slider(self):
        self.frame_window_slider = QSlider(Qt.Horizontal, self)
        self.frame_window_slider.setToolTip('Move slider to change preview frame number.')
        self.frame_window_slider.move(5, 1040)
        self.frame_window_slider.resize(1000, 10)
        self.frame_window_slider.setFocusPolicy(Qt.StrongFocus)
        self.frame_window_slider.setTickPosition(QSlider.TicksBelow)
        self.frame_window_slider.setTickInterval(0)
        self.frame_window_slider.setSingleStep(0)
        self.set_frame_window_slider_inactive()
        self.frame_window_slider.sliderMoved.connect(self.frame_window_slider_moved)

    def set_frame_window_slider_inactive(self):
        self.frame_window_slider.setMinimum(0)
        self.frame_window_slider.setMaximum(0)
        self.frame_window_slider.setValue(0)

    def frame_window_slider_moved(self):
        if self.video_path is not None:
            self.frame_number = int(self.frame_window_slider.sliderPosition())
            self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
            if self.frame is not None:
                self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                self.update_preview_frame_window()
                self.update_preview_frame_number_textbox()

    def add_preview_frame_number_textbox(self):
        font = QFont()
        font.setPointSize(10)
        self.preview_frame_number_textbox = QLineEdit(self)
        self.preview_frame_number_textbox.move(150, 1060)
        self.preview_frame_number_textbox.resize(100, 20)
        self.preview_frame_number_textbox.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.preview_frame_number_textbox.setFont(font)
        self.preview_frame_number_textbox.textEdited.connect(self.update_preview_frame_number_textbox_after_edit)
        self.update_preview_frame_number_textbox()

    def update_preview_frame_number_textbox(self):
        self.preview_frame_number_textbox.setText('{0}'.format(self.frame_number))

    def update_preview_frame_number_textbox_after_edit(self):
        if self.preview_background:
            self.preview_frame_number_textbox.setText('{0}'.format(0))

    def add_preview_frame_number_textbox_label(self):
        font = QFont()
        font.setPointSize(10)
        self.preview_frame_number_textbox_label = QLabel(self)
        self.preview_frame_number_textbox_label.move(5, 1060)
        self.preview_frame_number_textbox_label.resize(145, 20)
        self.preview_frame_number_textbox_label.setText('Preview Frame Number: ')
        self.preview_frame_number_textbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_frame_number_textbox_label.setFont(font)

    def add_update_preview_button(self):
        self.update_preview_button = QPushButton('Update Preview', self)
        self.update_preview_button.move(5, 1090)
        self.update_preview_button.resize(245, 50)
        self.update_preview_button.clicked.connect(self.update_preview_from_button)

    def update_preview_from_button(self):
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
                    self.frame_number = 0
                self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
                if self.frame is not None:
                    self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                    self.update_preview_frame_window()
                    self.update_frame_window_slider_position()
                    self.update_preview_frame_number_textbox()

    def update_frame_window_slider_position(self):
        self.frame_window_slider.setValue(self.frame_number)

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
        self.preview_background_checkbox.stateChanged.connect(self.check_preview_background_checkbox)
        self.preview_background_checkbox_label = QLabel(self)
        self.preview_background_checkbox_label.move(1045, 1113)
        self.preview_background_checkbox_label.resize(500, 20)
        self.preview_background_checkbox_label.setText('Preview background')
        self.preview_background_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_background_checkbox_label.setFont(font)

        self.preview_background_subtracted_frame_checkbox = QCheckBox(self)
        self.preview_background_subtracted_frame_checkbox.move(1025, 1150)
        self.preview_background_checkbox.stateChanged.connect(self.check_preview_background_checkbox)
        self.preview_background_subtracted_frame_checkbox.setEnabled(False)
        self.preview_background_subtracted_frame_checkbox_label = QLabel(self)
        self.preview_background_subtracted_frame_checkbox_label.move(1045, 1153)
        self.preview_background_subtracted_frame_checkbox_label.resize(500, 20)
        self.preview_background_subtracted_frame_checkbox_label.setText('Preview background subtracted frame')
        self.preview_background_subtracted_frame_checkbox_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.preview_background_subtracted_frame_checkbox_label.setFont(font)

    def check_preview_background_checkbox(self):
        self.preview_background = self.preview_background_checkbox.isChecked()
        if self.preview_background:
            if self.video_path is not None:
                self.set_frame_window_slider_inactive()
            self.update_preview_frame(self.background, self.background_width, self.background_height)
            self.update_preview_frame_window()
            self.update_preview_frame_number_textbox_after_edit()
        else:
            if self.video_path is not None:
                self.frame = tr.load_frame_into_memory(self.video_path, self.frame_number - 1)
                if self.frame is not None:
                    self.update_preview_frame(self.frame, self.video_frame_width, self.video_frame_height)
                    self.update_preview_frame_window()
                    self.update_frame_window_slider()
                    self.update_preview_frame_number_textbox()

    # def initUI(self):
    #
    #     self.color_updater = None
    #     self.light_on = None
    #     self.light_off = None
    #     self.light_on_text = None
    #     self.light_off_text = None
    #     self.workflow_started = False
    #     self.bonsai_path = None
    #
    #     self.select_path_to_bonsai_workflow = QAction(u'Select Folder to Workflow\u2026', self)
    #     self.select_path_to_bonsai_workflow.setStatusTip('Select the folder that contains the color picker bonsai workflow.')
    #     self.select_path_to_bonsai_workflow.triggered.connect(self.update_path_to_bonsai_workflow)
    #
    #     self.menubar  = self.menuBar()
    #     self.menu = self.menubar.addMenu('&Bonsai')
    #     self.menu.addAction(self.select_path_to_bonsai_workflow)
    #
    #     self.red_button = QPushButton('Red', self)
    #     self.red_button.setToolTip('Click to select red color.')
    #     self.red_button.setStyleSheet('QPushButton {background-color: red; font-size: 20px}; QToolTip {background-color: none; font-size: 12px}')
    #     self.red_button.setStatusTip('Red Color Button')
    #     self.red_button.resize(325, 100)
    #     self.red_button.move(50, 50)
    #     self.red_button.clicked.connect(self.run_red_conditioning_workflow)
    #
    #     self.blue_button = QPushButton('Blue', self)
    #     self.blue_button.setToolTip('Click to select blue color.')
    #     self.blue_button.setStyleSheet('QPushButton {background-color: blue; font-size: 20px}; QToolTip {background-color: none; font-size: 12px}')
    #     self.blue_button.setStatusTip('Blue Color Button')
    #     self.blue_button.resize(325, 100)
    #     self.blue_button.move(375, 50)
    #     self.blue_button.clicked.connect(self.run_blue_conditioning_workflow)
    #
    #     self.green_button = QPushButton('Green', self)
    #     self.green_button.setToolTip('Click to select green color.')
    #     self.green_button.setStyleSheet('QPushButton {background-color: green; font-size: 20px}; QToolTip {background-color:none; font-size: 12px}')
    #     self.green_button.setStatusTip('Green Color Button')
    #     self.green_button.resize(325, 100)
    #     self.green_button.move(50, 150)
    #     self.green_button.clicked.connect(self.run_green_conditioning_workflow)
    #
    #     self.select_color_button = QPushButton('Other Color', self)
    #     self.select_color_button.setToolTip('Click to open a full color dialog and select a different color.')
    #     self.select_color_button.setStyleSheet('QPushButton {background-color: none; font-size: 20px}; QToolTip {background-color: none; font-size: 12px}')
    #     self.select_color_button.setStatusTip('Other Color Button')
    #     self.select_color_button.resize(325, 100)
    #     self.select_color_button.move(375, 150)
    #     self.select_color_button.clicked.connect(self.select_color)
    #
    #     self.light_on_label = QLabel('Light On:', self)
    #     self.light_on_label.setStyleSheet('font-size: 20px')
    #     self.light_on_label.resize(300, 100)
    #     self.light_on_label.move(40, 235)
    #
    #     self.light_on_slider = QSlider(Qt.Horizontal, self)
    #     self.light_on_slider.setToolTip('Move slider to change the light on time.')
    #     self.light_on_slider.setStatusTip('Light On Time Selector')
    #     self.light_on_slider.resize(550, 50)
    #     self.light_on_slider.move(150, 270)
    #     self.light_on_slider.setFocusPolicy(Qt.StrongFocus)
    #     self.light_on_slider.setTickPosition(QSlider.TicksBelow)
    #     self.light_on_slider.setTickInterval(1)
    #     self.light_on_slider.setSingleStep(1)
    #     self.light_on_slider.setMinimum(0)
    #     self.light_on_slider.setMaximum(23)
    #     self.light_on_slider.setValue(6)
    #     self.light_on = self.convert_slider_position_to_timespan(self.light_on_slider)
    #     self.light_on_text = self.convert_integer_to_time(self.light_on_slider.sliderPosition())
    #     self.set_time_labels_on_slider(slider_labels = np.arange(0, 24, 3), slider_length = 540, slider_position = [150, 250])
    #     self.light_on_slider.sliderMoved.connect(self.light_on_slider_moved)
    #
    #     self.light_off_label = QLabel('Light Off:', self)
    #     self.light_off_label.setStyleSheet('font-size: 20px')
    #     self.light_off_label.resize(300, 100)
    #     self.light_off_label.move(40, 335)
    #
    #     self.light_off_slider = QSlider(Qt.Horizontal, self)
    #     self.light_off_slider.setToolTip('Move slider to change the light off time.')
    #     self.light_off_slider.setStatusTip('Light Off Time Selector')
    #     self.light_off_slider.resize(550, 50)
    #     self.light_off_slider.move(150, 370)
    #     self.light_off_slider.setFocusPolicy(Qt.StrongFocus)
    #     self.light_off_slider.setTickPosition(QSlider.TicksBelow)
    #     self.light_off_slider.setTickInterval(1)
    #     self.light_off_slider.setSingleStep(1)
    #     self.light_off_slider.setMinimum(0)
    #     self.light_off_slider.setMaximum(23)
    #     self.light_off_slider.setValue(20)
    #     self.light_off = self.convert_slider_position_to_timespan(self.light_off_slider)
    #     self.light_off_text = self.convert_integer_to_time(self.light_off_slider.sliderPosition())
    #     self.set_time_labels_on_slider(slider_labels = np.arange(0, 24, 3), slider_length = 540, slider_position = [150, 350])
    #     self.light_off_slider.sliderMoved.connect(self.light_off_slider_moved)
    #
    #     self.start_workflow_button = QPushButton('Start Workflow', self)
    #     self.start_workflow_button.setStatusTip('Start Workflow Button')
    #     self.update_start_workflow_button()
    #     self.start_workflow_button.resize(350, 80)
    #     self.start_workflow_button.move(350, 480)
    #     self.start_workflow_button.clicked.connect(self.start_workflow)
    #     self.start_workflow_button.setEnabled(False)
    #
    #     self.stop_workflow_button = QPushButton('Stop Workflow', self)
    #     self.stop_workflow_button.setStatusTip('Stop Workflow Button')
    #     self.update_stop_workflow_button()
    #     self.stop_workflow_button.resize(350, 80)
    #     self.stop_workflow_button.move(350, 580)
    #     self.stop_workflow_button.clicked.connect(self.stop_workflow)
    #     self.stop_workflow_button.setEnabled(False)
    #
    #     self.current_color_selected = QLabel('Current Color Selected: {0}'.format(self.color_updater), self)
    #     self.current_color_selected.setStyleSheet('QLabel {font-size: 16px}')
    #     self.current_color_selected.resize(300, 100)
    #     self.current_color_selected.move(40, 450)
    #
    #     self.current_light_on_time = QLabel('Current Light On Time: {0}'.format(self.light_on_text), self)
    #     self.current_light_on_time.setStyleSheet('QLabel {font-size: 16px}')
    #     self.current_light_on_time.resize(300, 100)
    #     self.current_light_on_time.move(40, 500)
    #
    #     self.current_light_off_time = QLabel('Current Light Off Time: {}'.format(self.light_off_text), self)
    #     self.current_light_off_time.setStyleSheet('QLabel {font-size: 16px}')
    #     self.current_light_off_time.resize(300, 100)
    #     self.current_light_off_time.move(40, 550)
    #
    #     self.statusBar = QStatusBar()
    #     self.setStatusBar(self.statusBar)
    #     self.statusBar.setStyleSheet('QStatusBar QLabel {border: 0px solid black}')
    #     self.status_bar_message = 'Welcome to food conditioning color picker! Pick a color and press the Start Workflow button to start running a workflow.'
    #     self.statusBar.showMessage(self.status_bar_message)
    #     self.statusBar.messageChanged.connect(self.update_status_bar_message)
    #
    #     # self.resize(750, 680)
    #     self.setFixedSize(750, 690)
    #     self.center()
    #     self.setWindowTitle('Food Conditioning Color Picker')
    #     self.show()

    def convert_integer_to_time(self, value):
        if value == 0:
            time = '{0}:00 AM'.format(value + 12)
        elif value == 12:
            time = '{0}:00 PM'.format(value)
        elif value < 12:
            time = '{0}:00 AM'.format(value)
        else:
            time = '{0}:00 PM'.format(value - 12)
        return time

    def convert_slider_position_to_timespan(self, slider):
        value = int(slider.sliderPosition())
        if value < 10:
            return '0{}:00:00'.format(value)
        else:
            return '{}:00:00'.format(value)

    def light_on_slider_moved(self):
        self.light_on = self.convert_slider_position_to_timespan(self.light_on_slider)
        self.light_on_text = self.convert_integer_to_time(int(self.light_on_slider.sliderPosition()))
        self.current_light_on_time.setText('Current Light On Time: {}'.format(self.light_on_text))

    def light_off_slider_moved(self):
        self.light_off = self.convert_slider_position_to_timespan(self.light_off_slider)
        self.light_off_text = self.convert_integer_to_time(int(self.light_off_slider.sliderPosition()))
        self.current_light_off_time.setText('Current Light Off Time: {}'.format(self.light_off_text))

    def set_time_labels_on_slider(self, slider_labels, slider_length, slider_position):
        for i in range(len(slider_labels)):
            if int(slider_labels[i] / 12) == 0:
                if slider_labels[i] == 0:
                    self.time_label = QLabel('{}:00 AM'.format(slider_labels[i] + 12), self)
                else:
                    self.time_label = QLabel('{}:00 AM'.format(slider_labels[i]), self)
            else:
                if slider_labels[i] == 12:
                    self.time_label = QLabel('{}:00 PM'.format(slider_labels[i]), self)
                else:
                    self.time_label = QLabel('{}:00 PM'.format(slider_labels[i] - 12), self)
            self.time_label.move(slider_position[0] + ((slider_length / 23) * slider_labels[i]) - 40, slider_position[1] + 80)
            self.time_label.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(6)
            self.time_label.setFont(font)
            self.time_label.setStyleSheet('font-size: 12px')

    def update_start_workflow_button(self):
        if self.color_updater == None:
            self.start_workflow_button.setToolTip('Must select a color before starting a workflow.')
        elif not self.workflow_started:
            self.start_workflow_button.setEnabled(True)
            self.start_workflow_button.setToolTip('Click to start the workflow.')
        else:
            self.start_workflow_button.setEnabled(False)
            self.start_workflow_button.setToolTip('Workflow running. Must stop the current workflow before starting a new workflow.')

    def run_red_conditioning_workflow(self):
        self.color_updater = [255, 0, 0]
        self.current_color_selected.setText('Color Selected: {0} (R, G, B)'.format(self.color_updater))
        self.update_start_workflow_button()

    def run_green_conditioning_workflow(self):
        self.color_updater = [0, 255, 0]
        self.current_color_selected.setText('Color Selected: {0} (R, G, B)'.format(self.color_updater))
        self.update_start_workflow_button()

    def run_blue_conditioning_workflow(self):
        self.color_updater = [0, 0, 255]
        self.current_color_selected.setText('Color Selected: {0} (R, G, B)'.format(self.color_updater))
        self.update_start_workflow_button()

    def select_color(self):
        self.color_picker = QColorDialog.getColor()
        self.color_updater = [self.color_picker.red(), self.color_picker.green(), self.color_picker.blue()]
        self.current_color_selected.setText('Color Selected: {0} (R, G, B)'.format(self.color_updater))
        self.update_start_workflow_button()

    def start_workflow(self):
        if self.bonsai_path == None:
            try:
                os.chdir('C:\\Users\\Thiele Lab\\Documents\\Workflows\\Color Picker Workflow')
            except:
                self.update_path_to_bonsai_workflow()
                os.chdir(self.bonsai_path)
        else:
            os.chdir(self.bonsai_path)
        bonsai_call = ['Bonsai64.exe', 'Color_Picker.bonsai', '-p:ColorPicker.Red={0}'.format(self.color_updater[0] / 255), '-p:ColorPicker.Green={0}'.format(self.color_updater[1] / 255), '-p:ColorPicker.Blue={0}'.format(self.color_updater[2] / 255), '-p:ColorPicker.LightOn={0}'.format(self.light_on), '-p:ColorPicker.LightOff={0}'.format(self.light_off), '--start', '--noeditor']
        self.bonsai_running = subprocess.Popen(bonsai_call)
        self.workflow_started = True
        self.status_bar_message = 'Workflow running... Click the Stop Workflow button to stop the current workflow.'
        self.update_start_workflow_button()
        self.update_stop_workflow_button()

    def stop_workflow(self):
        try:
            process = psutil.Process(self.bonsai_running.pid)
            for proc in process.children(recursive=True):
                proc.kill()
            process.kill()
        except:
            pass
        self.workflow_started = False
        self.status_bar_message = 'Workflow stopped... Click the Start Workflow button to start running the workflow with the current color.'
        self.update_stop_workflow_button()
        self.update_start_workflow_button()

    def update_stop_workflow_button(self):
        if self.workflow_started:
            self.stop_workflow_button.setEnabled(True)
            self.stop_workflow_button.setToolTip('Click to stop the workflow.')
        else:
            self.stop_workflow_button.setEnabled(False)
            self.stop_workflow_button.setToolTip('No workflow started. Must start a workflow before stopping.')

    def update_path_to_bonsai_workflow(self):
        self.bonsai_path = QFileDialog.getExistingDirectory(self, 'Select folder path to bonsai workflow.')

    def closeEvent(self, event):
        # if self.workflow_started:
        #     self.stop_workflow()
        event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
