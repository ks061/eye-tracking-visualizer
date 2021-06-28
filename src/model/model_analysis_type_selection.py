"""
Contains the class ModelAnalysisTypeSelection
"""


class ModelAnalysisTypeSelection:
    """
    Model for the analysis type selection
    """
    __instance = None

    selection = None

    def __init__(self):
        if ModelAnalysisTypeSelection.__instance is not None:
            raise Exception("ModelAnalysisTypeSelection should be treated as a singleton class.")
        else:
            ModelAnalysisTypeSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ModelAnalysisTypeSelection
        """
        if ModelAnalysisTypeSelection.__instance is None:
            ModelAnalysisTypeSelection()
        return ModelAnalysisTypeSelection.__instance

    def set_selection(self, selection):
        """
        Sets the selected analysis type

        :param selection: selected analysis type
        :type selection: str
        """
        self.selection = selection

    def get_selection(self):
        """
        Gets the selected analysis type

        :return: selected analysis type
        :rtype: str
        """
        return self.selection

    def clear(self):
        """
        Clears the analysis type model
        """
        self.selection = None
