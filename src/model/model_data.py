"""
Contains the class ModelData
"""

# External imports
import pandas as pd
# Internal imports
from src.main import config as config


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
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ModelData
        """
        if ModelData.__instance is None:
            ModelData()
        return ModelData.__instance

    def get_df(self):
        """
        Returns the data contained in the model

        :return: data
        :rtype: pd.DataFrame
        """
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
    def get_df_one_participant_all_stimuli(data_directory_path,
                                           selected_participant):
        """
        Returns a pandas DataFrame containing eye-tracking data
        from the participant filename specified

        :param data_directory_path: directory path containing eye-tracking data
        :type data_directory_path: str
        :param selected_participant: participant of which data will be retrieved
        :type selected_participant: str
        :return data
        :rtype: pd.DataFrame
        """
        # additional variables being used
        selected_participant_file_path = str(data_directory_path + "/" + selected_participant)

        return pd.read_csv(selected_participant_file_path, sep='\t')

    @staticmethod
    def remove_incomplete_observations(df, col_names):
        """
        Removes any observations from the specified pandas
        DataFrame that have an unspecified
        value in any of the specified columns

        :param df: target DataFrame
        :type df: pd.DataFrame
        :param col_names: target columns in target DataFrame
        :type col_names: list
        :return: result DataFrame
        :rtype: pd.DataFrame
        """
        for col_name in col_names:
            df = df[df[col_name].notnull()]
        return df

    # Return a data frame based on data for multiple participants
    # from multiple specified .tsv files within the
    # selected_participant_file_name_list array. Optional parameter
    # stimulus_file_name to filter by a particular stimulus.
    def get_df_multi_selected_participants_all_stimuli(self,
                                                       data_directory_path,
                                                       selected_participants):
        """
        Returns a pandas DataFrame containing eye-tracking data
        from the selected participants' eye-tracking data files
        (inclusive of all stimuli present in the data)

        :return: selected participants' eye-tracking data
        :rtype: pd.DataFrame
        """
        # additional variable used
        # noinspection PyUnusedLocal
        df_one_participant_no_stimulus = None
        df_multi_participants_all_stimulus = None

        # obtain data frame for each participant
        for i in range(len(selected_participants)):
            selected_participant_file_name = selected_participants[i]
            df_one_participant_no_stimulus = self.get_df_one_participant_all_stimuli(
                selected_participants,
                data_directory_path
            )

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

    def set_df_multi_selected_participants_no_stimulus(self,
                                                       data_directory_path,
                                                       selected_participants):
        """
        Sets the model's stored DataFrame as a pandas
        DataFrame containing eye-tracking data from
        the selected participants' eye-tracking data files
        (inclusive of all stimuli present in the data)
        """
        self.df = self.get_df_multi_selected_participants_all_stimuli(
            data_directory_path=data_directory_path,
            selected_participants=selected_participants
        )

    def get_df_multi_selected_participants_selected_stimulus(self,
                                                             data_directory_path,
                                                             selected_participants,
                                                             selected_stimulus):
        """
        Returns a pandas DataFrame containing eye-tracking data
        from the selected participants' eye-tracking data files
        for a particular stimulus
        (inclusive of all stimuli present in the data)

        :return: selected participants' eye-tracking data for
        a particular stimulus
        :rtype: pd.DataFrame
        """
        df_one_participant_selected_stimulus = self.get_df_multi_selected_participants_all_stimuli(
            data_directory_path=data_directory_path,
            selected_participants=selected_participants
        )
        return df_one_participant_selected_stimulus.loc[
            df_one_participant_selected_stimulus[config.STIMULUS_COL_TITLE] == \
            selected_stimulus
            ]

    def set_df_multi_selected_participants_selected_stimulus(self,
                                                             data_directory_path,
                                                             selected_participants,
                                                             selected_stimulus):
        """
        Sets the model's stored DataFrame as a pandas
        DataFrame containing eye-tracking data
        from the selected participants' eye-tracking
        data files for a particular stimulus
        (inclusive of all stimuli present in the data)
        """
        self.df = self.get_df_multi_selected_participants_selected_stimulus(
            data_directory_path=data_directory_path,
            selected_participants=selected_participants,
            selected_stimulus=selected_stimulus
        )