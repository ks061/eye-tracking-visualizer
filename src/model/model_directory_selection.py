"""
Contains the class ModelDirectorySelection
"""


class ModelDirectorySelection:
    """
    Model for the directory selection
    """
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
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ModelDirectorySelection
        """
        if ModelDirectorySelection.__instance is None:
            ModelDirectorySelection()
        return ModelDirectorySelection.__instance

    def set_path(self, path):
        """
        Sets the selected directory path

        :param path: selected directory path
        :type path: str
        """
        self.path = path

    def get_path(self):
        """
        Returns the selected directory path

        :return: selected directory path
        :rtype: str
        """
        return self.path

    def clear(self):
        """
        Clears the directory selection model
        """
        self.path = None