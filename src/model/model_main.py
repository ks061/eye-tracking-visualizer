from src.model.model_participant_selection import ModelParticipantSelection
from src.model.utils import data_util
from src.view.view_directory_selection import ViewDirectorySelection
from src.view.view_participant_selection import ViewParticipantSelection


class ModelMain:

    __instance = None

    df = None

    def __init__(self):
        super().__init__()
        if ModelMain.__instance is not None:
            raise Exception("ModelMain should be treated as a singleton class.")
        else:
            ModelMain.__instance = self
        self.df = data_util.get_data_frame_multiple_participants(
            ModelParticipantSelection.get_instance().get_selected_participants(),
            ViewDirectorySelection.get_instance().path
        )

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