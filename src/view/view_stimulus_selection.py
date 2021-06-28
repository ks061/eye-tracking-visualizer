"""
Contains the class ViewStimulusSelection
"""
from src.model.model_stimulus_selection import ModelStimulusSelection


class ViewStimulusSelection:
    """
    View for the stimulus selection
    """

    __instance = None

    hbox = None
    label = None
    menu = None

    def __init__(self,
                 hbox,
                 label,
                 menu):
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
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewStimulusSelection
        """
        if ViewStimulusSelection.__instance is None:
            raise Exception("ViewStimulusSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewStimulusSelection.__instance

    def disable(self):
        """
        Disable stimulus selection menu
        """
        # Disable interface
        self.menu.setEnabled(False)

    def clear(self):
        """
        Clear stimulus selection menu
        """
        # clear stimulus selection menu
        self.menu.clear()

    def setup(self):
        """
        Sets up stimulus selection menu
        """
        # initialize with stimulus options within specified tsv file
        self.menu.clear()
        for stimulus in ModelStimulusSelection.get_instance().get_stimuli_names():
            self.menu.addItem(str(stimulus))

    # Initializes the drop down menu to select the stimulus
    # based on stimuli available in the specified tsv file
    def enable(self):
        """
        Enables stimulus selection menu
        """
        # Enable interface
        self.menu.setEnabled(True)

    def update(self):
        """
        Updates stimulus selection menu
        """
        self.disable()
        self.clear()
        self.setup()
        self.enable()

    def get_current_menu_selection(self):
        """
        Returns the current stimulus selection
        :return: Current stimulus selection
        :rtype: str
        """
        return self.menu.currentText()