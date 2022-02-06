"""
Contains the class ControllerParticipantSelection

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""


class ControllerParticipantSelection(object):
    """
    Controls operation of application functions
    that are related to participant selected
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
    def update_view_selection_participants_from_model() -> None:
        """
        Updates the participant view selected menu based upon
        the available participants, as determined by the
        participant selected model
        """
        ViewParticipantSelection.get_instance().disable()
        ViewParticipantSelection.get_instance().clear()
        ViewParticipantSelection.get_instance().update_selection_checkboxes()
        ViewParticipantSelection.get_instance().enable()

    @staticmethod
    def update_model_selected_participants_from_view() -> list:
        """
        Updates the participant model based upon
        the selected participants within the participant
        selected view
        """
        if ViewParticipantSelection.get_instance().update_selected_checkboxes() is not None:
            ModelParticipantSelection.get_instance().set_selected_participants(
                selected_participants=list(map(lambda check_box: check_box.text(),
                                               ViewParticipantSelection.get_instance().update_selected_checkboxes()))
            )
        return ModelParticipantSelection.get_instance().get_selected_participants()


from src.model.model_participant_selection import ModelParticipantSelection
from src.view.view_participant_selection import ViewParticipantSelection
