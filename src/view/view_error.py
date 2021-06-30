"""
Contains the class ViewError
"""


class ViewError:
    """
    View for the error-displaying
    part of the user interface
    """

    __instance = None

    scroll_area = None
    scrollAreaWidgetContents = None
    message = None

    def __init__(self,
                 scroll_area,
                 scroll_area_widget_contents,
                 message):
        if ViewError.__instance is not None:
            raise Exception("ViewError should be treated as a singleton class.")
        else:
            ViewError.__instance = self
        self.scroll_area = scroll_area
        self.scrollAreaWidgetContents = scroll_area_widget_contents
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
