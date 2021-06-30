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
        """
        Enables the analysis type selection menu
        """
        self.menu.setEnabled(True)

    def setup(self):
        """
        Sets up the analysis type selection menu
        """
        if self.menu.findText("Scatter Plot") == -1:
            self.menu.addItem("Scatter Plot")
        if self.menu.findText("Line Plot") == -1:
            self.menu.addItem("Line Plot")
        if self.menu.findText("Heat Map") == -1:
            self.menu.addItem("Heat Map")
        if self.menu.findText("Cluster") == -1:
            self.menu.addItem("Cluster")

    def disable(self):
        """
        Disables the analysis type selection menu
        """
        self.menu.setEnabled(False)

    def clear(self):
        """
        Clears the analysis type selection menu
        """
        self.menu.clear()

    def get_current_menu_selection(self):
        """
        Gets the current user selection in
        the analysis type selection menu

        :return: analysis type selection
        :rtype: str
        """
        return self.menu.currentText()