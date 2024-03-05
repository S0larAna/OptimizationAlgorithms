import sys

from PyQt5.QtWidgets import QApplication

from View.app import MyMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow().create()
    w.show()
    sys.exit(app.exec())