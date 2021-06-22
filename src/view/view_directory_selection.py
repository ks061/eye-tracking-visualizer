class ViewDirectorySelection:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with selecting
    the directory from which the app will be plotting.
    """

    __instance = None

    button = None
    path = None

    def __init__(self, button):
        super().__init__()
        if ViewDirectorySelection.__instance is not None:
            raise Exception("ViewDirectorySelection should be treated as a singleton class.")
        else:
            ViewDirectorySelection.__instance = self
        self.button = button

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewDirectorySelection
        """
        if ViewDirectorySelection.__instance is not None:
            pass
        else:
            raise Exception("ViewDirectorySelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewDirectorySelection.__instance

    def show(self):
        # Data type selection
        self.button.show()

    def hide(self):
        # Data type selection
        self.button.hide()

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path