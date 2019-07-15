import os
import glob

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
        self._stimulus_selection_menu.currentTextChanged.connect(self._process_stimulus_selection_button_click)
        self._data_type_selection_menu.currentTextChanged.connect(self._process_data_type_selection_button_click)
        self._analysis_type_selection_menu.currentTextChanged.connect(self._process_analysis_type_selection_button_click)
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
            self._directory_path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
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
        # disable/clear latter setup options
        self._disable_stimulus_selection_interface()
        self._disable_data_type_selection_interface()
        self._disable_analysis_type_selection_interface()
        self._disable_matplotlib_configurations()

        # Gather list of file names of selected participants
        self._selected_participant_file_name_list = []
        for participant_selection_check_box in self._participant_selection_check_box_list:
            if (participant_selection_check_box.isChecked()):
                self._selected_participant_file_name_list.append(participant_selection_check_box.text())
        if (len(self._selected_participant_file_name_list) != 0):
            self._init_stimulus_selection_interface()

    # Processes the stimulus selection button click
    def _process_stimulus_selection_button_click(self):
        # disable/clear latter setup options
        self._disable_data_type_selection_interface()
        self._disable_analysis_type_selection_interface()
        self._disable_matplotlib_configurations()

        if (visual_util._stimulus_image_exists(self._stimulus_selection_menu.currentText())):
            self._error_message.setText('')
            self._data_frame = data_util._get_data_frame_multiple_participants(self._selected_participant_file_name_list,
                                                                               stimulus_file_name = self._stimulus_selection_menu.currentText())
            self._init_data_type_selection_interface()
        else:
            self._error_message.setText('Stimulus image file ' +
                                        self._stimulus_selection_menu.currentText() +
                                        ' not found.')

    # Processes the data type selection button click
    def _process_data_type_selection_button_click(self):
        # disable/clear latter setup options
        self._disable_analysis_type_selection_interface()
        self._disable_matplotlib_configurations()

        self._init_analysis_type_selection_interface()

    # Processes the analysis type selection button click
    def _process_analysis_type_selection_button_click(self):
        # disable/clear latter setup options
        self._disable_matplotlib_configurations()

        self._set_plot_from_data()
        self._init_matplotlib_configurations()

    # Processes a click on the plot
    def _process_plot_click(self, event):
        pass

    # Initializes the check box selection area to select
    # the participants to view
    def _init_participant_selection_interface(self):
        if (hasattr(self, '_participant_selection_layout')):
            QtWidgets.QWidget().setLayout(self._participant_selection_layout)
        self._participant_selection_layout = QtWidgets.QVBoxLayout()
        self._participant_selection_widget_holder.setLayout(self._participant_selection_layout)

        # Import eligible .tsv files
        os.chdir(self._directory_path)
        participant_file_list = glob.glob('*.{}'.format('tsv'))
        self._participant_selection_check_box_list = []
        for participant_file in participant_file_list:
            check_box_widget = QtWidgets.QCheckBox()
            check_box_widget.setText(participant_file)
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

        if (hasattr(self, '_participant_selection_check_box_list')):
            for participant_selection_check_box in self._participant_selection_check_box_list:
                self._participant_selection_layout.removeWidget(participant_selection_check_box)
            self._participant_selection_check_box_list = []

    # Initializes the drop down menu to select the stimulus
    # based on stimuli available in the specified tsv file
    def _init_stimulus_selection_interface(self):
        # store all data from multiple participants
        self._data_frame = data_util._get_data_frame_multiple_participants(self._selected_participant_file_name_list)

        # initialize with stimulus options within specified tsv file
        for stimulus in data_util._get_stimuli(self._data_frame):
            if (str(stimulus) not in CONFIG.EXCLUDE_STIMULI_LIST):
                self._stimulus_selection_menu.addItem(str(stimulus))

        # Enable interface
        self._stimulus_selection_menu.setEnabled(True)

    def _disable_stimulus_selection_interface(self):
        # Disable interface
        self._stimulus_selection_menu.setEnabled(False)

        # clear stimulus selection menu
        self._stimulus_selection_menu.clear()

    def _init_data_type_selection_interface(self):
        self._data_type_selection_menu.addItem("Gaze")

        # Enable interface
        self._data_type_selection_menu.setEnabled(True)

    def _disable_data_type_selection_interface(self):
        # Disable interface
        self._data_type_selection_menu.setEnabled(False)

        # clear data type selection menu
        self._data_type_selection_menu.clear()

    def _init_analysis_type_selection_interface(self):
        self._analysis_type_selection_menu.addItem("Scatter Plot")

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
        if (hasattr(self, '_canvas')): # if this canvas is not the initial blank canvas
            self._previous_canvas = self._canvas

        self._canvas = PyQt5MPLCanvas(self._plot)
        self._canvas.mpl_connect('button_press_event', self._process_plot_click)

        self._hide_all_widgets()
        if (self._plotting_row_plot.indexOf(self._plot_placeholder) != -1): # if the plot placeholder is still on the display
            self._plotting_row_plot.removeWidget(self._plot_placeholder)
        elif (hasattr(self, '_previous_canvas')): # if this canvas is not the initial blank canvas
            self._plotting_row_plot.removeWidget(self._previous_canvas)
        self._plotting_row_plot.addWidget(self._canvas)
        self._show_all_widgets()

    # Initializes the plot to be displayed
    def _set_plot_from_data(self):
        try:
            self._plot = visual_util._get_gaze_plot(self._data_frame,
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
        if (hasattr(self, '_previous_canvas')): # if this canvas is not the initial blank canvas
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
        if (hasattr(self, '_previous_canvas')): # if this canvas is not the initial blank canvas
            self._previous_canvas.show()
        self._canvas.show()
