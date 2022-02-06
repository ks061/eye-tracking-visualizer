"""
Contains the class ViewParticipantSelection

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

from PyQt5 import QtWidgets


class ViewParticipantSelection(object):
    """
    View for the participant selected
    """

    __instance = None

    menu = None
    select_all_button = None
    deselect_all_button = None
    widget_holder = None

    # initialized within class
    layout = None
    selection_checkbox_list = None
    selected_checkbox_list = None

    def select_all(self) -> None:
        for selection_checkbox in self.selection_checkbox_list:
            selection_checkbox.setChecked(True)

    def deselect_all(self) -> None:
        for selection_checkbox in self.selection_checkbox_list:
            selection_checkbox.setChecked(False)

    def __init__(self,
                 select_all_button,
                 deselect_all_button,
                 menu,
                 widget_holder):
        if ViewParticipantSelection.__instance is not None:
            raise Exception("ViewParticipantSelection should be treated as a singleton class.")
        else:
            ViewParticipantSelection.__instance = self

        self.select_all_button = select_all_button
        self.deselect_all_button = deselect_all_button
        self.menu = menu
        self.widget_holder = widget_holder

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewParticipantSelection
        """
        if ViewParticipantSelection.__instance is None:
            raise Exception("ViewParticipantSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewParticipantSelection.__instance

    def setup_layout(self) -> None:
        self.layout = QtWidgets.QVBoxLayout()
        self.widget_holder.setLayout(self.layout)

    def update_selection_checkboxes(self) -> list:
        """
        Sets the list of participants

        :return: list of selection checkboxes
        """
        self.clear()
        if self.layout is None:
            self.setup_layout()
        # initialize check boxes for selected participants
        self.selection_checkbox_list = []
        for participant in ModelParticipantSelection.get_instance().import_stimuli_filtered_participant_selection():
            checkbox_widget = QtWidgets.QCheckBox()
            checkbox_widget.setText(participant)
            self.layout.addWidget(checkbox_widget)
            self.selection_checkbox_list.append(checkbox_widget)
        return self.selection_checkbox_list

    def update_selected_checkboxes(self) -> list:
        """
        Updates the checkboxes that are selected
        in the participant selected menu

        :return: list of selected checkboxes
        """
        self.selected_checkbox_list = []
        for checkbox in self.selection_checkbox_list:
            if checkbox.isChecked():
                self.selected_checkbox_list.append(checkbox)
        return self.selected_checkbox_list

    def enable(self) -> None:
        """
        Enables the participant selected menu interface
        """
        self.select_all_button.setEnabled(True)
        self.deselect_all_button.setEnabled(True)
        self.menu.setEnabled(True)

    def disable(self) -> None:
        """
        Disables the participant selected menu interface
        """
        # Disable interface
        self.select_all_button.setEnabled(False)
        self.deselect_all_button.setEnabled(False)
        self.menu.setEnabled(False)

    def clear(self) -> None:
        """
        Clears the participant selected menu interface
        """
        if self.selection_checkbox_list is not None:
            for selection_checkbox in self.selection_checkbox_list:
                self.layout.removeWidget(selection_checkbox)
                selection_checkbox.hide()  # necessary for removing checkboxes from
                # old participant list from display once
                # new directory is selected
            self.selection_checkbox_list = []


from src.model.model_participant_selection import ModelParticipantSelection
