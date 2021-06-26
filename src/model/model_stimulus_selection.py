import os

import numpy as np

import src.model.utils.fixation_util as visual_util
from src.main import config

from src.model.model_data import ModelData
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

    # Return a list of stimuli, where each stimulus corresponds to
    # a trial on a participant, from a specified data frame
    # and column title
    def _get_one_stimuli(self, selected_participant_check_box_list_text, data_directory_path):
        ModelData.get_instance().get_data_frame_multiple_participants(
            selected_participant_check_box_list_text,
            data_directory_path)
        data_frame[config.STIMULUS_COL_TITLE].unique()
        return data_frame[col_title].unique()

    # Returns a list of stimuli that whose corresponding images
    # could be found in the stimuli images directory specified
    # in the project configuration file
    def _get_stimuli_list(self, selected_participant_check_box_list_text, data_directory_path, col_title=None):
        if col_title is None:
            col_title = config.STIMULUS_COL_TITLE
        stimuli_list = self.get_stimuli(selected_participant_check_box_list_text, data_directory_path, col_title)
        for stimulus in stimuli_list:
            if str(stimulus) in config.EXCLUDE_STIMULI_LIST:
                stimuli_list = np.delete(stimuli_list, np.argwhere(stimulus))
            elif not self.stimulus_image_exists(str(stimulus)):
                stimuli_list = np.delete(stimuli_list, np.argwhere(stimulus))
        return stimuli_list

    # Returns True if image exists
    def stimulus_image_exists(stimulus_image_file_name):
        return os.path.exists(str(Path.cwd() / config.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_image_file_name))

    # Returns a 2D array with RGB values for each
    # pixel in the specified file_name containing the
    # stimulus image
    def import_stimulus_image(stimulus_image_file_name):
        return plt.imread(str(Path.cwd() / config.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_image_file_name))
