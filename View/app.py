import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import LinearLocator
from PyQt5 import uic
from Controller.mainController import mainWindowController
from Controller.lab2Controller import Lab2Controller
from Controller.lab3Controller import Lab3Controller
from Controller.lab4Controller import Lab4Controller
from Controller.lab5Controller import Lab5Controller
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSignal, QThread, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from Model.functions import *


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = mainWindowController(self)
        self.labController = mainWindowController(self)
        # self.labController.set_function(Himmelblau(self.X, self.Y))
        # Load the UI file
        uic.loadUi('ui\main_window.ui', self)
        self.layout = QVBoxLayout(self.widget)
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.ax.set_zlim(-1.01, 1.01)
        self.ax.zaxis.set_major_locator(LinearLocator(10))
        self.ax.zaxis.set_major_formatter('{x:.02f}')
        self.tabWidget.setCurrentIndex(0)
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)
        self.text_thread = TextThread(self)
        self.point_thread = PointThread(self)
        self.point_list_thread = PointListThread(self, self.canvas)
        self.tabWidget.currentChanged.connect(self.onTabChanged)
        self.functionBox.currentTextChanged.connect(lambda: self.controller.change_function())
        self.startButton.clicked.connect(lambda: self.labController.run())
        self.points = []
        self.text_thread.text_signal.connect(self.resultsTextEdit.append)
        self.point_thread.point_signal.connect(self.drawPoints)
        self.point_list_thread.point_signal.connect(self.drawPoints)
        self.point_list_thread.clearPointsSignal.connect(self.clear_points_dynamic)


    def onTabChanged(self, index):
        if index == 0:
            self.labController = mainWindowController(self)
        elif index == 1:
            self.labController = Lab2Controller(self)
        elif index == 2:
            self.labController = Lab3Controller(self)
        elif index == 3:
            self.labController = Lab4Controller(self)
        elif index == 4:
            self.labController = Lab5Controller(self)

    def clear_points_dynamic(self):
        for point in self.points:
            if isinstance(point, list):
                point.clear()
            else:
                point.remove()  # Удаляем все точки с графика
        self.points.clear()

    def drawGraph(self, function, X, Y):
        self.ax.clear()
        self.X, self.Y = np.meshgrid(X, Y)
        self.ax.autoscale(enable=True)

        # Plot the surface.
        self.ax.plot_surface(self.X, self.Y, function.func, cmap=matplotlib.colormaps['viridis'],
                                    linewidth=0, alpha=0.65, rcount=200, ccount=200)

        # Add the FigureCanvasQTAgg object to the layout
        # self.layout.addWidget(self.canvas)
        self.canvas.draw()

    def drawPoint(self, x, y, function, mycolor='black'):
        self.ax.scatter(x, y, function.compute(x, y), color=mycolor, marker='o', s=10, zorder=10)
        print(x, y, function.compute(x, y))
        self.canvas.draw()

    def drawPoints(self, points, mycolor='black'):
        for point in points:
            x, y, z = point
            self.points.append(self.ax.scatter(x, y, z, color=mycolor, marker='o', s=10, zorder=10))
        self.canvas.draw()

    def updateText(self, text, delay=0):
        self.text_thread.add_text(text, delay)
        if not self.text_thread.isRunning():
            self.text_thread.start()

    def updateListPoint(self, points, color='black', marker='o', delay=0):
        self.point_list_thread.set_points(points, color, marker, delay)
        if not self.point_list_thread.isRunning():
            self.point_list_thread.start()

class TextThread(QThread):
    text_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.texts = []

    def add_text(self, text, delay):
        self.texts.append((text, delay))

    def run(self):
        for text, delay in self.texts:
            self.msleep(int(delay * 1000))
            self.text_signal.emit(text)
        self.texts.clear()

class PointThread(QThread):
    point_signal = pyqtSignal(list, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.points = []

    def add_points(self, points, color, marker, delay):
        # self.points= []
        if isinstance(points, tuple):
            points = [points]
        # print(self.points)
        self.points.append((points, color, marker, delay))

    def run(self):
        for point_data in self.points:
            points, color, marker, delay = point_data
            self.msleep(int(delay * 1000))
            self.point_signal.emit(points, color, marker)
        # GraphWidget().clear_points()  # Очищаем список точек
        self.points.clear()

class PointListThread(QThread):
    point_signal = pyqtSignal(list, str, str)
    clearPointsSignal = pyqtSignal()  # Новый сигнал для очистки точек

    def __init__(self, parent, graph):
        super().__init__(parent)
        self.points = []
        self.painting = False
        self.graph = graph

    def add_points(self, points, color, marker, delay):
        self.points = []
        for el in points:
            self.points.append((el, color, marker, delay))

    def set_points(self, points, color, marker, delay):
        self.points.clear()
        self.add_points(points, color, marker, delay)

    def run(self):
        for i, el in enumerate(self.points):
            min_point = min(el[0], key=lambda x: x[2])
            self.point_signal.emit(el[0], el[1], el[2])
            self.point_signal.emit([min_point], 'red', 'o')
            self.msleep(int(el[3] * 1000))
            if i != len(self.points) - 1:
                self.clearPointsSignal.emit()
