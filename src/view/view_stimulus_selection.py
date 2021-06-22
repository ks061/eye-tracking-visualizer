import os

from PyQt5 import QtWidgets

from src.view.utils import visual_util


class ViewStimulusSelection:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with selecting
    the background image, i.e. the stimulus, that will
    be displayed as the background of the plot.
    """

    __instance = None

    hbox = None
    label = None
    menu = None

    selection = None

    view_directory_selection = None
    view_participant_selection = None

    def __init__(self,
                 hbox,
                 label,
                 menu,
                 view_directory_selection,
                 view_participant_selection):
        super().__init__()
        if ViewStimulusSelection.__instance is not None:
            raise Exception("ViewStimulusSelection should be treated as a singleton class.")
        else:
            ViewStimulusSelection.__instance = self
        self.hbox = hbox
        self.label = label
        self.menu = menu

        self.view_directory_selection = view_directory_selection
        self.view_participant_selection = view_participant_selection

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewStimulusSelection
        """
        if ViewStimulusSelection.__instance is not None:
            pass
        else:
            raise Exception("ViewStimulusSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewStimulusSelection.__instance

    def show(self):
        # Data type selection
        self.menu.show()

    def hide(self):
        # Data type selection
        self.menu.hide()

    # Initializes the drop down menu to select the stimulus
    # based on stimuli available in the specified tsv file
    def enable(self):
        # Enable interface
        self.menu.setEnabled(True)

    def setup(self):
        # initialize with stimulus options within specified tsv file
        for stimulus in visual_util.get_found_stimuli(
                self.view_participant_selection.get_selected_check_box_list_text(), self.view_directory_selection.path):
            self.menu.addItem(str(stimulus))

    def disable(self):
        # Disable interface
        self.menu.setEnabled(False)

    def clear(self):
        # clear stimulus selection menu
        self.menu.clear()

    def update(self):
        # disconnect stimulus selection from plotting
        try:
            self.menu.currentTextChanged.disconnect()
        except:
            pass

        self.disable()
        self.clear()
        self.setup()
        self.enable()

    def set_selection(self):
        self.selection = self.menu.currentText()

    def get_selection(self):
        return self.selection


