class ViewError:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with
    displaying any errors that occur during the initial
    selection (of parameters) process prior to the
    application plotting.
    """

    __instance = None

    scroll_area = None
    scrollAreaWidgetContents = None
    message = None

    def __init__(self,
                 scroll_area,
                 scroll_area_widget_contents,
                 message):
        super().__init__()
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
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewError
        """
        if ViewError.__instance is not None:
            pass
        else:
            raise Exception("ViewError has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewError.__instance

    def show(self):
        self.scroll_area.show()
        self.message.show()

    def hide(self):
        self.scroll_area.hide()
        self.message.hide()