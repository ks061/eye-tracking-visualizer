"""
Contains the class ModelStimulusSelection
"""

# External imports
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Internal imports
from src.main import config


class ModelStimulusSelection:
    """
    Model for the stimulus selection
    """
    __instance = None

    stimuli_names = None
    selection = None

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

    def update_stimuli_names(self,
                             data):
        """
        Updates the list of available stimuli
        based upon the stimuli across the observations
        across the selected participants

        :param data: eye-tracking data
        :type data: pd.DataFrame
        """
        self.stimuli_names = self.get_existing_stimuli(data)

    def get_stimuli_names(self):
        """
        Get the list of available stimuli

        :return: available stimuli
        :rtype: str
        """
        return self.stimuli_names

    def set_selection(self, selection):
        """
        Sets the selected stimulus

        :param selection: selected stimulus
        :type selection: str
        """
        self.selection = selection

    def get_selection(self):
        """
        Gets the selected stimulus

        :return: selected stimulus
        :rtype: str
        """
        return self.selection

    def clear(self):
        """
        Clears the selected stimulus
        """
        self.selection = None

    # Return a list of stimuli, where each stimulus corresponds to
    # a trial on a participant, from a specified data frame
    # and column title
    @staticmethod
    def get_stimuli_from_data(data,
                              stimulus_col_title=None):
        """
        Returns a list of stimuli from a pandas DataFrame
        containing eye-tracking data across
        a set of participants (removing any
        undefined, i.e. np.nan, values)

        :param data: eye-tracking data
        :type data: pd.DataFrame
        :param stimulus_col_title: column title in DataFrame
            that holds the stimulus names
        :type stimulus_col_title: str
        :return: list of stimulus names
        :rtype: list
        """
        if stimulus_col_title is None:
            stimulus_col_title = config.STIMULUS_COL_TITLE
        stimuli = data[stimulus_col_title].unique()
        return stimuli[~(pd.isnull(stimuli))]

    # Returns a list of stimuli that whose corresponding images
    # could be found in the stimuli images directory specified
    # in the project configuration file
    def get_existing_stimuli(self,
                             data,
                             stimulus_col_title=None,
                             stimulus_dir=None):
        """
        Returns a list of stimuli that are within the specified
        eye-tracking data and could be found within the stimulus
        images directory

        :param data: eye-tracking data
        :type data: pd.DataFrame
        :param stimulus_col_title: column title in DataFrame
            containing eye-tracking data
        :type stimulus_col_title: str
        :param stimulus_dir: directory containing stimuli
        :type stimulus_dir: str
        :return: list of stimuli names
        :rtype: list
        """
        if stimulus_col_title is None:
            stimulus_col_title = config.STIMULUS_COL_TITLE
        if stimulus_dir is None:
            stimulus_dir = config.RELATIVE_STIMULUS_IMAGE_DIRECTORY
        # get stimuli found in the stimulus directory
        stimuli = self.get_stimuli_from_data(data, stimulus_col_title)
        # filter found stimuli for those that
        # are existing in the stimulus directory
        for stimulus in stimuli:
            if stimulus in config.EXCLUDE_STIMULI_LIST:
                stimuli = np.delete(stimuli, np.argwhere(stimulus))
            elif not self.stimulus_image_exists(stimulus, stimulus_dir):
                stimuli = np.delete(stimuli, np.argwhere(stimulus))
        return stimuli

    @staticmethod
    def stimulus_image_exists(stimulus_name,
                              stimulus_relative_dir=None):
        """
        Returns True if the specified filename exists
        in the stimuli directory

        :param stimulus_name: filename of stimulus
        :type stimulus_name: str
        :param stimulus_relative_dir: directory specified to contain
            the stimulus images
        :type stimulus_relative_dir: str
        :return: True if specified filename exists in
            the stimuli directory
        :rtype: bool
        """
        if stimulus_relative_dir is None:
            stimulus_relative_dir = config.RELATIVE_STIMULUS_IMAGE_DIRECTORY
        return os.path.exists(
            str(os.path.dirname(os.path.realpath(__file__)) + \
                stimulus_relative_dir + \
                stimulus_name)
        )

    @staticmethod
    def import_stimulus_image(stimulus_name,
                              stimulus_relative_dir=None):
        """
        Returns a 2D array with RGB values for
        the specified stimulus in the specified
        directory containing the stimulus

        :param stimulus_name: filename of the stimulus
        :type stimulus_name: str
        :param stimulus_relative_dir: directory containing the stimulus
        :type stimulus_relative_dir: str
        :return: 2D array of RGB values of stimulus
        :rtype: np.array
        """
        if stimulus_relative_dir is None:
            stimulus_relative_dir = config.RELATIVE_STIMULUS_IMAGE_DIRECTORY
        return plt.imread(
            str(os.path.dirname(os.path.realpath(__file__)) + "/" + \
                stimulus_relative_dir + "/" + \
                stimulus_name)
        )
