"""
Contains the class ViewStimulusSelection

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""


class ViewStimulusSelection(object):
    """
    View for the stimulus selected
    """

    __instance = None

    menu = None

    def enable(self) -> None:
        self.menu.setEnabled(True)

    def disable(self) -> None:
        self.menu.setEnabled(False)

    def clear(self) -> None:
        self.menu.clear()

    def get_selected(self) -> str:
        return self.menu.currentText()

    def __init__(self,
                 menu):
        if ViewStimulusSelection.__instance is not None:
            raise Exception("ViewStimulusSelection should be treated as a singleton class.")
        else:
            ViewStimulusSelection.__instance = self
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

    def setup(self) -> None:
        """
        Sets up stimulus selected menu
        """
        # initialize with stimulus options within specified tsv file
        self.menu.clear()
        for stimulus in ModelStimulusSelection.get_instance().update_stimuli_from_data_and_dir():
            self.menu.addItem(str(stimulus))


from src.model.model_stimulus_selection import ModelStimulusSelection
