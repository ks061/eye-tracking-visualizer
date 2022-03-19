"""
Contains the class ViewAnalysisTypeSelection

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""


class ViewAnalysisTypeSelection(object):
    """
    View for the analysis type selected
    """

    __instance = None

    menu = None

    def enable(self) -> None:
        self.menu.setEnabled(True)

    def disable(self) -> None:
        self.menu.setEnabled(False)

    def clear(self) -> None:
        self.menu.clear()

    def get_selected(self) -> str:
        return self.menu.currentText()

    def __init__(self, menu):
        if ViewAnalysisTypeSelection.__instance is not None:
            raise Exception("ViewAnalysisSelection should be treated as a singleton class.")
        else:
            ViewAnalysisTypeSelection.__instance = self
        self.menu = menu

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewAnalysisTypeSelection
        """
        if ViewAnalysisTypeSelection.__instance is None:
            raise Exception("ViewAnalysisTypeSelection has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewAnalysisTypeSelection.__instance

    def setup(self) -> None:
        """
        Sets up the analysis type selected menu
        """
        analysis_types = ["Cluster", "Scatter Plot", "Line Plot", "Heat Map"]
        for analysis_type in analysis_types:
            if self.menu.findText(analysis_type) == -1:
                self.menu.addItem(analysis_type)
