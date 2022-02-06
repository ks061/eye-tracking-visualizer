"""
Contains the class Controller

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""


class ControllerPlot(object):
    """
    Controls operation of application functions
    that are related to data type selected
    among model and view
    """
    __instance = None

    def __init__(self):
        if ControllerPlot.__instance is not None:
            raise Exception("ControllerPlot should be treated as a singleton class.")
        else:
            ControllerPlot.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ControllerPlot
        """
        if ControllerPlot.__instance is None:
            ControllerPlot()
        return ControllerPlot.__instance

    @staticmethod
    def process_plot_button_click() -> None:
        """
        Processes when the user clicks the plot button,
        updating the internal model of the plot based upon
        user selections and then displaying the updated
        plot
        """
        ControllerParticipantSelection.get_instance().update_model_selected_participants_from_view()
        ModelData.get_instance().update_df()
        ModelPlot.get_instance().update_fig(
            min_samples=ViewPlot.get_instance().min_samples_slider.value()
        )
        ViewPlot.get_instance().plot(
            min_samples=ViewPlot.get_instance().min_samples_slider.value()
        )


from src.controller.controller_participant_selection import ControllerParticipantSelection
from src.model.model_data import ModelData
from src.model.model_plot import ModelPlot
from src.view.view_plot import ViewPlot
