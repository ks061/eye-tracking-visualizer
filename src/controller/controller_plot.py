"""
Contains the class Controller

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""
from src.view.view_monte_carlo_cluster_p_values import ViewMonteCarloClusterPValues


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
        # ModelPlot.get_instance().update_fig() # already updated in ViewPlot.get_instance().plot()
        ViewPlot.get_instance().plot()

    @staticmethod
    def process_eps_input_min_entered() -> None:
        eps_input_min_val = ViewPlot.get_instance().eps_input_min.value()
        eps_input_min_val = 1 if eps_input_min_val <= 0 else eps_input_min_val
        if ViewPlot.get_instance().eps_curr_input.value() < eps_input_min_val:
            ViewPlot.get_instance().eps_curr_input.setValue(eps_input_min_val)
            ControllerPlot.process_eps_input_curr_entered()
        ViewPlot.get_instance().eps_input_min.setValue(eps_input_min_val)
        ViewPlot.get_instance().eps_slider.setMinimum(eps_input_min_val)

    @staticmethod
    def process_eps_input_curr_entered() -> None:
        eps_input_curr_val = ViewPlot.get_instance().eps_curr_input.value()
        eps_input_curr_val = 1 if eps_input_curr_val <= 0 else eps_input_curr_val
        ViewPlot.get_instance().eps_curr_input.setValue(eps_input_curr_val)
        if eps_input_curr_val < ViewPlot.get_instance().eps_input_min.value():
            ViewPlot.get_instance().eps_input_min.setValue(eps_input_curr_val)
            ControllerPlot.process_eps_input_min_entered()
        if eps_input_curr_val > ViewPlot.get_instance().eps_input_max.value():
            ViewPlot.get_instance().eps_input_max.setValue(eps_input_curr_val)
            ControllerPlot.process_eps_input_max_entered()
        ViewPlot.get_instance().eps_slider.setValue(eps_input_curr_val)

    @staticmethod
    def process_eps_input_max_entered() -> None:
        eps_input_max_val = ViewPlot.get_instance().eps_input_max.value()
        eps_input_max_val = 1 if eps_input_max_val <= 0 else eps_input_max_val
        if ViewPlot.get_instance().eps_curr_input.value() > eps_input_max_val:
            ViewPlot.get_instance().eps_curr_input.setValue(eps_input_max_val)
            ControllerPlot.process_eps_input_curr_entered()
        ViewPlot.get_instance().eps_input_max.setValue(eps_input_max_val)
        ViewPlot.get_instance().eps_slider.setMaximum(eps_input_max_val)

    @staticmethod
    def process_min_samples_input_min_entered() -> None:
        min_samples_input_min_val = ViewPlot.get_instance().min_samples_input_min.value()
        min_samples_input_min_val = 1 if min_samples_input_min_val <= 0 else min_samples_input_min_val
        if ViewPlot.get_instance().min_samples_curr_input.value() < min_samples_input_min_val:
            ViewPlot.get_instance().min_samples_curr_input.setValue(min_samples_input_min_val)
            ControllerPlot.process_min_samples_input_curr_entered()
        ViewPlot.get_instance().min_samples_input_min.setValue(min_samples_input_min_val)
        ViewPlot.get_instance().min_samples_slider.setMinimum(min_samples_input_min_val)

    @staticmethod
    def process_min_samples_input_curr_entered() -> None:
        min_samples_input_curr_val = ViewPlot.get_instance().min_samples_curr_input.value()
        min_samples_input_curr_val = 1 if min_samples_input_curr_val <= 0 else min_samples_input_curr_val
        ViewPlot.get_instance().min_samples_curr_input.setValue(min_samples_input_curr_val)
        if min_samples_input_curr_val < ViewPlot.get_instance().min_samples_input_min.value():
            ViewPlot.get_instance().min_samples_input_min.setValue(min_samples_input_curr_val)
            ControllerPlot.process_min_samples_input_min_entered()
        if min_samples_input_curr_val > ViewPlot.get_instance().min_samples_input_max.value():
            ViewPlot.get_instance().min_samples_input_max.setValue(min_samples_input_curr_val)
            ControllerPlot.process_min_samples_input_max_entered()
        ViewPlot.get_instance().min_samples_slider.setValue(min_samples_input_curr_val)

    @staticmethod
    def process_min_samples_input_max_entered() -> None:
        min_samples_input_max_val = ViewPlot.get_instance().min_samples_input_max.value()
        min_samples_input_max_val = 1 if min_samples_input_max_val <= 0 else min_samples_input_max_val
        if ViewPlot.get_instance().min_samples_curr_input.value() > min_samples_input_max_val:
            ViewPlot.get_instance().min_samples_curr_input.setValue(min_samples_input_max_val)
            ControllerPlot.process_min_samples_input_curr_entered()
        ViewPlot.get_instance().min_samples_input_max.setValue(min_samples_input_max_val)
        ViewPlot.get_instance().min_samples_slider.setMaximum(min_samples_input_max_val)

    @staticmethod
    def process_eps_slider_moved() -> None:
        ViewPlot.get_instance().eps_curr_input.setValue(
            ViewPlot.get_instance().eps_slider.value()
        )

    @staticmethod
    def process_min_samples_slider_moved() -> None:
        ViewPlot.get_instance().min_samples_curr_input.setValue(
            ViewPlot.get_instance().min_samples_slider.value()
        )

    @staticmethod
    def process_run_monte_carlo_button_clicked() -> None:
        ModelPlot.get_instance().run_monte_carlo_stimulation()
        ViewMonteCarloClusterPValues.get_instance().show()

from src.controller.controller_participant_selection import ControllerParticipantSelection
from src.model.model_plot import ModelPlot
from src.view.view_plot import ViewPlot
