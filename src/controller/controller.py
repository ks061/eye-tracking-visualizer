"""
Contains the class Controller

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""


class Controller(object):
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

        self.connect_buttons_to_functions()
        self.setup_static_selection_menus()
        self.load_data()
        self.load_stimuli_menu()
        self.load_participants()

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

    @staticmethod
    def connect_buttons_to_functions() -> None:
        """
        Connects buttons to actions
        """
        ViewStimulusSelection.get_instance().menu.currentIndexChanged.connect(
            lambda: ViewParticipantSelection.get_instance().update_selection_checkboxes()
        )
        ViewParticipantSelection.get_instance().select_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().select_all()
        )
        ViewParticipantSelection.get_instance().deselect_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().deselect_all()
        )
        ViewPlot.get_instance().plot_button.clicked.connect(
            lambda: ControllerPlot.get_instance().process_plot_button_click()
        )
        ViewPlot.get_instance().eps_input_min.returnPressed.connect(
            lambda: ControllerPlot.get_instance().process_eps_input_min_entered()
        )
        ViewPlot.get_instance().eps_input_max.returnPressed.connect(
            lambda: ControllerPlot.get_instance().process_eps_input_max_entered()
        )
        ViewPlot.get_instance().min_samples_input_min.returnPressed.connect(
            lambda: ControllerPlot.get_instance().process_min_samples_input_min_entered()
        )
        ViewPlot.get_instance().min_samples_input_max.returnPressed.connect(
            lambda: ControllerPlot.get_instance().process_min_samples_input_max_entered()
        )
        ViewPlot.get_instance().eps_slider.sliderMoved.connect(
            lambda: ControllerPlot.get_instance().process_eps_slider_moved()
        )
        ViewPlot.get_instance().min_samples_slider.sliderMoved.connect(
            lambda: ControllerPlot.get_instance().process_min_samples_slider_moved()
        )
        ViewPlot.get_instance().eps_slider.sliderReleased.connect(
            lambda: ControllerPlot.get_instance().process_plot_button_click()
        )
        ViewPlot.get_instance().min_samples_slider.sliderReleased.connect(
            lambda: ControllerPlot.get_instance().process_plot_button_click()
        )

    @staticmethod
    def setup_static_selection_menus() -> None:
        """
        Initialize static (non-changing) selection menus
        """
        ViewDataTypeSelection.get_instance().setup()
        ViewAnalysisTypeSelection.get_instance().setup()

    @staticmethod
    def load_data() -> None:
        ModelData.get_instance().update_df()

    @staticmethod
    def load_stimuli_menu() -> None:
        ModelStimulusSelection.get_instance().update_stimuli_from_data_and_dir()
        ViewStimulusSelection.get_instance().setup()

    @staticmethod
    def load_participants() -> None:
        ModelParticipantSelection.get_instance().import_stimuli_filtered_participant_selection()
        ControllerParticipantSelection.get_instance().update_view_selection_participants_from_model()


from src.controller.controller_participant_selection import ControllerParticipantSelection
from src.controller.controller_plot import ControllerPlot
from src.model.model_data import ModelData
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_plot import ViewPlot
from src.view.view_stimulus_selection import ViewStimulusSelection
