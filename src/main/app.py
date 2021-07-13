"""
Launches the eye-tracking visualizer application
"""

# External imports
import sys
from PyQt5.QtWidgets import QApplication
# Internal imports
from src.controller.delegator import Delegator

if __name__ == '__main__':
    app = QApplication(sys.argv)
    delegator = Delegator()
    sys.exit(app.exec_())