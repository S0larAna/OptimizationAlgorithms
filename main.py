import sys

from Model.functions import Himmelblau
from PyQt5.QtWidgets import QApplication
import numpy as np

from View.app import MyMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyMainWindow()
    w.drawGraph(Himmelblau(np.arange(-5, 5, 0.25), np.arange(-5, 5, 0.25)))
    w.show()
    sys.exit(app.exec())