import os

from PyQt5 import QtWidgets, QtWebEngineWidgets
import plotly.express as px

from src.main import config
from src.model.model_main import ModelMain
from src.model.model_plot import ModelPlot
from src.model.utils import data_util
from src.view.utils import visual_util
from src.view.view_directory_selection import ViewDirectorySelection


class ViewPlot:
    """
    Wrapper for the object that represents
    the GUI component of the app that deals with
    displaying the plot plotted by the
    application.
    """

    __instance = None

    placeholder = None
    browser = None
    vbox = None

    def __init__(self,
                 placeholder):
        super().__init__()
        if ViewPlot.__instance is not None:
            raise Exception("ViewPlot should be treated as a singleton class.")
        else:
            ViewPlot.__instance = self
        self.placeholder = placeholder
        self._setup()

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewPlot
        """
        if ViewPlot.__instance is None:
            raise Exception("ViewPlot has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewPlot.__instance

    def _setup(self):
        self.browser = QtWebEngineWidgets.QWebEngineView(self.placeholder)
        self.vbox = QtWidgets.QVBoxLayout(self.placeholder)
        self.vbox.addWidget(self.browser)

    def plot(self):
        fig = ModelPlot.get_instance().get_fig()
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))