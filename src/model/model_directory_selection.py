class ModelDirectorySelection:
    __instance = None

    path = None

    def __init__(self):
        if ModelDirectorySelection.__instance is not None:
            raise Exception("ModelDirectorySelection should be treated as a singleton class.")
        else:
            ModelDirectorySelection.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ModelDirectorySelection
        """
        if ModelDirectorySelection.__instance is None:
            ModelDirectorySelection()
        return ModelDirectorySelection.__instance

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def clear(self):
        self.path = None