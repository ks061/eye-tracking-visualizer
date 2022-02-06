"""
Launches the eye-tracking visualizer application
"""

# External imports
import PyQt5.QtWidgets
import sys

# Internal imports
from src.controller.delegator import Delegator

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    delegator = Delegator()
    sys.exit(app.exec_())
