# PyQt learn
# eye image: https://commons.wikimedia.org/wiki/File:Eye_Icon.svg

#!/usr/bin/python3

print("Practice QDate, QTime, and QDate")

from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

now = QDate.currentDate()

print(now.toString(Qt.ISODate));
print(now.toString(Qt.DefaultLocaleLongDate))

datetime = QDateTime.currentDateTime()

print(datetime.toString())

time = QTime.currentTime()

print(time.toString(Qt.DefaultLocaleLongDate))


import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':

    application = QApplication(sys.argv)
    
    widg = QWidget()
    widg.resize(300, 200)
    widg.move(200,200)
    widg.setWindowTitle('Hello World')
    widg.show()

    sys.exit(application.exec_())
