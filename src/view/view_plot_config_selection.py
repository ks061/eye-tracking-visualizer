import os

from PyQt5 import QtWidgets

from src.view.view_directory_selection import ViewDirectorySelection


class ViewPlotConfigSelection:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with selecting
    the plotting configurations for the plotting that
    the application will do.
    """

    __instance = None

    vbox = None
    axes_selection_check_box = None
    only_data_on_stimulus_selection_check_box = None

    def __init__(self,
                 vbox,
                 axes_selection_check_box,
                 only_data_on_stimulus_selection_check_box):
        super().__init__()
        if ViewPlotConfigSelection.__instance is not None:
            raise Exception("ViewPlotConfigSelection should be treated as a singleton class.")
        else:
            ViewPlotConfigSelection.__instance = self
        self.vbox = vbox
        self.axes_selection_check_box = axes_selection_check_box
        self.only_data_on_stimulus_selection_check_box = only_data_on_stimulus_selection_check_box

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewPlotConfigSelection
        """
        if ViewPlotConfigSelection.__instance is not None:
            pass
        else:
            raise Exception("ViewPlotConfigSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewPlotConfigSelection.__instance

    def show(self):
        self.axes_selection_check_box.show()
        self.only_data_on_stimulus_selection_check_box.show()

    def hide(self):
        self.axes_selection_check_box.hide()
        self.only_data_on_stimulus_selection_check_box.hide()

    # Displays matplotlib configurations
    def enable(self):
        # Enable interface
        self.axes_selection_check_box.setEnabled(True)
        self.only_data_on_stimulus_selection_check_box.setEnabled(True)

    # Disables matplotlib configurations
    def disable(self):
        # Disable interface
        self.axes_selection_check_box.setEnabled(False)
        self.only_data_on_stimulus_selection_check_box.setEnabled(False)

    def axes_on_selected(self):
        return self.axes_selection_check_box.isChecked()

    def only_show_data_on_stimulus(self):
        return self.only_data_on_stimulus_selection_check_box.isChecked()