import sys

# for error catching
import sentry_sdk

# Matplotlib/PyQt5 libraries
from PyQt5.QtWidgets import QApplication
 
# Main function that runs the application
from src.controller.delegator import Delegator

if __name__ == '__main__':
    sentry_sdk.init(
        "https://3d2472c9289945538baba50800a83ad3@o741188.ingest.sentry.io/5786631",

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )
    app = QApplication(sys.argv)
    delegator = Delegator()
    sys.exit(app.exec_())
