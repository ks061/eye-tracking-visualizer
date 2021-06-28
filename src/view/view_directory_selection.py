"""
Contains the class ViewDirectorySelection
"""


class ViewDirectorySelection:
    """
    View for the directory selection
    """

    __instance = None

    button = None

    def __init__(self, button):
        if ViewDirectorySelection.__instance is not None:
            raise Exception("ViewDirectorySelection should be treated as a singleton class.")
        else:
            ViewDirectorySelection.__instance = self
        self.button = button

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewDirectorySelection
        """
        if ViewDirectorySelection.__instance is None:
            raise Exception("ViewDirectorySelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewDirectorySelection.__instance