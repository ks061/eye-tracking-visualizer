# Project libraries
from pyqt5_mpl_canvas import PyQt5MPLCanvas

# Matplotlib/PyQt5 libraries
from matplotlib.backends.qt_compat import QtWidgets

# PyQt5MPLWidget is a QWidget that
# is customized for Matplotlib
# figures to be embedded within the GUI.
class PyQt5MPLWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self._canvas = PyQt5MPLCanvas()
        self._vbox = QtWidgets.QVBoxLayout()
        self._vbox.addWidget(self._canvas)
        self.setLayout(self._vbox)
