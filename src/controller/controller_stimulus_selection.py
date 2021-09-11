"""
Contains the class ControllerStimulusSelection
"""

from src.model.model_data import ModelData
from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.view.view_main import ViewMain
from src.view.view_stimulus_selection import ViewStimulusSelection


class ControllerStimulusSelection:
    """
    Controls operation of application functions
    that are related to stimulus selection
    among model and view
    """
    __instance = None

    def __init__(self):
        if ControllerStimulusSelection.__instance is not None:
            raise Exception("ControllerStimulusSelection should be treated as a singleton class.")
        else:
            ControllerStimulusSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ControllerStimulusSelection
        """
        if ControllerStimulusSelection.__instance is None:
            ControllerStimulusSelection()
        return ControllerStimulusSelection.__instance

    @staticmethod
    def _pre_process_selection_button_click_disable():
        ViewMain.get_instance().plot_button.setEnabled(False)

    @staticmethod
    def _post_process_selection_button_click_enable():
        ViewMain.get_instance().plot_button.setEnabled(True)

    def process_stimulus_selection_menu_change(self):
        """
        Processes when the user makes a change in their
        selection within the stimulus selection
        menu, updating the corresponding internal model
        accordingly
        """
        self._pre_process_selection_button_click_disable()

        ModelStimulusSelection.get_instance().set_selection(
            selection=ViewStimulusSelection.get_instance().get_current_menu_selection()
        )
        ModelData.get_instance().set_df_multi_selected_participants_selected_stimulus(
            data_directory_path=ModelDirectorySelection.get_instance().get_path(),
            selected_participants=ModelParticipantSelection.get_instance().get_selected_participants(),
            selected_stimulus=ModelStimulusSelection.get_instance().get_selection()
        )

        self._post_process_selection_button_click_enable()
