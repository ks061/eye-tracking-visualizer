import os

import PyQt5
import seaborn as sns

import src.controller.delegator as delegator
from src.controller.controller_participant_selection import ControllerParticipantSelection

from src.view.utils import visual_util
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_directory_selection import ViewDirectorySelection
from src.view.view_error import ViewError
from src.view.view_main import ViewMain
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_plot import ViewPlot
from src.view.view_plot_config_selection import ViewPlotConfigSelection
from src.view.view_stimulus_selection import ViewStimulusSelection


class Controller:
    # singleton instance
    __instance = None

    delegator = None

    # Sub Controllers
    controller_participant_selection = None

    def __init__(self):
        super().__init__()
        if Controller.__instance is not None:
            raise Exception("Controller should be treated as a singleton class.")
        else:
            Controller.__instance = self
        self._connect_gui_components_to_functions()

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of Controller
        """
        if Controller.__instance is not None:
            pass
        else:
            raise Exception("Controller has not been instantiated and " + \
                            "cannot be done so without a Delegator object")
        return Controller.__instance

    def _connect_gui_components_to_functions(self):
        ViewDirectorySelection.get_instance().button.clicked.connect(
            lambda: self.process_directory_selection_button_click()
        )
        ViewParticipantSelection.get_instance().select_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().process_select_all_button_click()
        )
        ViewParticipantSelection.get_instance().deselect_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().process_deselect_all_button_click()
        )
        ViewParticipantSelection.get_instance().selection_button.clicked.connect(
            lambda: self.process_participant_selection_button_click()
        )
        ViewStimulusSelection.get_instance().menu.activated.connect(
            lambda: self.process_stimulus_selection_menu_change()
        )
        ViewDataTypeSelection.get_instance().menu.activated.connect(
            lambda: self.process_data_type_selection_menu_change()
        )
        ViewAnalysisTypeSelection.get_instance().menu.activated.connect(
            lambda: self.process_analysis_type_selection_menu_change()
        )
        ViewMain.get_instance().plot_button.clicked.connect(
            lambda: self.process_plot_button_click()
        )

    @staticmethod
    # Processes the directory selection button click
    def process_directory_selection_button_click():
        # disable/clear latter setup options
        ViewParticipantSelection.get_instance().disable()
        ViewStimulusSelection.get_instance().disable()
        ViewDataTypeSelection.get_instance().disable()
        ViewAnalysisTypeSelection.get_instance().disable()
        ViewPlotConfigSelection.get_instance().disable()

        path = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(delegator.Delegator.get_instance(), "Select Directory"))
        ViewDirectorySelection.get_instance().set_path(
            path
        )
        ControllerParticipantSelection.update_view_selection_participants_from_model()

    @staticmethod
    # Processes the participant selection button click
    def process_participant_selection_button_click():
        # disable/clear latter setup options
        ViewStimulusSelection.get_instance().disable()
        ViewDataTypeSelection.get_instance().disable()
        ViewAnalysisTypeSelection.get_instance().disable()
        ViewPlotConfigSelection.get_instance().disable()

        ControllerParticipantSelection.get_instance().update_model_selected_participants_from_view()

        # Participants selected with check marks; now, time to update
        # the colors to the left of the participant selection menu.

        if len(ViewParticipantSelection.get_instance().selected_check_box_list) != 0:
            ViewError.get_instance().message.setText('')

            ViewStimulusSelection.get_instance().enable()
        else:
            ViewError.get_instance().message.setText(
                "No participants selected. Please select at least one participant" +
                " to refresh the plot area"
            )
        ViewStimulusSelection.get_instance().update()

    @staticmethod
    def process_stimulus_selection_menu_change():
        # disable/clear latter setup options
        ViewDataTypeSelection.get_instance().disable()
        ViewAnalysisTypeSelection.get_instance().disable()
        ViewPlotConfigSelection.get_instance().disable()

        ViewStimulusSelection.get_instance().set_selection()

        # enable next option
        ViewDataTypeSelection.get_instance().update()

    @staticmethod
    def process_data_type_selection_menu_change():
        # disable/clear latter setup options
        ViewAnalysisTypeSelection.get_instance().disable()
        ViewPlotConfigSelection.get_instance().disable()

        ViewDataTypeSelection.get_instance().set_selection()

        # enable next option
        ViewAnalysisTypeSelection.get_instance().update()

    @staticmethod
    def process_analysis_type_selection_menu_change():
        ViewPlotConfigSelection.get_instance().disable()

        ViewAnalysisTypeSelection.get_instance().set_selection()

        ViewPlotConfigSelection.get_instance().enable()

    @staticmethod
    def process_plot_button_click():
        ViewPlot.get_instance().setup()
        ViewPlot.get_instance().plot()
