import src.view.utils.visual_util as visual_util

from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_participant_selection import ModelParticipantSelection


class ModelStimulusSelection:

    __instance = None

    stimuli_names: list = None
    selection: str = None

    def __init__(self):
        super().__init__()
        if ModelStimulusSelection.__instance is not None:
            raise Exception("ModelStimulusSelection should be treated as a singleton class.")
        else:
            ModelStimulusSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ModelStimulusSelection
        """
        if ModelStimulusSelection.__instance is None:
            ModelStimulusSelection()
        return ModelStimulusSelection.__instance

    def update_stimuli_names(self):
        self.stimuli_names = visual_util.get_found_stimuli(
            ModelParticipantSelection.get_instance().get_selected_participants(),
            ModelDirectorySelection.get_instance().get_path()
        )

    def get_stimuli_names(self):
        return self.stimuli_names

    def set_selection(self, selection):
        self.selection = selection

    def get_selection(self):
        return self.selection

    def clear(self):
        self.selection = None
