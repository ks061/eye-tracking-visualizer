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
    min_samples_label = None
    min_samples_slider = None

    browser = None
    vbox = None

    def __init__(self,
                 placeholder,
                 min_samples_label,
                 min_samples_slider):
        if ViewPlot.__instance is not None:
            raise Exception("ViewPlot should be treated as a singleton class.")
        else:
            ViewPlot.__instance = self
        self.placeholder = placeholder
        self.min_samples_label = min_samples_label
        self.min_samples_slider = min_samples_slider

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
        """
        Sets up the layout of the plot-holding
        widget and removes the old layout if
        needed
        """
        self.vbox = QtWidgets.QVBoxLayout(self.placeholder)
        self._browser_refresh()

        self.min_samples_slider.setMinimum(2)
        self.min_samples_slider.setMaximum(10)
        self.min_samples_slider.setValue(5)
        self.min_samples_slider.setSingleStep(1)

    def _browser_refresh(self):
        self.vbox.removeWidget(self.browser)
        self.browser = QtWebEngineWidgets.QWebEngineView(self.placeholder)
        self.vbox.insertWidget(0, self.browser)

    def plot(self, min_samples):
        """
        Creates a visualization based upon the given data,
        stimulus, and other menu selections made by the user
        """
        self._browser_refresh()
        fig = ModelPlot.get_instance().get_fig(min_samples)
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
