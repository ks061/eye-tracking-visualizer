from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

from src.controller.controller import Controller
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_directory_selection import ViewDirectorySelection
from src.view.view_error import ViewError
from src.view.view_main import ViewMain
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_plot import ViewPlot
from src.view.view_plot_config_selection import ViewPlotConfigSelection
from src.view.view_stimulus_selection import ViewStimulusSelection


class Delegator(QMainWindow):
    """
    This class delegates the user interface components loaded in
    from the specified UI file by PyQt5's uic library. It delegates
    them to static wrapper objects that will contain specific
    sets of those components and manage them accordingly.
    """
    # singleton instance
    __instance = None

    # View objects
    view_main = None
    view_error = None
    view_directory_selection = None
    view_participant_selection = None
    view_stimulus_selection = None
    view_data_type_selection = None
    view_analysis_type_selection = None
    view_plot_config_selection = None
    view_plot = None

    # ViewMain components
    main_window = None
    central_widget = None
    plotting_row_hbox = None
    plotting_row_options_vbox = None
    directory_vspacer = None
    plot_button = None
    bottom_vspacer = None
    plotting_row_plot_vbox = None
    plotting_row_vspacer = None

    # ViewError components
    error_scroll_area = None
    scroll_area_widget_contents = None
    error_message = None

    # ViewDirectory components
    directory_button = None

    # ViewParticipantSelection components
    participant_select_deselect_all_button_hbox = None
    participant_select_all_button = None
    participant_deselect_all_button = None
    participant_select_deselect_all_hspacer = None
    participant_selection_menu = None
    participant_selection_widget_holder = None
    participant_selection_button = None

    # ViewStimulusSelection components
    stimulus_hbox = None
    stimulus_label = None
    stimulus_menu = None

    # ViewDataTypeSelection components
    data_type_hbox = None
    data_type_label = None
    data_type_menu = None

    # ViewAnalysisTypeSelection components
    analysis_type_hbox = None
    analysis_type_label = None
    analysis_type_menu = None

    # ViewPlotConfigSelection components
    plot_config_selection_vbox = None
    axes_selection_check_box = None
    only_data_on_stimulus_selection_check_box = None

    # ViewPlot components
    plot_placeholder = None

    def __init__(self):
        super().__init__()
        if Delegator.__instance is not None:
            raise Exception("Delegator should be treated as a singleton class.")
        else:
            Delegator.__instance = self
        # importing UI components
        self.set_attributes()
        # self.set_main_window_attributes()
        # self.set_other_component_attributes()
        # creating view objects with UI components
        self.create_view_objects()
        # creating controller
        Controller(self)
        # show main window
        self.show()

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of Delegator
        """
        if Delegator.__instance is not None:
            pass
        else:
            Delegator()
        return Delegator.__instance

    def set_attributes(self):
        uic.loadUi('app_gui.ui', self)

    def create_view_objects(self):
        # Encapsulating the main window
        self.view_main = ViewMain(
            main_window=self.main_window,
            central_widget=self.central_widget,
            plotting_row_hbox=self.plotting_row_hbox,
            plotting_row_options_vbox=self.plotting_row_options_vbox,
            directory_vspacer=self.directory_vspacer,
            plot_button=self.plot_button,
            bottom_vspacer=self.bottom_vspacer,
            plotting_row_plot_vbox=self.plotting_row_plot_vbox,
            plotting_row_vspacer=self.plotting_row_vspacer
        )
        # Encapsulating the error displaying UI section
        self.view_error = ViewError(
            scroll_area=self.error_scroll_area,
            scroll_area_widget_contents=self.scroll_area_widget_contents,
            message=self.error_message
        )
        # Encapsulating the directory selection UI functionality
        self.view_directory_selection = ViewDirectorySelection(
            button=self.directory_button
        )
        # Encapsulating the participation selection UI functionality
        self.view_participant_selection = ViewParticipantSelection(
            hbox=self.participant_select_deselect_all_button_hbox,
            select_all_button=self.participant_select_all_button,
            deselect_all_button=self.participant_deselect_all_button,
            select_deselect_all_hspacer=self.participant_select_deselect_all_hspacer,
            menu=self.participant_selection_menu,
            widget_holder=self.participant_selection_widget_holder,
            selection_button=self.participant_selection_button,
            view_directory_selection=self.view_directory_selection,
            delegator=self
        )
        # Encapsulating the stimulus selection UI functionality
        self.view_stimulus_selection = ViewStimulusSelection(
            hbox=self.stimulus_hbox,
            label=self.stimulus_label,
            menu=self.stimulus_menu,
            view_directory_selection=self.view_directory_selection,
            view_participant_selection=self.view_participant_selection
        )
        # Encapsulating the data type selection UI functionality
        self.view_data_type_selection = ViewDataTypeSelection(
            hbox=self.data_type_hbox,
            label=self.data_type_label,
            menu=self.data_type_menu
        )
        # Encapsulating the analysis type selection UI functionality
        self.view_analysis_type_selection = ViewAnalysisTypeSelection(
            hbox=self.analysis_type_hbox,
            label=self.analysis_type_label,
            menu=self.analysis_type_menu
        )
        # Encapsulating the plotting config UI functionality
        self.view_plot_config_selection = ViewPlotConfigSelection(
            vbox=self.plot_config_selection_vbox,
            axes_selection_check_box=self.axes_selection_check_box,
            only_data_on_stimulus_selection_check_box=self.only_data_on_stimulus_selection_check_box
        )
        # Encapsulating the plot to be displayed in the UI
        self.view_plot = ViewPlot(
            placeholder=self.plot_placeholder,
            view_directory_selection=self.view_directory_selection,
            view_participant_selection=self.view_participant_selection,
            view_stimulus_selection=self.view_stimulus_selection,
            view_data_type_selection=self.view_data_type_selection,
            view_analysis_type_selection=self.view_analysis_type_selection,
            view_plot_config_selection=self.view_plot_config_selection
        )