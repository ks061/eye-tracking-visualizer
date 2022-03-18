"""
Contains the class Delegator

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class Delegator(QMainWindow):
    """
    This class delegates the user interface components loaded in
    from the specified UI file by PyQt5's uic library. It delegates
    them to static wrapper objects that will contain specific
    sets of those components and manage them accordingly.
    """
    # singleton instance
    __instance = None

    # ViewMain components
    main_window = None
    central_widget = None
    plotting_row_hbox = None
    plotting_row_options_vbox = None
    directory_vspacer = None
    bottom_vspacer = None
    plotting_row_plot_vbox = None
    plotting_row_vspacer = None

    # ViewError components
    error_scroll_area = None
    scroll_area_widget_contents = None
    error_message = None

    # ViewStimulusSelection components
    stimulus_hbox = None
    stimulus_label = None
    stimulus_menu = None

    # ViewParticipantSelection components
    participant_select_deselect_all_button_hbox = None
    participant_select_all_button = None
    participant_deselect_all_button = None
    participant_select_deselect_all_hspacer = None
    participant_selection_menu = None
    participant_selection_widget_holder = None

    # ViewDataTypeSelection components
    data_type_hbox = None
    data_type_label = None
    data_type_menu = None

    # ViewAnalysisTypeSelection components
    analysis_type_hbox = None
    analysis_type_label = None
    analysis_type_menu = None

    # ViewPlot components
    plot_placeholder = None
    plot_button = None
    eps_input_min = None
    eps_input_max = None
    eps_slider = None
    eps_curr_input = None
    min_samples_input_min = None
    min_samples_input_max = None
    min_samples_slider = None
    min_samples_curr_input = None
    support_input = None
    forward_confidence_input = None
    backward_confidence_input = None

    def __init__(self):
        super(Delegator, self).__init__()
        if Delegator.__instance is not None:
            raise Exception("Delegator should be treated as a singleton class.")
        else:
            Delegator.__instance = self
        # importing UI components
        self.set_attributes()
        # creating view objects with UI components
        self.create_view_objects()
        # creating controller
        Controller(delegator=self)
        # show main window
        self.show()

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: Delegator
        """
        if Delegator.__instance is not None:
            pass
        else:
            Delegator()
        return Delegator.__instance

    def set_attributes(self) -> None:
        """
        Setting attributes based upon GUI components
        defined in the UI file created by QtDesigner
        """
        curr_file_path = os.path.dirname(os.path.abspath(__file__))
        uic.loadUi(os.path.join(curr_file_path, '../main/app_gui.ui'), self)

    def create_view_objects(self) -> None:
        """
        Initializes the various view objects
        with the relevant GUI components
        """
        # Encapsulating the main window
        ViewMain(
            main_window=self.main_window,
            central_widget=self.central_widget
        )
        # Encapsulating the error displaying UI section
        ViewError(
            message=self.error_message
        )
        # Encapsulating the stimulus selected UI functionality
        ViewStimulusSelection(
            menu=self.stimulus_menu
        )
        # Encapsulating the participation selected UI functionality
        ViewParticipantSelection(
            select_all_button=self.participant_select_all_button,
            deselect_all_button=self.participant_deselect_all_button,
            menu=self.participant_selection_menu,
            widget_holder=self.participant_selection_widget_holder
        )
        # Encapsulating the data type selected UI functionality
        ViewDataTypeSelection(
            menu=self.data_type_menu
        )
        # Encapsulating the analysis type selected UI functionality
        ViewAnalysisTypeSelection(
            menu=self.analysis_type_menu
        )

        # Encapsulating the plot to be displayed in the UI
        ViewPlot(
            plot_button=self.plot_button,
            plot_placeholder=self.plot_placeholder,
            eps_input_min=self.eps_input_min,
            eps_input_max=self.eps_input_max,
            eps_slider=self.eps_slider,
            eps_curr_input=self.eps_curr_input,
            min_samples_input_min=self.min_samples_input_min,
            min_samples_input_max=self.min_samples_input_max,
            min_samples_slider=self.min_samples_slider,
            min_samples_curr_input=self.min_samples_curr_input,
            support_input=self.support_input,
            forward_confidence_input=self.forward_confidence_input,
            backward_confidence_input=self.backward_confidence_input
        )

from src.controller.controller import Controller
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_error import ViewError
from src.view.view_main import ViewMain
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_plot import ViewPlot
from src.view.view_stimulus_selection import ViewStimulusSelection
