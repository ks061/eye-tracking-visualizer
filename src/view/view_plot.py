import os

from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.express as px

from src.main import config
from src.model.utils import data_util
from src.view.utils import visual_util
from src.view.view_directory_selection import ViewDirectorySelection


class ViewPlot:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with
    displaying the plot plotted by the
    application.
    """

    __instance = None

    placeholder = None
    browser = None
    vbox = None

    view_directory_selection = None
    view_participant_selection = None
    view_stimulus_selection = None
    view_data_type_selection = None
    view_analysis_type_selection = None
    view_plot_config_selection = None

    # canvas = None
    # previous_canvas = None
    # plot = None

    def __init__(self,
                 placeholder,
                 view_directory_selection,
                 view_participant_selection,
                 view_stimulus_selection,
                 view_data_type_selection,
                 view_analysis_type_selection,
                 view_plot_config_selection):
        super().__init__()
        if ViewPlot.__instance is not None:
            raise Exception("ViewPlot should be treated as a singleton class.")
        else:
            ViewPlot.__instance = self
        self.placeholder = placeholder
        self.view_directory_selection = view_directory_selection
        self.view_participant_selection = view_participant_selection
        self.view_stimulus_selection = view_stimulus_selection
        self.view_data_type_selection = view_data_type_selection
        self.view_analysis_type_selection = view_analysis_type_selection
        self.view_plot_config_selection = view_plot_config_selection

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewPlot
        """
        if ViewPlot.__instance is not None:
            pass
        else:
            raise Exception("ViewPlot has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewPlot.__instance

    def setup(self):
        self.browser = QtWebEngineWidgets.QWebEngineView(self.placeholder)
        self.vbox = QtWidgets.QVBoxLayout(self.placeholder)
        self.vbox.addWidget(self.browser)

    def plot(self):
        df = data_util.get_data_frame_multiple_participants(
            self.view_participant_selection.get_selected_check_box_list_text(),
            self.view_directory_selection.path
        )
        fig = px.scatter(
            df,
            x=config.X_GAZE_COL_TITLE,
            y=config.Y_GAZE_COL_TITLE
        )
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def show(self):
        # Plot
        self.plot_placeholder.show()
        if hasattr(self, 'previous_canvas'):  # if this canvas is not the initial blank canvas
            pass
            # self.previous_canvas.show()
        self.canvas.show()

    def hide(self):
        # Plot
        self.plot_placeholder.hide()
        if hasattr(self, '_previous_canvas'):  # if this canvas is not the initial blank canvas
            self.previous_canvas.hide()
        self.canvas.hide()