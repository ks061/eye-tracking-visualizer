import pandas as pd

from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.model.utils import data_util


class ModelMain:

    __instance = None

    df: pd.DataFrame = None

    def __init__(self):
        super().__init__()
        if ModelMain.__instance is not None:
            raise Exception("ModelMain should be treated as a singleton class.")
        else:
            ModelMain.__instance = self
        self._update_df()

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ModelMain
        """
        if ModelMain.__instance is None:
            ModelMain()
        return ModelMain.__instance

    def _update_df(self):
        self.df = data_util.get_data_frame_multiple_participants(
            selected_participant_file_name_list=ModelParticipantSelection.get_instance().get_selected_participants(),
            data_directory_path=ModelDirectorySelection.get_instance().path,
            stimulus_file_name=ModelStimulusSelection.get_instance().get_selection()
        )

    def get_df(self):
        self._update_df()
        return self.df

    def clear(self):
        self.df = None