"""
Contains the class ViewPlot

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

# External imports
from PyQt5 import QtWidgets, QtWebEngineWidgets


class ViewPlot(object):
    """
    View for the plot
    """

    __instance = None

    plot_button = None
    placeholder = None
    min_samples_slider = None

    # initialized in class
    browser = None
    vbox = None

    def __init__(self,
                 plot_button,
                 placeholder,
                 min_samples_slider):
        if ViewPlot.__instance is not None:
            raise Exception("ViewPlot should be treated as a singleton class.")
        else:
            ViewPlot.__instance = self
        self.plot_button = plot_button
        self.placeholder = placeholder
        self.min_samples_slider = min_samples_slider

        self.setup()

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

    def setup(self) -> None:
        """
        Sets up the layout of the plot-holding
        widget and removes the old layout if
        needed
        """
        self.vbox = QtWidgets.QVBoxLayout(self.placeholder)
        self.browser_refresh()

        self.min_samples_slider.setMinimum(2)
        self.min_samples_slider.setMaximum(10)
        self.min_samples_slider.setValue(5)
        self.min_samples_slider.setSingleStep(1)

    def plot(self, min_samples: int) -> None:
        """
        Creates a visualization based upon the given data,
        stimulus, and other menu selections made by the user
        """
        self.browser_refresh()
        fig = ModelPlot.get_instance().update_fig(min_samples)
        self.browser.resize(900, 700)
        self.browser.show()
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))

    def browser_refresh(self) -> None:
        self.vbox.removeWidget(self.browser)
        self.browser = QtWebEngineWidgets.QWebEngineView(self.placeholder)
        self.vbox.insertWidget(0, self.browser)


from src.model.model_plot import ModelPlot
