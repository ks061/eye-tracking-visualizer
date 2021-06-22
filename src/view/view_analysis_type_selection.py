class ViewAnalysisTypeSelection:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with selecting
    the type of analysis that the app will be plotting.
    """

    __instance = None

    hbox = None
    label = None
    menu = None

    selection = None

    def __init__(self,
                 hbox,
                 label,
                 menu):
        super().__init__()
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
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewAnalysisTypeSelection
        """
        if ViewAnalysisTypeSelection.__instance is not None:
            pass
        else:
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

    def update(self):
        self.disable()
        self.clear()
        self.setup()
        self.enable()

    def show(self):
        # Data type selection
        self.menu.show()

    def hide(self):
        # Data type selection
        self.menu.hide()

    def set_selection(self):
        self.selection = self.menu.currentText()

    def get_selection(self):
        return self.selection