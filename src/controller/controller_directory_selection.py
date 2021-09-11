"""
Contains the class ControllerDirectorySelection
"""

import PyQt5

from src.model.model_data import ModelData
from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.view.view_main import ViewMain
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_stimulus_selection import ViewStimulusSelection


class ControllerDirectorySelection:
    """
    Controls operation of application functions
    that are related to directory selection
    among model and view
    """
    # singleton instance
    __instance = None

    def __init__(self):
        if ControllerDirectorySelection.__instance is not None:
            raise Exception("ControllerDirectorySelection should be treated as a singleton class.")
        else:
            ControllerDirectorySelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ControllerDirectorySelection
        """
        if ControllerDirectorySelection.__instance is None:
            ControllerDirectorySelection()
        return ControllerDirectorySelection.__instance

    @staticmethod
    def _pre_process_selection_button_click_disable():
        ViewMain.get_instance().plot_button.setEnabled(False)
        ViewParticipantSelection.get_instance().disable()
        ViewStimulusSelection.get_instance().disable()

    @staticmethod
    def _post_process_selection_button_click_enable():
        ModelStimulusSelection.get_instance().clear()
        ViewStimulusSelection.get_instance().clear()
        ViewMain.get_instance().plot_button.setEnabled(True)

    def process_directory_selection_button_click(self, delegator):
        """
        Processes when user clicks directory button
        Refreshes participant selection menu
        Disables stimulus selection menu and plot button
        """
        self._pre_process_selection_button_click_disable()

        # noinspection PyUnresolvedReferences
        path = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(delegator.get_instance(),
                                                                    "Select Directory"))
        ModelDirectorySelection.get_instance().set_path(
            path=path
        )
        ModelData.get_instance().import_data(path)
        ModelParticipantSelection.get_instance().selection_participants = \
            ModelData.get_instance().participants

        self._post_process_selection_button_click_enable()
