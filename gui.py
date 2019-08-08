import os
import glob
from pathlib import Path
from PIL import Image, ImageDraw

# debugging
# import traceback

# Project libraries
import data_util
import visual_util
import config as CONFIG
from pyqt5_mpl_canvas import PyQt5MPLCanvas

# Data libraries
import pandas as pd
import seaborn as sns

# Matplotlib/PyQt5 libraries
from matplotlib.backends.qt_compat import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import uic

class GUI(QtWidgets.QMainWindow):
    # Dot parameters
    WHITE_DOT_IMAGE_PATH = str(Path.cwd() / ('_images/white_dot.png'))
    COLORED_DOT_IMAGE_PATH_PREFIX = str(Path.cwd() / '_images/colored_dots/colored_dot_')
    DOT_SIZE = 19
    DOT_PERCENT_INWARDS = 20
    DOT_MARGIN_ADJUSTMENT = (DOT_PERCENT_INWARDS / 100.0) * DOT_SIZE

    # Constructor
    def __init__(self):
        super().__init__()

        uic.loadUi('app_gui.ui', self)
        self._connect_GUI_components_to_functions()
        self._init_blank_plot()

    # Connect GUI components to functions
    def _connect_GUI_components_to_functions(self):
        self._directory_selection_button.clicked.connect(self._process_directory_selection_button_click)
        self._participant_select_all_button.clicked.connect(self._process_participant_select_all_button_click)
        self._participant_deselect_all_button.clicked.connect(self._process_participant_deselect_all_button_click)
        self._participant_selection_button.clicked.connect(self._process_participant_selection_button_click)
        # stimulus connection happens in _init_stimulus_selection_interface()
        self._data_type_selection_menu.currentTextChanged.connect(self._set_plot_from_data)
        self._analysis_type_selection_menu.currentTextChanged.connect(self._set_plot_from_data)
        self._axes_selection_check_box.stateChanged.connect(self._set_plot_from_data)
        self._only_data_on_stimulus_selection_check_box.stateChanged.connect(self._set_plot_from_data)

    # Processes the directory selection button click
    def _process_directory_selection_button_click(self):
        # disable/clear latter setup options
        self._disable_participant_selection_interface()
        self._disable_stimulus_selection_interface()
        self._disable_data_type_selection_interface()
        self._disable_analysis_type_selection_interface()
        self._disable_matplotlib_configurations()

        try:
            self._data_directory_path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
            self._init_participant_selection_interface()
        except FileNotFoundError:
            pass

    # Processes the select all button click in the participant selection interface
    def _process_participant_select_all_button_click(self):
        for participant_selection_check_box in self._participant_selection_check_box_list:
            participant_selection_check_box.setChecked(True)

    # Processes the deselect all button click in the participant selection interface
    def _process_participant_deselect_all_button_click(self):
        for participant_selection_check_box in self._participant_selection_check_box_list:
            participant_selection_check_box.setChecked(False)

    # Processes the participant selection button click
    def _process_participant_selection_button_click(self):
        # List of check boxes of selected participants
        self._selected_participant_check_box_list = []
        for participant_selection_check_box in self._participant_selection_check_box_list:
            if participant_selection_check_box.isChecked():
                self._selected_participant_check_box_list.append(participant_selection_check_box)

        # reset previous assignment of color palette
        for check_box in self._participant_selection_check_box_list:
            check_box.setStyleSheet("")
        # generate color palette
        self._color_palette = sns.color_palette(n_colors = len(self._participant_selection_check_box_list))
        self._scaled_color_palette = visual_util._scale_palette(self._color_palette)
        self._color_palette_dict = {}
        # assigning color palette
        for i in range(len(self._selected_participant_check_box_list)):
            colored_dot_image_path = self._generate_colored_dot(self._scaled_color_palette[i], i)
            selected_participant_check_box = self._selected_participant_check_box_list[i]
            selected_participant_check_box.setStyleSheet("QCheckBox::indicator:unchecked {image: url(" + self.WHITE_DOT_IMAGE_PATH + ");}" +
                                                         "QCheckBox::indicator:checked {image: url(" + colored_dot_image_path + ");}")
            self._color_palette_dict[selected_participant_check_box.text()] = self._color_palette[i]

        if len(self._selected_participant_check_box_list) != 0:
            self._error_message.setText('')

            self._init_stimulus_selection_interface()
            self._init_data_type_selection_interface()
            self._init_analysis_type_selection_interface()
            self._init_matplotlib_configurations()

            self._set_plot_from_data()
        else:
            self._error_message.setText('No participants selected. Please select at least one participant to refresh the plot area.')


    # Processes a click on the plot
    def _process_plot_click(self, event):
        pass

    # Initializes the check box selection area to select
    # the participants to view
    def _init_participant_selection_interface(self):
        if not hasattr(self, '_participant_selection_layout'):
            self._participant_selection_layout = QtWidgets.QVBoxLayout()
            self._participant_selection_widget_holder.setLayout(self._participant_selection_layout)

        # Import eligible .tsv files
        saved_cwd = os.getcwd()
        os.chdir(self._data_directory_path)
        participant_file_list = glob.glob('*.{}'.format('tsv'))
        os.chdir(saved_cwd)
        self._participant_selection_check_box_list = []

        # generate white dot
        self._generate_white_dot()

        # initialize check boxes for selected participants
        for i in range(len(participant_file_list)):
            check_box_widget = QtWidgets.QCheckBox()
            check_box_widget.setText(participant_file_list[i])
            self._participant_selection_layout.addWidget(check_box_widget)
            self._participant_selection_check_box_list.append(check_box_widget)

        # Enable interface
        self._participant_select_all_button.setEnabled(True)
        self._participant_deselect_all_button.setEnabled(True)
        self._participant_selection_menu.setEnabled(True)
        self._participant_selection_button.setEnabled(True)

    def _disable_participant_selection_interface(self):
        # Disable interface
        self._participant_select_all_button.setEnabled(False)
        self._participant_deselect_all_button.setEnabled(False)
        self._participant_selection_menu.setEnabled(False)
        self._participant_selection_button.setEnabled(False)

        if hasattr(self, '_participant_selection_check_box_list'):
            for participant_selection_check_box in self._participant_selection_check_box_list:
                self._participant_selection_layout.removeWidget(participant_selection_check_box)
                participant_selection_check_box.hide() # necessary for removing checkboxes from
                                                       # old participant list from display once
                                                       # new directory is selected
            self._participant_selection_check_box_list = []

    # Initializes the drop down menu to select the stimulus
    # based on stimuli available in the specified tsv file
    def _init_stimulus_selection_interface(self):
        # disconnect stimulus selection from plotting
        try:
            self._stimulus_selection_menu.currentTextChanged.disconnect()
        except Exception:
            pass

        # clear stimulus selection menu
        self._stimulus_selection_menu.clear()

        # initialize with stimulus options within specified tsv file
        for stimulus in visual_util._get_found_stimuli(self._selected_participant_check_box_list, self._data_directory_path):
            self._stimulus_selection_menu.addItem(str(stimulus))

        # connect interface
        self._stimulus_selection_menu.currentTextChanged.connect(self._set_plot_from_data)

        # Enable interface
        self._stimulus_selection_menu.setEnabled(True)

    def _disable_stimulus_selection_interface(self):
        # Disable interface
        self._stimulus_selection_menu.setEnabled(False)

    def _init_data_type_selection_interface(self):
        if self._data_type_selection_menu.findText("Gaze Data") == -1:
            self._data_type_selection_menu.addItem("Gaze Data")
        if self._data_type_selection_menu.findText("Fixation Data") == -1:
            self._data_type_selection_menu.addItem("Fixation Data")

        # Enable interface
        self._data_type_selection_menu.setEnabled(True)

    def _disable_data_type_selection_interface(self):
        # Disable interface
        self._data_type_selection_menu.setEnabled(False)

        # clear data type selection menu
        self._data_type_selection_menu.clear()

    def _init_analysis_type_selection_interface(self):
        if self._analysis_type_selection_menu.findText("Scatter Plot") == -1:
            self._analysis_type_selection_menu.addItem("Scatter Plot")
        if self._analysis_type_selection_menu.findText("Line Plot") == -1:
            self._analysis_type_selection_menu.addItem("Line Plot")
        if self._analysis_type_selection_menu.findText("Heat Map") == -1:
            self._analysis_type_selection_menu.addItem("Heat Map")

        # Enable interface
        self._analysis_type_selection_menu.setEnabled(True)

    def _disable_analysis_type_selection_interface(self):
        # Disable interface
        self._analysis_type_selection_menu.setEnabled(False)

        # clear analysis type selection menu
        self._analysis_type_selection_menu.clear()

    # Displays matplotlib configurations
    def _init_matplotlib_configurations(self):
        # Enable interface
        self._axes_selection_check_box.setEnabled(True)
        self._only_data_on_stimulus_selection_check_box.setEnabled(True)

    # Disables matplotlib configurations
    def _disable_matplotlib_configurations(self):
        # Disable interface
        self._axes_selection_check_box.setEnabled(False)
        self._only_data_on_stimulus_selection_check_box.setEnabled(False)

    # Initializes a blank plot
    def _init_blank_plot(self):
        self._plot = visual_util._get_blank_plot()
        self._set_canvas()

    # Sets and displays a new canvas
    # based upon self._plot
    def _set_canvas(self):
        if hasattr(self, '_canvas'): # if this canvas is not the initial blank canvas
            self._previous_canvas = self._canvas

        self._canvas = PyQt5MPLCanvas(self._plot)
        self._canvas.mpl_connect('button_press_event', self._process_plot_click)

        self._hide_all_widgets()
        if self._plotting_row_plot.indexOf(self._plot_placeholder) != -1: # if the plot placeholder is still on the display
            self._plotting_row_plot.removeWidget(self._plot_placeholder)
        elif hasattr(self, '_previous_canvas'): # if this canvas is not the initial blank canvas
            self._plotting_row_plot.removeWidget(self._previous_canvas)
        self._plotting_row_plot.addWidget(self._canvas)
        self._show_all_widgets()

    # Initializes the plot to be displayed
    def _set_plot_from_data(self):
        # plotting
        self._stimulus_filtered_data_frame = data_util._get_data_frame_multiple_participants(list(map(visual_util._get_check_box_text, self._selected_participant_check_box_list)),
                                                                                                                   self._data_directory_path,
                                                                                                                   stimulus_file_name = self._stimulus_selection_menu.currentText())
        try:
            if (self._data_type_selection_menu.currentText() == "Gaze Data" and
               self._analysis_type_selection_menu.currentText() == "Scatter Plot"):
                self._plot = visual_util._get_gaze_scatter_plot(self._stimulus_filtered_data_frame,
                                                                self._color_palette_dict,
                                                                self._stimulus_selection_menu.currentText(),
                                                                self._axes_selection_check_box.isChecked(),
                                                                self._only_data_on_stimulus_selection_check_box.isChecked())
            elif (self._data_type_selection_menu.currentText() == "Fixation Data" and
                 self._analysis_type_selection_menu.currentText() == "Scatter Plot"):
                self._plot = visual_util._get_fixation_scatter_plot(self._stimulus_filtered_data_frame,
                                                                 self._color_palette_dict,
                                                                 self._stimulus_selection_menu.currentText(),
                                                                 self._axes_selection_check_box.isChecked(),
                                                                 self._only_data_on_stimulus_selection_check_box.isChecked())
            elif (self._data_type_selection_menu.currentText() == "Gaze Data" and
                 self._analysis_type_selection_menu.currentText() == "Line Plot"):
                self._plot = visual_util._get_gaze_line_plot(self._stimulus_filtered_data_frame,
                                                                    self._color_palette_dict,
                                                                    self._stimulus_selection_menu.currentText(),
                                                                    self._axes_selection_check_box.isChecked(),
                                                                    self._only_data_on_stimulus_selection_check_box.isChecked())
            elif (self._data_type_selection_menu.currentText() == "Fixation Data" and
                 self._analysis_type_selection_menu.currentText() == "Line Plot"):
                self._plot = visual_util._get_fixation_line_plot(self._stimulus_filtered_data_frame,
                                                                 self._color_palette_dict,
                                                                 self._stimulus_selection_menu.currentText(),
                                                                 self._axes_selection_check_box.isChecked(),
                                                                 self._only_data_on_stimulus_selection_check_box.isChecked())
            elif (self._data_type_selection_menu.currentText() == "Gaze Data" and
                 self._analysis_type_selection_menu.currentText() == "Heat Map"):
                self._plot = visual_util._get_gaze_heat_map(self._stimulus_filtered_data_frame,
                                                                 self._color_palette_dict,
                                                                 self._stimulus_selection_menu.currentText(),
                                                                 self._axes_selection_check_box.isChecked(),
                                                                 self._only_data_on_stimulus_selection_check_box.isChecked())
            elif (self._data_type_selection_menu.currentText() == "Fixation Data" and
                 self._analysis_type_selection_menu.currentText() == "Heat Map"):
                self._plot = visual_util._get_fixation_heat_map(self._stimulus_filtered_data_frame,
                                                                 self._color_palette_dict,
                                                                 self._stimulus_selection_menu.currentText(),
                                                                 self._axes_selection_check_box.isChecked(),
                                                                 self._only_data_on_stimulus_selection_check_box.isChecked())
            self._error_message.setText('')
            self._set_canvas()
        except FileNotFoundError:
            self._error_message.setText('Stimulus image file ' +
                                        self._stimulus_selection_menu.currentText() +
                                        ' not found.')

    # Hides all widgets
    def _hide_all_widgets(self):
        # Error bar
        self._error_message_scroll_area.hide()
        self._error_message.hide()
        # Directory selection
        self._directory_selection_button.hide()
        # Participant selection
        self._participant_select_all_button.hide()
        self._participant_deselect_all_button.hide()
        self._participant_selection_menu.hide()
        self._participant_selection_button.hide()
        # Stimulus selection
        self._stimulus_selection_menu.hide()
        # Data type selection
        self._data_type_selection_menu.hide()
        # Analysis type selection
        self._analysis_type_selection_menu.hide()
        # Matplotlib options
        self._axes_selection_check_box.hide()
        self._only_data_on_stimulus_selection_check_box.hide()
        # Plot
        self._plot_placeholder.hide()
        if hasattr(self, '_previous_canvas'): # if this canvas is not the initial blank canvas
            self._previous_canvas.hide()
        self._canvas.hide()

    # Shows all widgets
    def _show_all_widgets(self):
        # Error bar
        self._error_message_scroll_area.show()
        self._error_message.show()
        # Directory selection
        self._directory_selection_button.show()
        # Participant selection
        self._participant_select_all_button.show()
        self._participant_deselect_all_button.show()
        self._participant_selection_menu.show()
        self._participant_selection_button.show()
        # Stimulus selection
        self._stimulus_selection_menu.show()
        # Data type selection
        self._data_type_selection_menu.show()
        # Analysis type selection
        self._analysis_type_selection_menu.show()
        # Matplotlib options
        self._axes_selection_check_box.show()
        self._only_data_on_stimulus_selection_check_box.show()
        # Plot
        self._plot_placeholder.show()
        if hasattr(self, '_previous_canvas'): # if this canvas is not the initial blank canvas
            self._previous_canvas.show()
        self._canvas.show()

    # Generates an image of a dot with a particular fill and outline color
    # and saves it at the specified image path
    def _generate_dot(self, fill_color, outline_color, image_path):
        window_color = self.palette().color(QtGui.QPalette.Background)
        image = Image.new('RGB', (self.DOT_SIZE, self.DOT_SIZE),
                          color=(window_color.red(), window_color.green(), window_color.blue(), 0))
        drawing = ImageDraw.Draw(image)
        drawing.ellipse((0 + self.DOT_MARGIN_ADJUSTMENT,
                         0 + self.DOT_MARGIN_ADJUSTMENT,
                         self.DOT_SIZE - self.DOT_MARGIN_ADJUSTMENT,
                         self.DOT_SIZE - self.DOT_MARGIN_ADJUSTMENT),
                        fill=fill_color,
                        outline=outline_color)
        image.save(image_path)

    # Generates an image of a dot with a particular RBG color and saves it
    # at the specified image path that has a unique ID id_num
    def _generate_colored_dot(self, scaled_color, id_num):
        red_value = scaled_color[0]
        green_value = scaled_color[1]
        blue_value = scaled_color[2]

        fill_color = (red_value, green_value, blue_value, 0)
        outline_color = (red_value, green_value, blue_value, 0)

        colored_dot_image_path = self.COLORED_DOT_IMAGE_PATH_PREFIX + (str(id_num) + '.png')

        self._generate_dot(fill_color, outline_color, colored_dot_image_path)

        return colored_dot_image_path

    # Generates an image of a white dot at its image path as specified by self.WHITE_DOT_IMAGE_PATH
    def _generate_white_dot(self):
        fill_color = 'white'
        outline_color = 'white'

        self._generate_dot(fill_color, outline_color, self.WHITE_DOT_IMAGE_PATH)


