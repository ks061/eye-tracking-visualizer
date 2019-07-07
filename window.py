# Project libraries
import data_util
import visual_util
import config as CONFIG
from pyqt5_mpl_canvas import PyQt5MPLCanvas

# Data libraries
import pandas as pd
import seaborn as sns

# Matplotlib/PyQt5 libraries
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class Window(QtWidgets.QMainWindow):

    # Constants
    AXES_SELECTION_CHECK_BOX_TEXT = 'Show Axes'
    FILE_SELECTION_BUTTON_TEXT = 'Open File'
    FILE_SELECTION_TEXTBOX_PREFILLED_TEXT = '<filename>.tsv'
    ## Maximum width for GUI components related to plot options
    MAXIMUM_PLOT_OPTIONS_WIDTH = 225
    ## Maximum height for GUI components related to plot options
    MAXIMUM_PLOT_OPTIONS_HEIGHT = 23
    ## Maximum height for the error message bar
    MAXIMUM_ERROR_MESSAGE_BAR_HEIGHT = MAXIMUM_PLOT_OPTIONS_HEIGHT * 2
    ONLY_DATA_ON_STIMULUS_CHECK_BOX_TEXT = 'Only Show Data on Stimulus'
    SELECT_STIMULUS_BUTTON_TEXT = 'Select Stimulus'
    WINDOW_TITLE = 'Eye-Tracking Visualizer'



    # Constructor
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self._main_widget = QtWidgets.QWidget()
        self.setCentralWidget(self._main_widget)
        self._layout = QtWidgets.QVBoxLayout(self._main_widget)

        self._screen_width = screen_width
        self._screen_height = screen_height

        self._init_startup_UI()

    # Initializes the startup interface
    def _init_startup_UI(self):
        # Set window title
        self._title = self.WINDOW_TITLE
        self.setWindowTitle(self._title)

        # Initialize main plotting row
        self._plotting_row = QtWidgets.QHBoxLayout()
        self._layout.addLayout(self._plotting_row)

        # Initialize vertical components of plotting row
        self._plotting_row_options = QtWidgets.QVBoxLayout()
        self._plotting_row.addLayout(self._plotting_row_options)
        self._plotting_row_plot = QtWidgets.QVBoxLayout()
        self._plotting_row.addLayout(self._plotting_row_plot)

        # Initialize plotting row options components

        ## Error message bar
        self._error_message_bar = QtWidgets.QLabel()
        self._error_message_bar.setWordWrap(True)

        ## Initialize file selection textbox
        self._file_selection_textbox = QtWidgets.QTextEdit(self.FILE_SELECTION_TEXTBOX_PREFILLED_TEXT)

        ## Initialize file selection button
        self._file_selection_button = QtWidgets.QPushButton(self.FILE_SELECTION_BUTTON_TEXT)
        self._file_selection_button.clicked.connect(self._process_file_selection_button_click)

        ## Initialize stimulus selection menu
        self._stimulus_selection_menu = QtWidgets.QComboBox()

        ## Initialize stimulus selection button
        self._stimulus_selection_button = QtWidgets.QPushButton(self.SELECT_STIMULUS_BUTTON_TEXT)
        self._stimulus_selection_button.clicked.connect(self._process_stimulus_selection_button_click)

        ## Initialize matplotlib configurations
        self._axes_selection_check_box = QtWidgets.QCheckBox(self.AXES_SELECTION_CHECK_BOX_TEXT)
        self._axes_selection_check_box.setChecked(True)
        self._axes_selection_check_box.stateChanged.connect(self._toggle_axes)
        self._show_axes = self._axes_selection_check_box.isChecked()

        self._only_data_on_stimulus_selection_check_box = QtWidgets.QCheckBox(self.ONLY_DATA_ON_STIMULUS_CHECK_BOX_TEXT)
        self._only_data_on_stimulus_selection_check_box.setChecked(False)
        self._only_data_on_stimulus_selection_check_box.stateChanged.connect(self._toggle_only_data_on_stimulus)
        self._show_only_data_on_stimulus = self._only_data_on_stimulus_selection_check_box.isChecked()

        ## Add plotting row options components to related vertical box
        self._plotting_row_options.addWidget(self._error_message_bar)
        self._plotting_row_options.addWidget(self._file_selection_textbox)
        self._plotting_row_options.addWidget(self._file_selection_button)
        self._plotting_row_options.addWidget(self._stimulus_selection_menu)
        self._plotting_row_options.addWidget(self._stimulus_selection_button)
        self._plotting_row_options.addWidget(self._axes_selection_check_box)
        self._plotting_row_options.addWidget(self._only_data_on_stimulus_selection_check_box)

        ## Set maximum width of plotting row options components
        self._error_message_bar.setFixedWidth(self.MAXIMUM_PLOT_OPTIONS_WIDTH)
        self._file_selection_textbox.setFixedWidth(self.MAXIMUM_PLOT_OPTIONS_WIDTH)
        self._file_selection_button.setFixedWidth(self.MAXIMUM_PLOT_OPTIONS_WIDTH)
        self._stimulus_selection_menu.setFixedWidth(self.MAXIMUM_PLOT_OPTIONS_WIDTH)
        self._stimulus_selection_button.setFixedWidth(self.MAXIMUM_PLOT_OPTIONS_WIDTH)
        self._axes_selection_check_box.setFixedWidth(self.MAXIMUM_PLOT_OPTIONS_WIDTH)
        self._only_data_on_stimulus_selection_check_box.setFixedWidth(self.MAXIMUM_PLOT_OPTIONS_WIDTH)

        ## Set maximum height of plotting row options components
        self._error_message_bar.setFixedHeight(self.MAXIMUM_ERROR_MESSAGE_BAR_HEIGHT)
        self._file_selection_textbox.setFixedHeight(self.MAXIMUM_PLOT_OPTIONS_HEIGHT)
        self._file_selection_button.setFixedHeight(self.MAXIMUM_PLOT_OPTIONS_HEIGHT)
        self._stimulus_selection_menu.setFixedHeight(self.MAXIMUM_PLOT_OPTIONS_HEIGHT)
        self._stimulus_selection_button.setFixedHeight(self.MAXIMUM_PLOT_OPTIONS_HEIGHT)
        self._axes_selection_check_box.setFixedHeight(self.MAXIMUM_PLOT_OPTIONS_HEIGHT)
        self._only_data_on_stimulus_selection_check_box.setFixedHeight(self.MAXIMUM_PLOT_OPTIONS_HEIGHT)

        ## Hide stimulus selection menu and matplotlib configurations
        self._stimulus_selection_menu.hide()
        self._stimulus_selection_button.hide()
        self._axes_selection_check_box.hide()
        self._only_data_on_stimulus_selection_check_box.hide()

        ## Initialize blank plot
        self._init_blank_plot()

        ## Refresh display
        self._define_display()

    # Processes the file selection button click
    @QtCore.pyqtSlot()
    def _process_file_selection_button_click(self):
        tsv_filename = self._file_selection_textbox.toPlainText()
        self._init_stimulus_selection_interface(tsv_filename)

    # Processes the stimulus selection button click
    @QtCore.pyqtSlot()
    def _process_stimulus_selection_button_click(self):
        self._set_plot_from_data()
        self._init_matplotlib_configurations()

    # Processes a click on the plot
    def _process_plot_click(self, event):
        pass

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

        if (hasattr(self, '_previous_canvas')): # if this canvas is not the initial blank canvas
            self._hide_all_widgets()
            self._plotting_row_plot.removeWidget(self._previous_canvas)
        self._plotting_row_plot.addWidget(self._canvas)
        if (hasattr(self, '_previous_canvas')): # if this canvas is not the initial blank canvas
            self._show_all_widgets()

        self._define_display()

    # Initializes the drop down menu to select the stimulus
    # based on stimuli available in the specified tsv file
    def _init_stimulus_selection_interface(self, tsv_filename):
        # import data from specified tsv file
        self._data_frame = data_util._import_data(tsv_filename)

        # clear stimulus selection menu
        self._stimulus_selection_menu.clear()

        # initialize with stimulus options within specified tsv file
        for stimulus in data_util._get_stimuli(self._data_frame):
            if (str(stimulus) not in CONFIG.EXCLUDE_STIMULI_LIST):
                self._stimulus_selection_menu.addItem(str(stimulus))

        # show stimulus selection is not yet shown
        self._stimulus_selection_menu.show()
        self._stimulus_selection_button.show()

    # Displays matplotlib configurations
    def _init_matplotlib_configurations(self):
        self._axes_selection_check_box.show()
        self._only_data_on_stimulus_selection_check_box.show()

    # Initializes the plot to be displayed
    def _set_plot_from_data(self):
        try:
            self._plot = visual_util._get_gaze_plot(self._data_frame,
                                                    self._stimulus_selection_menu.currentText(),
                                                    self._show_axes,
                                                    self._show_only_data_on_stimulus)
            self._error_message_bar.setText('')
            self._set_canvas()
        except FileNotFoundError:
            self._error_message_bar.setText('Stimulus image file ' +
                                    self._stimulus_selection_menu.currentText() +
                                    ' not found.')

    # Refreshes the display
    def _define_display(self):
        # set size policy to fixed
        self._window_width = self.MAXIMUM_PLOT_OPTIONS_WIDTH +\
                             self._canvas.sizeHint().width()
        self._window_height = self._canvas.sizeHint().height()
        # resize window to default dimensions
        self.resize(self._window_width, self._window_height)
        self.setMinimumWidth(self._window_width)
        self.setMaximumWidth(self._window_width)
        self.setMinimumHeight(self._window_height)
        self.setMaximumHeight(self._window_height)
        # move window to top left corner of screen
        self.setGeometry(0, 0, self.geometry().width(), self.geometry().height())

    # Toggles showing of axes in plot
    def _toggle_axes(self, state):
        if (state == QtCore.Qt.Checked):
            self._show_axes = True
        else:
            self._show_axes = False
        self._set_plot_from_data()

    # Toggles showing only data on stimulus
    def _toggle_only_data_on_stimulus(self, state):
        if (state == QtCore.Qt.Checked):
            self._show_only_data_on_stimulus = True
        else:
            self._show_only_data_on_stimulus = False
        self._set_plot_from_data()

    # Hides all widgets
    def _hide_all_widgets(self):
        self._file_selection_textbox.hide()
        self._file_selection_button.hide()
        self._stimulus_selection_menu.hide()
        self._stimulus_selection_button.hide()
        self._axes_selection_check_box.hide()
        self._only_data_on_stimulus_selection_check_box.hide()
        self._canvas.hide()
        if (hasattr(self, '_previous_canvas')):
            self._previous_canvas.hide()

    # Shows all widgets
    def _show_all_widgets(self):
        self._file_selection_textbox.show()
        self._file_selection_button.show()
        self._stimulus_selection_menu.show()
        self._stimulus_selection_button.show()
        self._axes_selection_check_box.show()
        self._only_data_on_stimulus_selection_check_box.show()
        self._canvas.show()
        if (hasattr(self, '_previous_canvas')):
            self._previous_canvas.show()
