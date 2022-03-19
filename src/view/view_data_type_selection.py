"""
Contains the class ViewDataTypeSelection

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""


class ViewDataTypeSelection(object):
    """
    View for the data type selected
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

    def __init__(self, menu):
        if ViewDataTypeSelection.__instance is not None:
            raise Exception("ViewDataTypeSelection should be treated as a singleton class.")
        else:
            ViewDataTypeSelection.__instance = self
        self.menu = menu

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewDataTypeSelection
        """
        if ViewDataTypeSelection.__instance is None:
            raise Exception("ViewDataTypeSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewDataTypeSelection.__instance

    def setup(self) -> None:
        """
        Setup data type selected menu
        """
        data_types = ["Fixation Data", "Gaze Data"]
        for data_type in data_types:
            if self.menu.findText(data_type) == -1:
                self.menu.addItem(data_type)
