"""
Contains the class ModelParticipantSelection

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

# External imports
import glob
import os

from src.main.config import RELATIVE_DATA_DIR
from src.main.config import STIMULUS_COL_TITLE


class ModelParticipantSelection(object):
    """
    Model for the participant selected
    """
    __instance = None

    all_participants: list = None
    stimulus_filtered_participants: list = None
    selected_participants: list = None

    def set_selected_participants(self, selected_participants: list) -> None:
        self.selected_participants = selected_participants

    def get_selected_participants(self) -> list:
        return self.selected_participants

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

    def import_all_participants(self) -> list:
        """
        Imports and stores all participants
        from the eye-tracking data directory

        :return: all participants
        :rtype: list
        """
        saved_wd = os.getcwd()
        os.chdir(RELATIVE_DATA_DIR)
        self.all_participants = glob.glob('*.{}'.format('tsv'))
        self.all_participants = sorted(self.all_participants)
        os.chdir(saved_wd)
        return self.all_participants

    def import_stimuli_filtered_participant_selection(self) -> list:
        if self.all_participants is None:
            self.import_all_participants()

        df = ModelData.get_instance().df
        df = df[df[STIMULUS_COL_TITLE] == ViewStimulusSelection.get_instance().get_selected()]

        self.stimulus_filtered_participants = df['participant_filename'].unique()
        return self.stimulus_filtered_participants


from src.model.model_data import ModelData
from src.view.view_stimulus_selection import ViewStimulusSelection
