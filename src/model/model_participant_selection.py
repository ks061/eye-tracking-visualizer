"""
Contains the class ModelParticipantSelection
"""


# External imports
import glob
import os

# Internal imports
from src.model.model_directory_selection import ModelDirectorySelection


class ModelParticipantSelection:
    """
    Model for the participant selection
    """
    __instance = None

    selection_participants = None
    selected_participants = None

    def __init__(self):
        if ModelParticipantSelection.__instance is not None:
            raise Exception("ModelParticipantSelection should be treated as a singleton class.")
        else:
            ModelParticipantSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ModelParticipantSelection
        """
        if ModelParticipantSelection.__instance is None:
            ModelParticipantSelection()
        return ModelParticipantSelection.__instance

    def import_selection_participants(self):
        """
        Imports and sets the possible selection of participants
        from the directory specified in ModelDirectorySelection
        """
        # Import eligible .tsv files
        saved_wd = os.getcwd()
        os.chdir(ModelDirectorySelection.get_instance().get_path())
        self.selection_participants = glob.glob('*.{}'.format('tsv'))
        os.chdir(saved_wd)

    def get_selection_participants(self):
        """
        Gets the possible selection of participants

        :return: possible selection of participants
        :rtype: list
        """
        self.import_selection_participants()
        return self.selection_participants

    def set_selection_participants(self, selection_participants):
        """
        Sets the possible selection of participants

        :param selection_participants: possible selection of participants
        :type selection_participants: list
        """
        self.selection_participants = selection_participants

    def get_selected_participants(self):
        """
        Gets the selected participants

        :return: selected participants
        :rtype: list
        """
        return self.selected_participants

    def set_selected_participants(self, selected_participants):
        """
        Sets the selected participants

        :param selected_participants: selected participants
        :type selected_participants: list
        """
        self.selected_participants = selected_participants

    def enforce_exists_selected_participants(self):
        """
        Enforces that the number of selected participants
        is positive

        :raises TypeError: List of selected participant file names is null.
        :raises ValueError: No participants were selected.
        """
        if self.selected_participants is None:
            raise TypeError("List of selected participant file names is null.")
        if len(self.selected_participants) == 0:
            raise ValueError("No participants were selected.")

    def clear(self):
        """
        Clears the participant selection model
        """
        self.selection_participants = None
        self.selected_participants = None