import os

import PyQt5
import seaborn as sns

from src.view.utils import visual_util


class Controller:
    # singleton instance
    __instance = None

    # initializing controller
    delegator = None

    # View objects
    view_main = None
    view_error = None
    view_directory_selection = None
    view_participant_selection = None
    view_stimulus_selection = None
    view_data_type_selection = None
    view_analysis_type_selection = None
    view_plot_config_selection = None
    view_plot = None

    def __init__(self, delegator):
        super().__init__()
        if Controller.__instance is not None:
            raise Exception("Controller should be treated as a singleton class.")
        else:
            Controller.__instance = self
        self.delegator = delegator
        self.init_view_objects()
        self.connect_gui_components_to_functions()

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

    def init_view_objects(self):
        self.view_main = self.delegator.view_main
        self.view_error = self.delegator.view_error
        self.view_directory_selection = self.delegator.view_directory_selection
        self.view_participant_selection = self.delegator.view_participant_selection
        self.view_stimulus_selection = self.delegator.view_stimulus_selection
        self.view_data_type_selection = self.delegator.view_data_type_selection
        self.view_analysis_type_selection = self.delegator.view_analysis_type_selection
        self.view_plot_config_selection = self.delegator.view_plot_config_selection
        self.view_plot = self.delegator.view_plot

    def connect_gui_components_to_functions(self):
        self.view_directory_selection.button.clicked.connect(
            lambda: self.process_directory_selection_button_click()
        )
        self.view_participant_selection.select_all_button.clicked.connect(
            lambda: self.view_participant_selection.process_select_all_button_click()
        )
        self.view_participant_selection.deselect_all_button.clicked.connect(
            lambda: self.view_participant_selection.process_deselect_all_button_click()
        )
        self.view_participant_selection.selection_button.clicked.connect(
            lambda: self.process_participant_selection_button_click()
        )
        self.view_stimulus_selection.menu.activated.connect(
            lambda: self.process_stimulus_selection_menu_change()
        )
        self.view_data_type_selection.menu.activated.connect(
            lambda: self.process_data_type_selection_menu_change()
        )
        self.view_analysis_type_selection.menu.activated.connect(
            lambda: self.process_analysis_type_selection_menu_change()
        )
        self.view_main.plot_button.clicked.connect(
            lambda: self.process_plot_button_click()
        )

    # Processes the directory selection button click
    def process_directory_selection_button_click(self):
        # disable/clear latter setup options
        self.view_participant_selection.disable()
        self.view_stimulus_selection.disable()
        self.view_data_type_selection.disable()
        self.view_analysis_type_selection.disable()
        self.view_plot_config_selection.disable()

        path = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self.delegator, "Select Directory"))
        self.view_directory_selection.set_path(
            path
        )
        self.view_participant_selection.update()

    # Processes the participant selection button click
    def process_participant_selection_button_click(self):
        # disable/clear latter setup options
        self.view_stimulus_selection.disable()
        self.view_data_type_selection.disable()
        self.view_analysis_type_selection.disable()
        self.view_plot_config_selection.disable()

        self.view_participant_selection.update_selected_check_box_list()

        # Participants selected with check marks; now, time to update
        # the colors to the left of the participant selection menu.

        # First, reset previous assignment of color palette
        self.view_participant_selection.reset_check_box_colors()
        # generate color palette
        self.view_participant_selection.color_palette = \
            sns.color_palette(
                n_colors=len(
                    self.view_participant_selection.selection_check_box_list
                )
            )
        self.view_participant_selection.scaled_color_palette = \
            visual_util.scale_palette(
                self.view_participant_selection.color_palette
            )
        self.view_participant_selection.color_palette_dict = {}
        # assigning color palette
        for i, check_box in zip(
                range(len(self.view_participant_selection.selected_check_box_list)),
                self.view_participant_selection.selected_check_box_list
        ):
            colored_dot_image_path = visual_util.generate_colored_dot(
                scaled_color=self.view_participant_selection.scaled_color_palette[i],
                id_num=i,
                qmainwindow=self.delegator
            )
            check_box.setStyleSheet(
                "QCheckBox::indicator:checked {image: url(" + colored_dot_image_path + ");}"
            )
            self.view_participant_selection.color_palette_dict[check_box.text()] = \
                self.view_participant_selection.color_palette[i]

        if len(self.view_participant_selection.selected_check_box_list) != 0:
            self.view_error.message.setText('')

            self.view_stimulus_selection.enable()
        else:
            self.view_error.message.setText(
                "No participants selected. Please select at least one participant" +
                " to refresh the plot area"
            )

        self.view_stimulus_selection.update()

    def process_stimulus_selection_menu_change(self):
        # disable/clear latter setup options
        self.view_data_type_selection.disable()
        self.view_analysis_type_selection.disable()
        self.view_plot_config_selection.disable()

        self.view_stimulus_selection.set_selection()

        # enable next option
        self.view_data_type_selection.update()

    def process_data_type_selection_menu_change(self):
        # disable/clear latter setup options
        self.view_analysis_type_selection.disable()
        self.view_plot_config_selection.disable()

        self.view_data_type_selection.set_selection()

        # enable next option
        self.view_analysis_type_selection.update()

    def process_analysis_type_selection_menu_change(self):
        self.view_plot_config_selection.disable()

        self.view_analysis_type_selection.set_selection()

        self.view_plot_config_selection.enable()

    def process_plot_button_click(self):
        self.view_plot.setup()
        self.view_plot.plot()
