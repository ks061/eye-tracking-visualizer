"""
Contains the class ControllerDataTypeSelection
"""

from src.model.model_data_type_selection import ModelDataTypeSelection
from src.view.view_main import ViewMain
from src.view.view_stimulus_selection import ViewStimulusSelection


class ControllerDataTypeSelection:
    """
    Controls operation of application functions
    that are related to data type selection
    among model and view
    """
    __instance = None

    def __init__(self):
        if ControllerDataTypeSelection.__instance is not None:
            raise Exception("ControllerDataTypeSelection should be treated as a singleton class.")
        else:
            ControllerDataTypeSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ControllerDataTypeSelection
        """
        if ControllerDataTypeSelection.__instance is None:
            ControllerDataTypeSelection()
        return ControllerDataTypeSelection.__instance

    @staticmethod
    def process_data_type_selection_menu_change():
        """
        Processes when the user makes a change in their
        selection within the data type selection
        menu, updating the corresponding internal model
        accordingly
        """
        ViewMain.get_instance().plot_button.setEnabled(False)
        ModelDataTypeSelection.get_instance().set_selection(
            selection=ViewStimulusSelection.get_instance().get_current_menu_selection()
        )
        ViewMain.get_instance().plot_button.setEnabled(True)