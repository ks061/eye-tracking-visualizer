"""
Contains the class ViewPlot

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

# External imports
import time

import plotly.graph_objects as go
from PyQt5 import QtWidgets, QtWebEngineWidgets

from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection


class ViewPlot(object):
    """
    View for the plot
    """

    __instance = None

    plot_button = None
    plot_placeholder = None
    eps_input_min = None
    eps_input_max = None
    eps_slider = None
    eps_curr_input = None
    min_samples_input_ma = None,
    min_samples_slider = None
    min_samples_curr_input = None
    support_input = None
    forward_confidence_input = None
    backward_confidence_input = None
    num_trials_monte_carlo_input = None
    run_monte_carlo_button = None
    monte_carlo_progress_bar = None
    time_left_monte_carlo = None

    # initialized in class
    browser = None
    vbox = None
    figure_widget = None

    # plot selections
    saved_stimulus_selection: str = None
    saved_participant_selection: list = None
    saved_data_type_selection: str = None
    saved_analysis_type_selection: str = None
    saved_eps_val: int = None
    saved_min_samples_val: int = None
    saved_support_threshold: int = None
    saved_forward_confidence_threshold: int = None
    saved_backward_confidence_threshold: int = None

    def __init__(self,
                 plot_button,
                 plot_placeholder,
                 eps_input_min,
                 eps_input_max,
                 eps_slider,
                 eps_curr_input,
                 min_samples_input_min,
                 min_samples_input_max,
                 min_samples_slider,
                 min_samples_curr_input,
                 support_input,
                 forward_confidence_input,
                 backward_confidence_input,
                 num_trials_monte_carlo_input,
                 run_monte_carlo_button,
                 monte_carlo_progress_bar,
                 time_left_monte_carlo):
        if ViewPlot.__instance is not None:
            raise Exception("ViewPlot should be treated as a singleton class.")
        else:
            ViewPlot.__instance = self
        self.plot_button = plot_button
        self.plot_placeholder = plot_placeholder
        self.eps_input_min = eps_input_min
        self.eps_input_max = eps_input_max
        self.eps_slider = eps_slider
        self.eps_curr_input = eps_curr_input
        self.min_samples_input_min = min_samples_input_min
        self.min_samples_input_max = min_samples_input_max
        self.min_samples_slider = min_samples_slider
        self.min_samples_curr_input = min_samples_curr_input
        self.support_input = support_input
        self.forward_confidence_input = forward_confidence_input
        self.backward_confidence_input = backward_confidence_input
        self.num_trials_monte_carlo_input = num_trials_monte_carlo_input
        self.run_monte_carlo_button = run_monte_carlo_button
        self.monte_carlo_progress_bar = monte_carlo_progress_bar
        self.time_left_monte_carlo = time_left_monte_carlo

        self.setup()

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewPlot
        """
        if ViewPlot.__instance is None:
            raise Exception("ViewPlot has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewPlot.__instance

    def setup(self) -> None:
        """
        Sets up the layout of the plot-holding
        widget and removes the old layout if
        needed
        """
        self.vbox = QtWidgets.QVBoxLayout(self.plot_placeholder)
        self.browser_refresh()

    def save_curr_plot_selections(self) -> None:
        self.saved_stimulus_selection = ViewStimulusSelection.get_instance().menu.currentText()
        self.saved_participant_selection = ViewParticipantSelection.get_instance().update_selected_checkboxes()
        self.saved_data_type_selection = ViewDataTypeSelection.get_instance().get_selected()
        self.saved_analysis_type_selection = ViewAnalysisTypeSelection.get_instance().get_selected()
        self.saved_eps_val = ModelPlot.get_eps_value()
        self.saved_min_samples_val = ModelPlot.get_min_samples_value()
        self.saved_support_threshold = ViewPlot.get_instance().support_input.value()
        self.saved_forward_confidence_threshold = ViewPlot.get_instance().forward_confidence_input.value()
        self.saved_backward_confidence_threshold = ViewPlot.get_instance().backward_confidence_input.value()

    def are_same_plot_selections(self) -> bool:
        if self.saved_stimulus_selection != ViewStimulusSelection.get_instance().menu.currentText():
            return False
        if self.saved_participant_selection != ViewParticipantSelection.get_instance().update_selected_checkboxes():
            return False
        if self.saved_data_type_selection != ViewDataTypeSelection.get_instance().get_selected():
            return False
        if self.saved_analysis_type_selection != ViewAnalysisTypeSelection.get_instance().get_selected():
            return False
        if self.saved_eps_val != ModelPlot.get_eps_value():
            return False
        if self.saved_min_samples_val != ModelPlot.get_min_samples_value():
            return False
        return True

    def are_same_assoc_rule_threshold_selections(self) -> bool:
        if self.saved_support_threshold != ViewPlot.get_instance().support_input.value():
            return False
        if self.saved_forward_confidence_threshold != ViewPlot.get_instance().forward_confidence_input.value():
            return False
        if self.saved_backward_confidence_threshold != ViewPlot.get_instance().backward_confidence_input.value():
            return False
        return True

    def plot(self) -> None:
        """
        Creates a visualization based upon the given data,
        stimulus, and other menu selections made by the user
        """
        self.browser_refresh()
        if not self.are_same_plot_selections():
            # start_time = time.time()  # profiling plotting
            fig = ModelPlot.get_instance().update_fig()
            # print(time.time() - start_time)
        elif not self.are_same_assoc_rule_threshold_selections():
            # start_time = time.time()  # profiling filtration and displaying on
            # significant association rules
            ModelPlot.get_instance().filter_sig_cluster_assoc_rule_arrows()
            fig = ModelPlot.get_instance().fig
            # print(time.time() - start_time)
        else:
            # start_time = time.time()
            fig = ModelPlot.get_instance().fig
            # print(time.time() - start_time)
        self.figure_widget = go.FigureWidget(fig)
        self.browser.resize(900, 700)
        self.browser.show()
        html_fig = fig.to_html(include_plotlyjs='cdn')
        self.browser.setHtml(html_fig)
        self.save_curr_plot_selections()

    def browser_refresh(self) -> None:
        self.vbox.removeWidget(self.browser)
        self.browser = QtWebEngineWidgets.QWebEngineView(self.plot_placeholder)
        self.vbox.insertWidget(0, self.browser)


from src.model.model_plot import ModelPlot
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_stimulus_selection import ViewStimulusSelection
