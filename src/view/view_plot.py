"""
Contains the class ViewPlot
"""

# External imports
from PyQt5 import QtWidgets, QtWebEngineWidgets
# Internal imports
from src.model.model_plot import ModelPlot


class ViewPlot:
    """
    View for the plot
    """

    __instance = None

    placeholder = None
    browser = None
    vbox = None

    def __init__(self,
                 placeholder):
        if ViewPlot.__instance is not None:
            raise Exception("ViewPlot should be treated as a singleton class.")
        else:
            ViewPlot.__instance = self
        self.placeholder = placeholder
        self._setup()

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewPlot
        """
        if ViewPlot.__instance is None:
            raise Exception("ViewPlot has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewPlot.__instance

    def _setup(self):
        self.vbox = QtWidgets.QVBoxLayout(self.placeholder)
        self._browser_refresh()

    def _browser_refresh(self):
        self.vbox.removeWidget(self.browser)
        self.browser = QtWebEngineWidgets.QWebEngineView(self.placeholder)
        self.vbox.addWidget(self.browser)

    def plot(self):
        self._browser_refresh()
        fig = ModelPlot.get_instance().get_fig()
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))