import sys

# Project libraries
from window import Window

# Matplotlib/PyQt5 libraries
from matplotlib.backends.qt_compat import QtWidgets

# Main function that runs the application
if __name__ == '__main__':
   application = QtWidgets.QApplication(sys.argv)
   screen_width = application.primaryScreen().size().width()
   screen_height = application.primaryScreen().size().height()
   win = Window(screen_width, screen_height)
   win.show()
   sys.exit(application.exec_())
