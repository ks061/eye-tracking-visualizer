from PyQt5 import QtWidgets


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
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewParticipantSelection
        """
        if ViewParticipantSelection.__instance is None:
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

    def setup_layout(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.widget_holder.setLayout(self.layout)

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

    def set_selection_check_box_list(self, selection_participant_list):
        if self.layout is None:
            self.setup_layout()
        # initialize check boxes for selected participants
        self.selection_check_box_list = []
        for participant in selection_participant_list:
            check_box_widget = QtWidgets.QCheckBox()
            check_box_widget.setText(participant)
            self.layout.addWidget(check_box_widget)
            self.selection_check_box_list.append(check_box_widget)

    def update_selected_check_box_list(self):
        self.selected_check_box_list = []
        for check_box in self.selection_check_box_list:
            if check_box.isChecked():
                self.selected_check_box_list.append(check_box)

    def get_selected_check_box_list(self):
        self.update_selected_check_box_list()
        return self.selected_check_box_list