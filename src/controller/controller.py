"""
Contains the class Controller
"""

from src.controller.controller_analysis_type_selection import ControllerAnalysisTypeSelection
from src.controller.controller_data_type_selection import ControllerDataTypeSelection
from src.controller.controller_directory_selection import ControllerDirectorySelection
from src.controller.controller_stimulus_selection import ControllerStimulusSelection
from src.model.model_analysis_type_selection import ModelAnalysisTypeSelection
from src.model.model_data_type_selection import ModelDataTypeSelection
from src.model.model_plot import ModelPlot
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_directory_selection import ViewDirectorySelection
from src.view.view_main import ViewMain
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_plot import ViewPlot
from src.view.view_stimulus_selection import ViewStimulusSelection


class Controller:
    """
    Controls operation of application among model and view
    """
    # singleton instance
    __instance = None

    delegator = None

    def __init__(self, delegator):
        if Controller.__instance is not None:
            raise Exception("Controller should be treated as a singleton class.")
        else:
            Controller.__instance = self
        self.delegator = delegator
        self._connect_gui_components_to_functions()
        self._setup_static_selection_menus()

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: Controller
        """
        if Controller.__instance is not None:
            pass
        else:
            raise Exception("Controller has not been instantiated and " + \
                            "cannot be done so without a Delegator object")
        return Controller.__instance

    def _connect_gui_components_to_functions(self):
        ViewDirectorySelection.get_instance().button.clicked.connect(
            lambda: ControllerDirectorySelection.get_instance().process_directory_selection_button_click(self.delegator)
        )
        ViewStimulusSelection.get_instance().menu.activated.connect(
            lambda: ControllerStimulusSelection.get_instance().process_stimulus_selection_menu_change()
        )
        ViewParticipantSelection.get_instance().select_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().process_select_all_button_click()
        )
        ViewParticipantSelection.get_instance().deselect_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().process_deselect_all_button_click()
        )
        ViewDataTypeSelection.get_instance().menu.activated.connect(
            lambda: ControllerDataTypeSelection.get_instance().process_data_type_selection_menu_change()
        )
        ViewAnalysisTypeSelection.get_instance().menu.activated.connect(
            lambda: ControllerAnalysisTypeSelection.get_instance().process_analysis_type_selection_menu_change()
        )
        ViewMain.get_instance().plot_button.clicked.connect(
            lambda: self.process_plot_button_click()
        )
        ViewPlot.get_instance().min_samples_slider.valueChanged.connect(
            lambda: self.process_plot_button_click()
        )

    @staticmethod
    def _setup_static_selection_menus():
        ViewDataTypeSelection.get_instance().setup()
        ViewAnalysisTypeSelection.get_instance().setup()

    @staticmethod
    def _pre_process_plot_button_click_disable():
        ViewMain.get_instance().plot_button.setEnabled(False)

    @staticmethod
    def _post_process_plot_button_click_enable():
        ViewMain.get_instance().plot_button.setEnabled(True)

    def process_plot_button_click(self):
        """
        Processes when the user clicks the plot button,
        updating the internal model of the plot based upon
        user selections and then displaying the updated
        plot
        """
        self._pre_process_plot_button_click_disable()

        ModelStimulusSelection.get_instance().set_selection(
            selection=ViewStimulusSelection.get_instance().get_current_menu_selection()
        )
        ModelDataTypeSelection.get_instance().set_selection(
            selection=ViewDataTypeSelection.get_instance().get_current_menu_selection()
        )
        ModelAnalysisTypeSelection.get_instance().set_selection(
            selection=ViewAnalysisTypeSelection.get_instance().get_current_menu_selection()
        )
        ModelPlot.get_instance().update_fig(
            min_samples=ViewPlot.get_instance().min_samples_slider.value()
        )
        ViewPlot.get_instance().plot(
            min_samples=ViewPlot.get_instance().min_samples_slider.value()
        )

        self._post_process_plot_button_click_enable()
