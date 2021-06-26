"""
Imports
"""
# External
import pandas as pd
# Internal
from src.main import config as config
from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_stimulus_selection import ModelStimulusSelection


class ModelData:
    """
    Contains pandas DataFrame of data being plotted
    """
    __instance = None

    df = None

    def __init__(self):
        """
        Initializes the model as a singleton
        """
        if ModelData.__instance is not None:
            raise Exception("ModelData should be treated as a singleton class.")
        else:
            ModelData.__instance = self

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance
        :return: the singleton instance
        """
        if ModelData.__instance is None:
            ModelData()
        return ModelData.__instance

    def get_df(self):
        """
        Returns the data contained in the model for participants in
        ModelParticipantSelection and stimulus in ModelStimulusSelection
        :return: data
        :return type
        """
        self.set_df_multi_participants_selected_stimulus()
        return self.df

    def clear(self):
        """
        Clears the data contained in the model
        """
        # noinspection PyTypeChecker
        self.df = None

    # Return a data frame based on data for a particular participant
    # from a specified .tsv file
    @staticmethod
    def get_df_one_participant_all_stimuli(selected_participant_file_name):
        """
        :param selected_participant_file_name: participant of which data will be retrieved
        :return data
        :rtype: pd.DataFrame
        """
        # additional variables being used
        data_directory_path = ModelDirectorySelection.get_instance().get_path()
        selected_participant_file_path = str(data_directory_path + "/" + selected_participant_file_name)

        return pd.read_csv(selected_participant_file_path, sep='\t')

    # Filter out rows with empty values in any of the columns specified.
    @staticmethod
    def remove_incomplete_observations(df, col_names):
        for col_name in col_names:
            df = df[df[col_name].notnull()]
        return df

    # Return a data frame based on data for multiple participants
    # from multiple specified .tsv files within the
    # selected_participant_file_name_list array. Optional parameter
    # stimulus_file_name to filter by a particular stimulus.
    def get_df_multi_participants_all_stimuli(self):
        # additional variable used
        # noinspection PyUnusedLocal
        df_one_participant_no_stimulus = None
        df_multi_participants_all_stimulus = None
        selected_participant_file_name_list = ModelParticipantSelection.get_instance().get_selected_participants()

        # obtain data frame for each participant
        for i in range(len(selected_participant_file_name_list)):
            selected_participant_file_name = selected_participant_file_name_list[i]
            df_one_participant_no_stimulus = self.get_df_one_participant_all_stimuli(selected_participant_file_name)

            df_one_participant_no_stimulus = df_one_participant_no_stimulus.assign(
                participant_identifier=selected_participant_file_name
            )
            # stack data frame from each participant
            if i == 0:
                df_multi_participants_all_stimulus = df_one_participant_no_stimulus
            else:
                df_multi_participants_all_stimulus = pd.concat([
                    df_multi_participants_all_stimulus,
                    df_one_participant_no_stimulus]
                )

        df_multi_participants_all_stimulus.reset_index(inplace=True)
        return df_multi_participants_all_stimulus

    def set_df_multi_participants_no_stimulus(self):
        self.df = self.get_df_multi_participants_all_stimuli()

    def get_df_multi_participants_selected_stimulus(self):
        df_one_participant_selected_stimulus = self.get_df_multi_participants_all_stimuli()
        return df_one_participant_selected_stimulus.loc[
            df_one_participant_selected_stimulus[config.STIMULUS_COL_TITLE] == \
            ModelStimulusSelection.get_instance().get_selection()
            ]

    def set_df_multi_participants_selected_stimulus(self):
        self.df = self.get_df_multi_participants_selected_stimulus()
