import cProfile
import sys

from PyQt5.QtWidgets import QApplication
from src.controller.delegator import Delegator


def run():
    """
    Runs the program
    """
    app = QApplication(sys.argv)
    Delegator()
    app.exec_()


# Runs the profiler on the program
# Inspired by
# https://stackoverflow.com/questions/21274898/
# python-getting-meaningful-results-from-cprofile
if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    run()
    profiler.disable()
    profiler.print_stats(sort='cumtime')
