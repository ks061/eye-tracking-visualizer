"""
Contains the class ViewDataTypeSelection
"""


class ViewDataTypeSelection:
    """
    View for the data type selection
    """

    __instance = None

    hbox = None
    label = None
    menu = None

    def __init__(self,
                 hbox,
                 label,
                 menu):
        if ViewDataTypeSelection.__instance is not None:
            raise Exception("ViewDataTypeSelection should be treated as a singleton class.")
        else:
            ViewDataTypeSelection.__instance = self
        self.hbox = hbox
        self.label = label
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

    def setup(self):
        if self.menu.findText("Gaze Data") == -1:
            self.menu.addItem("Gaze Data")
        if self.menu.findText("Fixation Data") == -1:
            self.menu.addItem("Fixation Data")

    def enable(self):
        # Enable interface
        self.menu.setEnabled(True)

    def disable(self):
        # Disable interface
        self.menu.setEnabled(False)

    def clear(self):
        # clear data type selection menu
        self.menu.clear()

    def get_current_menu_selection(self):
        return self.menu.currentText()
