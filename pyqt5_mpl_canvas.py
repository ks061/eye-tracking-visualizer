# Project libraries
import config as CONFIG

# Matplotlib/PyQt5 libraries
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.qt_compat import QtWidgets

# PyQt5MPLCanvas is a FigureCanvas that
# is customized for Matplotlib
# figures to be embedded within the GUI.
class PyQt5MPLCanvas(FigureCanvas):
    def __init__(self, fig):
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Fixed,
                                   QtWidgets.QSizePolicy.Fixed)
        FigureCanvas.updateGeometry(self)
