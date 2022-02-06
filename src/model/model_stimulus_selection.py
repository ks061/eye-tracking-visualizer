"""
Contains the class ModelStimulusSelection

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

# External imports
import numpy as np
import pandas as pd

from src.main.config import EXCLUDE_STIMULI_LIST
from src.main.config import STIMULUS_COL_TITLE

class ModelStimulusSelection(object):
    """
    Model for the stimulus selected
    """
    __instance = None

    stimuli_names = None

    def __init__(self):
        super(ModelStimulusSelection, self).__init__()
        if ModelStimulusSelection.__instance is not None:
            raise Exception("ModelStimulusSelection should be treated as a singleton class.")
        else:
            ModelStimulusSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ModelStimulusSelection
        """
        if ModelStimulusSelection.__instance is None:
            ModelStimulusSelection()
        return ModelStimulusSelection.__instance

    def update_stimuli_from_data_and_dir(self) -> list:
        """
        Returns and updates a list of stimuli names that are within the specified
        eye-tracking data and could be found within the stimulus images directory

        :return: list of stimuli names
        :rtype: list
        """
        stimuli_names = ModelData.get_instance().update_df()[STIMULUS_COL_TITLE].unique()
        stimuli_names = stimuli_names[~(pd.isnull(stimuli_names))]

        # filter found stimuli_names for those that
        # are existing in the stimulus directory
        for stimulus in stimuli_names:
            if stimulus in EXCLUDE_STIMULI_LIST:
                stimuli_names = np.delete(stimuli_names, np.argwhere(stimulus))
            elif not imgutils.img_exists(stimulus):
                stimuli_names = np.delete(stimuli_names, np.argwhere(stimulus))

        self.stimuli_names = stimuli_names
        return stimuli_names


import src.model.utils.img_utils as imgutils
from src.model.model_data import ModelData
