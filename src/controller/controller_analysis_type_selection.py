"""
Contains the class ControllerAnalysisTypeSelection
"""

from src.model.model_analysis_type_selection import ModelAnalysisTypeSelection
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_main import ViewMain


class ControllerAnalysisTypeSelection:
    """
    Controls operation of application functions
    that are related to data type selection
    among model and view
    """
    __instance = None

    def __init__(self):
        if ControllerAnalysisTypeSelection.__instance is not None:
            raise Exception("ControllerAnalysisTypeSelection should be treated as a singleton class.")
        else:
            ControllerAnalysisTypeSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ControllerAnalysisTypeSelection
        """
        if ControllerAnalysisTypeSelection.__instance is None:
            ControllerAnalysisTypeSelection()
        return ControllerAnalysisTypeSelection.__instance

    @staticmethod
    def _pre_process_selection_button_click_disable():
        ViewMain.get_instance().plot_button.setEnabled(False)

    @staticmethod
    def _post_process_selection_button_click_enable():
        ViewMain.get_instance().plot_button.setEnabled(True)

    def process_analysis_type_selection_menu_change(self):
        """
        Processes when the user makes a change in their
        selection within the analysis type selection
        menu, updating the corresponding internal model
        accordingly
        """
        self._pre_process_selection_button_click_disable()

        ModelAnalysisTypeSelection.get_instance().set_selection(
            selection=ViewAnalysisTypeSelection.get_instance().get_current_menu_selection()
        )

        self._post_process_selection_button_click_enable()