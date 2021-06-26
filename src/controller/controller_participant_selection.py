from src.model.model_participant_selection import ModelParticipantSelection
from src.view.view_participant_selection import ViewParticipantSelection


class ControllerParticipantSelection:
    __instance = None

    def __init__(self):
        super().__init__()
        if ControllerParticipantSelection.__instance is not None:
            raise Exception("ControllerParticipantSelection should be treated as a singleton class.")
        else:
            ControllerParticipantSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ControllerParticipantSelection
        """
        if ControllerParticipantSelection.__instance is None:
            ControllerParticipantSelection()
        return ControllerParticipantSelection.__instance

    @staticmethod
    def update_view_selection_participants_from_model():
        ViewParticipantSelection.get_instance().disable()
        ViewParticipantSelection.get_instance().set_selection_check_box_list(
            ModelParticipantSelection.get_instance().get_selection_participants()
        )
        ViewParticipantSelection.get_instance().enable()

    @staticmethod
    def update_model_selected_participants_from_view():
        ModelParticipantSelection.get_instance().set_selected_participants(
            list(map(lambda check_box: check_box.text(),
                     ViewParticipantSelection.get_instance().get_selected_check_box_list()))
        )
