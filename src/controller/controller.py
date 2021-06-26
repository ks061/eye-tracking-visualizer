import PyQt5

import src.controller.delegator as delegator
from src.controller.controller_participant_selection import ControllerParticipantSelection
from src.model.model_analysis_type_selection import ModelAnalysisTypeSelection
from src.model.model_data_type_selection import ModelDataTypeSelection
from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_main import ModelMain
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_plot import ModelPlot
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_directory_selection import ViewDirectorySelection
from src.view.view_error import ViewError
from src.view.view_main import ViewMain
from src.view.view_participant_selection import ViewParticipantSelection
from src.view.view_plot import ViewPlot
from src.view.view_stimulus_selection import ViewStimulusSelection


class Controller:
    # singleton instance
    __instance = None

    delegator = None

    # Sub Controllers
    controller_participant_selection = None

    def __init__(self):
        super().__init__()
        if Controller.__instance is not None:
            raise Exception("Controller should be treated as a singleton class.")
        else:
            Controller.__instance = self
        ViewMain.get_instance().plot_button.setEnabled(False)
        self._connect_gui_components_to_functions()
        self._setup_static_selection_menus()

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of Controller
        """
        if Controller.__instance is not None:
            pass
        else:
            raise Exception("Controller has not been instantiated and " + \
                            "cannot be done so without a Delegator object")
        return Controller.__instance

    def _connect_gui_components_to_functions(self):
        ViewDirectorySelection.get_instance().button.clicked.connect(
            lambda: self.process_directory_selection_button_click()
        )
        ViewParticipantSelection.get_instance().select_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().process_select_all_button_click()
        )
        ViewParticipantSelection.get_instance().deselect_all_button.clicked.connect(
            lambda: ViewParticipantSelection.get_instance().process_deselect_all_button_click()
        )
        ViewParticipantSelection.get_instance().selection_button.clicked.connect(
            lambda: self.process_participant_selection_button_click()
        )
        ViewStimulusSelection.get_instance().menu.activated.connect(
            lambda: self.process_stimulus_selection_menu_change()
        )
        ViewDataTypeSelection.get_instance().menu.activated.connect(
            lambda: self.process_data_type_selection_menu_change()
        )
        ViewAnalysisTypeSelection.get_instance().menu.activated.connect(
            lambda: self.process_analysis_type_selection_menu_change()
        )
        ViewMain.get_instance().plot_button.clicked.connect(
            lambda: self.process_plot_button_click()
        )

    @staticmethod
    def _setup_static_selection_menus():
        ViewDataTypeSelection.get_instance().setup()
        ViewAnalysisTypeSelection.get_instance().setup()

    @staticmethod
    # Processes the directory selection button click
    def process_directory_selection_button_click():
        # disable/clear latter setup options
        ViewMain.get_instance().plot_button.setEnabled(False)
        ViewParticipantSelection.get_instance().disable()
        ModelParticipantSelection.get_instance().clear()
        ViewStimulusSelection.get_instance().disable()
        ModelStimulusSelection.get_instance().clear()

        path = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(delegator.Delegator.get_instance(), "Select Directory"))
        ModelDirectorySelection.get_instance().set_path(
            path
        )
        ControllerParticipantSelection.update_view_selection_participants_from_model()

    @staticmethod
    # Processes the participant selection button click
    def process_participant_selection_button_click():
        # disable/clear latter setup options
        ViewMain.get_instance().plot_button.setEnabled(False)
        ViewStimulusSelection.get_instance().disable()
        ModelStimulusSelection.get_instance().clear()

        ControllerParticipantSelection.get_instance().update_model_selected_participants_from_view()

        # Participants selected with check marks; now, time to update
        # the colors to the left of the participant selection menu.

        if len(ViewParticipantSelection.get_instance().selected_check_box_list) != 0:
            ViewError.get_instance().message.setText('')

            ModelStimulusSelection.get_instance().update_stimuli_names()
            ViewStimulusSelection.get_instance().update()
        else:
            ViewError.get_instance().message.setText(
                "No participants selected. Please select at least one participant" +
                " to refresh the plot area"
            )

    @staticmethod
    def process_stimulus_selection_menu_change():
        ViewMain.get_instance().plot_button.setEnabled(True)

    @staticmethod
    def process_data_type_selection_menu_change():
        pass

    @staticmethod
    def process_analysis_type_selection_menu_change():
        pass

    @staticmethod
    def process_plot_button_click():
        ModelStimulusSelection.get_instance().set_selection(
            ViewStimulusSelection.get_instance().get_current_menu_selection()
        )
        ModelDataTypeSelection.get_instance().set_selection(
            ViewDataTypeSelection.get_instance().get_current_menu_selection()
        )
        ModelAnalysisTypeSelection.get_instance().set_selection(
            ViewAnalysisTypeSelection.get_instance().get_current_menu_selection()
        )
        ModelPlot.get_instance().update_fig()
        ViewPlot.get_instance().plot()
