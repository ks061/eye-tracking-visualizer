"""
Contains the class ViewError

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""


class ViewError(object):
    """
    View for the error-displaying
    part of the user interface
    """

    __instance = None

    scroll_area = None
    scrollAreaWidgetContents = None
    message = None

    def get_message(self) -> str: return self.message
    def set_message(self, message: str): self.message = message

    def __init__(self,
                 message):
        if ViewError.__instance is not None:
            raise Exception("ViewError should be treated as a singleton class.")
        else:
            ViewError.__instance = self
        self.message = message

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewError
        """
        if ViewError.__instance is None:
            raise Exception("ViewError has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewError.__instance
