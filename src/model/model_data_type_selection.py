class ModelDataTypeSelection:
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
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ModelDataTypeSelection
        """
        if ModelDataTypeSelection.__instance is None:
            ModelDataTypeSelection()
        return ModelDataTypeSelection.__instance

    def set_selection(self, selection):
        self.selection = selection

    def get_selection(self):
        return self.selection

    def clear(self):
        self.selection = None