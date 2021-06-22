class ViewDataTypeSelection:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with selecting
    the type of data that the app will be plotting.
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
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewDataTypeSelection
        """
        if ViewDataTypeSelection.__instance is not None:
            pass
        else:
            raise Exception("ViewDataTypeSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewDataTypeSelection.__instance

    def enable(self):
        # Enable interface
        self.menu.setEnabled(True)

    def setup(self):
        if self.menu.findText("Gaze Data") == -1:
            self.menu.addItem("Gaze Data")
        if self.menu.findText("Fixation Data") == -1:
            self.menu.addItem("Fixation Data")

    def disable(self):
        # Disable interface
        self.menu.setEnabled(False)

    def clear(self):
        # clear data type selection menu
        self.menu.clear()

    def update(self):
        self.disable()
        self.clear()
        self.setup()
        self.enable()

    def show(self):
        self.menu.show()

    def hide(self):
        self.menu.hide()

    def set_selection(self):
        self.selection = self.menu.currentText()

    def get_selection(self):
        return self.selection
