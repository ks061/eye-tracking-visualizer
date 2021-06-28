"""
Contains the class ModelDataTypeSelection
"""


class ModelDataTypeSelection:
    """
    Model for the data type selection
    """
    __instance = None

    selection = None

    def __init__(self):
        if ModelDataTypeSelection.__instance is not None:
            raise Exception("ModelDataTypeSelection should be treated as a singleton class.")
        else:
            ModelDataTypeSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ModelDataTypeSelection
        """
        if ModelDataTypeSelection.__instance is None:
            ModelDataTypeSelection()
        return ModelDataTypeSelection.__instance

    def set_selection(self, selection):
        """
        Sets the selected data type

        :param selection: selected data type
        :type selection: str
        """
        self.selection = selection

    def get_selection(self):
        """
        Returns the selected data type

        :return: selected data type
        :rtype: str
        """
        return self.selection

    def clear(self):
        """
        Clears the data type model
        """
        self.selection = None
