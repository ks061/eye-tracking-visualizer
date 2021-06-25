# import project libraries
import sys
import src.model.utils.data_util as data_util
import src.view.utils.visual_util as visual_util
import src.view.utils.heatmap_util as heatmap_util
import src.model.utils.cluster_util as cluster_util
import glob
import os
from pathlib import Path
# Data libraries
import seaborn as sns
# Visual libraries
from PIL import Image, ImageDraw
# Matplotlib/PyQt5 libraries
from PyQt5 import QtGui, QtWidgets
from PyQt5 import uic

sys.path.insert(0, '../../../../')


class ViewMain:
    __instance = None

    main_window = None
    central_widget = None

    plotting_row_hbox = None

    plotting_row_options_vbox = None
    directory_vspacer = None
    plot_button = None
    bottom_vspacer = None

    plotting_row_plot_vbox = None

    plotting_row_vspacer = None

    # Constructor
    def __init__(self,
                 main_window,
                 central_widget,
                 plotting_row_hbox,
                 plotting_row_options_vbox,
                 directory_vspacer,
                 plot_button,
                 bottom_vspacer,
                 plotting_row_plot_vbox,
                 plotting_row_vspacer):
        super().__init__()
        if ViewMain.__instance is not None:
            raise Exception("ViewMain should be treated as a singleton class.")
        else:
            ViewMain.__instance = self
        # 1. Main window/widget
        self.main_window = main_window
        self.central_widget = central_widget
        # 1.1 Row encapsulating all components of UI
        self.plotting_row_hbox = plotting_row_hbox
        # 1.1.1 Vertical column of option components
        self.plotting_row_options_vbox = plotting_row_options_vbox
        self.directory_vspacer = directory_vspacer
        self.plot_button = plot_button
        self.bottom_vspacer = bottom_vspacer
        # 1.2 Vertical column containing plot
        self.plotting_row_plot_vbox = plotting_row_plot_vbox
        # 1.3 Vertical spacer separating the
        #     option components and plot
        self.plotting_row_vspacer = plotting_row_vspacer

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ViewMain
        """
        if ViewMain.__instance is None:
            raise Exception("ViewMain has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewMain.__instance
