"""
Contains the class ModelData

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

# External imports
import os
import pandas as pd

from src.main.config import RELATIVE_DATA_DIR


class ModelData(object):
    """
    Contains pandas DataFrame of data being plotted
    """
    __instance = None

    df = None

    def clear(self) -> None:
        self.df = None

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

    def update_df(self) -> pd.DataFrame:
        """
        Imports all the eye-tracking data
        (of the selected participants) available
        in the specified data directory path
        :return complete data
        :rtype pd.DataFrame
        """
        self.df = pd.concat(
            pd.read_csv(
                os.path.join(
                    RELATIVE_DATA_DIR, participant_filename
                ),
                sep='\t'
            ).assign(participant_filename=participant_filename) \
            for participant_filename in ModelParticipantSelection.get_instance().import_all_participants()
        )
        return self.df


from src.model.model_participant_selection import ModelParticipantSelection
