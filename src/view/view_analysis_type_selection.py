"""
Contains the class ViewAnalysisTypeSelection
"""


class ViewAnalysisTypeSelection:
    """
    View for the analysis type selection
    """

    __instance = None

    hbox = None
    label = None
    menu = None

    def __init__(self,
                 hbox,
                 label,
                 menu):
        if ViewAnalysisTypeSelection.__instance is not None:
            raise Exception("ViewAnalysisSelection should be treated as a singleton class.")
        else:
            ViewAnalysisTypeSelection.__instance = self
        self.hbox = hbox
        self.label = label
        self.menu = menu

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewAnalysisTypeSelection
        """
        if ViewAnalysisTypeSelection.__instance is None:
            raise Exception("ViewAnalysisTypeSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewAnalysisTypeSelection.__instance

    def enable(self):
        # Enable interface
        self.menu.setEnabled(True)

    def setup(self):
        if self.menu.findText("Scatter Plot") == -1:
            self.menu.addItem("Scatter Plot")
        if self.menu.findText("Line Plot") == -1:
            self.menu.addItem("Line Plot")
        if self.menu.findText("Heat Map") == -1:
            self.menu.addItem("Heat Map")
        if self.menu.findText("Cluster") == -1:
            self.menu.addItem("Cluster")

    def disable(self):
        # Disable interface
        self.menu.setEnabled(False)

    def clear(self):
        # clear analysis type selection menu
        self.menu.clear()

    def get_current_menu_selection(self):
        return self.menu.currentText()