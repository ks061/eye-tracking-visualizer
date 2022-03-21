"""
Launches the eye-tracking visualizer application
"""

# External imports
from PyQt5.QtWidgets import QApplication
import sys

# Internal imports
from src.controller.delegator import Delegator
from src.model.model_data import ModelData

if __name__ == '__main__':
    ModelData.get_instance().load_df()
    app = QApplication(sys.argv)
    delegator = Delegator()
    sys.exit(app.exec_())