"""
Contains the class ViewMain

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

import sys

sys.path.insert(0, '../../../../')


class ViewMain(object):
    """
    Wrapper of the whole GUI of the application
    """
    __instance = None

    main_window = None
    central_widget = None

    # Constructor
    def __init__(self,
                 main_window,
                 central_widget):
        if ViewMain.__instance is not None:
            raise Exception("ViewMain should be treated as a singleton class.")
        else:
            ViewMain.__instance = self
        # 1. Main window/widget
        self.main_window = main_window
        self.central_widget = central_widget

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ViewMain
        """
        if ViewMain.__instance is None:
            raise Exception("ViewMain has not been instantiated and " + \
                            "cannot be done so without proper attributes")
        return ViewMain.__instance
