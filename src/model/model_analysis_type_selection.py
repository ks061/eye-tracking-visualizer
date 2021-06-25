class ModelAnalysisTypeSelection:
    __instance = None

    selection: str = None

    def __init__(self):
        super().__init__()
        if ModelAnalysisTypeSelection.__instance is not None:
            raise Exception("ModelAnalysisTypeSelection should be treated as a singleton class.")
        else:
            ModelAnalysisTypeSelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ModelAnalysisTypeSelection
        """
        if ModelAnalysisTypeSelection.__instance is None:
            ModelAnalysisTypeSelection()
        return ModelAnalysisTypeSelection.__instance

    def set_selection(self, selection):
        self.selection = selection

    def get_selection(self):
        return self.selection

    def clear(self):
        self.selection = None