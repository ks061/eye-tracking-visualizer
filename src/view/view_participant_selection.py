import glob
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel

from src.view.utils import visual_util


class ViewParticipantSelection:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with selecting
    the participants of which the data will be plotted.
    """

    __instance = None

    hbox = None
    select_all_button = None
    deselect_all_button = None
    select_deselect_all_hspacer = None

    menu = None
    widget_holder = None
    layout = None
    selection_button = None

    view_directory_selection = None
    delegator = None

    selection_check_box_list = None
    selected_check_box_list = None

    color_palette = None
    scaled_color_palette = None
    color_palette_dict = None

    def __init__(self,
                 hbox,
                 select_all_button,
                 deselect_all_button,
                 select_deselect_all_hspacer,
                 menu,
                 widget_holder,
                 selection_button,
                 view_directory_selection,
                 delegator):
        super().__init__()
        if ViewParticipantSelection.__instance is not None:
            raise Exception("ViewParticipantSelection should be treated as a singleton class.")
        else:
            ViewParticipantSelection.__instance = self

        self.hbox = hbox
        self.select_all_button = select_all_button
        self.deselect_all_button = deselect_all_button
        self.select_deselect_all_hspacer = select_deselect_all_hspacer
        self.menu = menu
        self.widget_holder = widget_holder
        self.selection_button = selection_button
        self.view_directory_selection = view_directory_selection
        self.delegator = delegator

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewParticipantSelection
        """
        if ViewParticipantSelection.__instance is not None:
            pass
        else:
            raise Exception("ViewParticipantSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewParticipantSelection.__instance

    def set_plot_from_data(self):
        pass

    def show(self):
        # Data type selection
        self.select_all_button.show()
        self.deselect_all_button.show()
        self.menu.show()
        self.selection_button.show()

    def hide(self):
        # Data type selection
        self.select_all_button.hide()
        self.deselect_all_button.hide()
        self.menu.hide()
        self.selection_button.hide()

    # Processes the select all button click in the participant selection interface
    def process_select_all_button_click(self):
        for selection_check_box in self.selection_check_box_list:
            selection_check_box.setChecked(True)

    # Processes the deselect all button click in the participant selection interface
    def process_deselect_all_button_click(self):
        for selection_check_box in self.selection_check_box_list:
            selection_check_box.setChecked(False)

    # Initializes the check box selection area to select
    # the participants to view

    def enable(self):
        # Enable interface
        self.select_all_button.setEnabled(True)
        self.deselect_all_button.setEnabled(True)
        self.menu.setEnabled(True)
        self.selection_button.setEnabled(True)

    def setup(self):
        layout = QtWidgets.QVBoxLayout()
        self.widget_holder.setLayout(layout)

        # Import eligible .tsv files
        saved_wd = os.getcwd()
        os.chdir(self.view_directory_selection.get_path())
        participant_file_list = glob.glob('*.{}'.format('tsv'))
        os.chdir(saved_wd)

        # generate white dot
        visual_util.generate_white_dot(self.delegator)

        # initialize check boxes for selected participants
        self.selection_check_box_list = []
        for i in range(len(participant_file_list)):
            check_box_widget = QtWidgets.QCheckBox()
            check_box_widget.setText(participant_file_list[i])
            layout.addWidget(check_box_widget)
            self.selection_check_box_list.append(check_box_widget)

    def disable(self):
        # Disable interface
        self.select_all_button.setEnabled(False)
        self.deselect_all_button.setEnabled(False)
        self.menu.setEnabled(False)
        self.selection_button.setEnabled(False)

    def clear(self):
        if self.selection_check_box_list is not None:
            for selection_check_box in self.selection_check_box_list:
                self.layout.removeWidget(selection_check_box)
                selection_check_box.hide()  # necessary for removing checkboxes from
                # old participant list from display once
                # new directory is selected
            self.selection_check_box_list = []

    def update(self):
        self.disable()
        self.clear()
        self.setup()
        self.enable()

    def get_check_box_list_text(self, check_box_list):
        check_box_list_text = []
        for check_box in check_box_list:
            check_box_list_text.append(check_box.text())
        return check_box_list_text

    def get_selection_check_box_list_text(self):
        return self.get_check_box_list_text(self.selection_check_box_list)

    def get_selected_check_box_list_text(self):
        return self.get_check_box_list_text(self.selected_check_box_list)

    def update_selected_check_box_list(self):
        self.selected_check_box_list = []
        for check_box in self.selection_check_box_list:
            if check_box.isChecked():
                self.selected_check_box_list.append(check_box)

    def reset_check_box_colors(self):
        for check_box in self.selection_check_box_list:
            check_box.setStyleSheet("")