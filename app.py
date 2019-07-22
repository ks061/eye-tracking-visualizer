import sys

# Project libraries
from gui import GUI

# Matplotlib/PyQt5 libraries
from matplotlib.backends.qt_compat import QtCore, QtWidgets

# Main function that runs the application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
