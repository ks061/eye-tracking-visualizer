"""
Contains the class ControllerParticipantSelection
"""

from src.model.model_data import ModelData
from src.model.model_data_type_selection import ModelDataTypeSelection
from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.view.view_error import ViewError
from src.view.view_main import ViewMain
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_stimulus_selection import ViewStimulusSelection


class ControllerParticipantSelection:
    """
    Controls operation of application functions
    that are related to participant selection
    among model and view
    """
    __instance = None

    def __init__(self):
        if ControllerParticipantSelection.__instance is not None:
            raise Exception("ControllerParticipantSelection should be treated as a singleton class.")
        else:
            ControllerParticipantSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ControllerParticipantSelection
        """
        if ControllerParticipantSelection.__instance is None:
            ControllerParticipantSelection()
        return ControllerParticipantSelection.__instance

    @staticmethod
    def update_view_selection_participants_from_model():
        """
        Updates the participant view selection menu based upon
        the available participants, as determined by the
        participant selection model
        """
        ViewParticipantSelection.get_instance().disable()
        ViewParticipantSelection.get_instance().clear()
        ViewParticipantSelection.get_instance().set_selection_check_box_list(
            selection_participant_list=ModelParticipantSelection.get_instance().get_selection_participants()
        )
        ViewParticipantSelection.get_instance().enable()

    @staticmethod
    def update_model_selected_participants_from_view():
        """
        Updates the participant model based upon
        the selected participants within the participant
        selection view
        """
        ModelParticipantSelection.get_instance().set_selected_participants(
            selected_participants=list(map(lambda check_box: check_box.text(),
                                           ViewParticipantSelection.get_instance().get_selected_check_boxes()))
        )

    @staticmethod
    def process_participant_selection_button_click():
        """
        Updates stimulus selection based on participant selection
        """
        # disable/clear latter setup options
        ViewMain.get_instance().plot_button.setEnabled(False)
        ViewStimulusSelection.get_instance().disable()
        ModelStimulusSelection.get_instance().clear()

        ControllerParticipantSelection.get_instance().update_model_selected_participants_from_view()

        if len(ViewParticipantSelection.get_instance().selected_check_box_list) != 0:
            ViewError.get_instance().message.setText('')
            ModelData.get_instance().set_df_multi_selected_participants_all_stimuli(
                data_directory_path=ModelDirectorySelection.get_instance().get_path(),
                selected_participants=ModelParticipantSelection.get_instance().get_selected_participants()
            )
            ModelStimulusSelection.get_instance().update_stimuli_names(
                data=ModelData.get_instance().get_df()
            )
            ViewStimulusSelection.get_instance().update()
            ModelDataTypeSelection.get_instance().set_selection(
                selection=ViewStimulusSelection.get_instance().get_current_menu_selection()
            )
        else:
            ViewError.get_instance().message.setText(
                "No participants selected. Please select at least one participant" +
                " to refresh the plot area"
            )

        # enable
        ViewMain.get_instance().plot_button.setEnabled(True)