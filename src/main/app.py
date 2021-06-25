import sys

# Matplotlib/PyQt5 libraries
from PyQt5.QtWidgets import QApplication

# Main function that runs the application
from src.controller.delegator import Delegator

if __name__ == '__main__':
    app = QApplication(sys.argv)
    delegator = Delegator()
    sys.exit(app.exec_())
