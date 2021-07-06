"""
Contains the class ViewParticipantSelection
"""

from PyQt5 import QtWidgets


class ViewParticipantSelection:
    """
    View for the participant selection
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

    selection_check_box_list = None
    selected_check_box_list = None

    def __init__(self,
                 hbox,
                 select_all_button,
                 deselect_all_button,
                 select_deselect_all_hspacer,
                 menu,
                 widget_holder,
                 selection_button):
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

    def show(self):
        """
        Show participant selection menu
        """
        self.select_all_button.show()
        self.deselect_all_button.show()
        self.menu.show()
        self.selection_button.show()

    def hide(self):
        """
        Hide participant selection menu
        """
        self.select_all_button.hide()
        self.deselect_all_button.hide()
        self.menu.hide()
        self.selection_button.hide()

    def process_select_all_button_click(self):
        """
        Select all participants in participant
        selection menu
        """
        for selection_check_box in self.selection_check_box_list:
            selection_check_box.setChecked(True)

    def process_deselect_all_button_click(self):
        """
        Deselect all participants in participant
        selection menu
        """
        for selection_check_box in self.selection_check_box_list:
            selection_check_box.setChecked(False)

    def enable(self):
        """
        Enables the participant selection menu interface
        """
        self.select_all_button.setEnabled(True)
        self.deselect_all_button.setEnabled(True)
        self.menu.setEnabled(True)
        self.selection_button.setEnabled(True)

    def disable(self):
        """
        Disables the participant selection menu interface
        """
        # Disable interface
        self.select_all_button.setEnabled(False)
        self.deselect_all_button.setEnabled(False)
        self.menu.setEnabled(False)
        self.selection_button.setEnabled(False)

    def clear(self):
        """
        Clears the participant selection menu interface
        """
        if self.selection_check_box_list is not None:
            for selection_check_box in self.selection_check_box_list:
                self.layout.removeWidget(selection_check_box)
                selection_check_box.hide()  # necessary for removing checkboxes from
                # old participant list from display once
                # new directory is selected
            self.selection_check_box_list = []

    def _setup_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.widget_holder.setLayout(self.layout)

    def set_selection_check_box_list(self, selection_participant_list):
        """
        Sets the list of participants

        :param selection_participant_list: list of participants
            that can be selected
        :type selection_participant_list: list
        """
        if self.layout is None:
            self._setup_layout()
        # initialize check boxes for selected participants
        self.selection_check_box_list = []
        for participant in selection_participant_list:
            check_box_widget = QtWidgets.QCheckBox()
            check_box_widget.setText(participant)
            self.layout.addWidget(check_box_widget)
            self.selection_check_box_list.append(check_box_widget)

    def update_selected_check_boxes(self):
        """
        Updates the check boxes that are selected
        in the participant selection menu
        """
        self.selected_check_box_list = []
        for check_box in self.selection_check_box_list:
            if check_box.isChecked():
                self.selected_check_box_list.append(check_box)

    def get_selected_check_boxes(self):
        """
        Gets the check boxes that are selected
            in the participant selection menu

        :return: check boxes that are selected
            in the participant selection menu
        :rtype: list
        """
        self.update_selected_check_boxes()
        return self.selected_check_box_list