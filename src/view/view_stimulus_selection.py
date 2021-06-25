import os

from PyQt5 import QtWidgets

from src.model.model_directory_selection import ModelDirectorySelection
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.view.utils import visual_util
from src.view.view_directory_selection import ViewDirectorySelection
from src.view.view_participant_selection import ViewParticipantSelection


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

    def __init__(self,
                 hbox,
                 label,
                 menu):
        super().__init__()
        if ViewStimulusSelection.__instance is not None:
            raise Exception("ViewStimulusSelection should be treated as a singleton class.")
        else:
            ViewStimulusSelection.__instance = self
        self.hbox = hbox
        self.label = label
        self.menu = menu

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewStimulusSelection
        """
        if ViewStimulusSelection.__instance is None:
            raise Exception("ViewStimulusSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewStimulusSelection.__instance

    def disable(self):
        # Disable interface
        self.menu.setEnabled(False)

    def clear(self):
        # clear stimulus selection menu
        self.menu.clear()

    def setup(self):
        # initialize with stimulus options within specified tsv file
        for stimulus in ModelStimulusSelection.get_instance().get_stimuli_names():
            self.menu.addItem(str(stimulus))

    # Initializes the drop down menu to select the stimulus
    # based on stimuli available in the specified tsv file
    def enable(self):
        # Enable interface
        self.menu.setEnabled(True)

    def update(self):
        self.disable()
        self.clear()
        self.setup()
        self.enable()

    def get_current_menu_selection(self):
        return self.menu.currentText()