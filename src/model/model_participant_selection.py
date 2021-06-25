import glob
import os

from src.model.model_directory_selection import ModelDirectorySelection


class ModelParticipantSelection:
    __instance = None

    selection_participants: list = None
    selected_participants: list = None

    def __init__(self):
        super().__init__()
        if ModelParticipantSelection.__instance is not None:
            raise Exception("ModelParticipantSelection should be treated as a singleton class.")
        else:
            ModelParticipantSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ModelParticipantSelection
        """
        if ModelParticipantSelection.__instance is None:
            ModelParticipantSelection()
        return ModelParticipantSelection.__instance

    def import_selection_participants(self):
        # Import eligible .tsv files
        saved_wd = os.getcwd()
        os.chdir(ModelDirectorySelection.get_instance().get_path())
        self.selection_participants = glob.glob('*.{}'.format('tsv'))
        os.chdir(saved_wd)

    def get_selection_participants(self):
        self.import_selection_participants()
        return self.selection_participants

    def set_selection_participants(self, selection_participants):
        self.selection_participants = selection_participants

    def get_selected_participants(self):
        return self.selected_participants

    def set_selected_participants(self, selected_participants):
        self.selected_participants = selected_participants

    def clear(self):
        self.selection_participants = None
        self.selected_participants = None