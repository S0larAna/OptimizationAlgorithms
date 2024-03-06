import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.ticker import LinearLocator
from PyQt5 import uic
from Controller.mainController import mainWindowController


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = mainWindowController(self)

        # Load the UI file
        uic.loadUi('ui\main_window.ui', self)
        # Find the appropriate widget in the UI file
        # Create a layout for the widget
        self.layout = QVBoxLayout(self.widget)
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.ax.set_zlim(-1.01, 1.01)
        self.ax.zaxis.set_major_locator(LinearLocator(10))
        # A StrMethodFormatter is used automatically
        self.ax.zaxis.set_major_formatter('{x:.02f}')
        self.canvas = FigureCanvas(self.fig)
        #self.X = np.arange(-5, 5, 0.25)
        #self.Y = np.arange(-5, 5, 0.25)

        self.functionBox.currentTextChanged.connect(lambda: self.controller.change_function())
        self.startButton.clicked.connect(lambda: self.controller.startDescent())

    def drawGraph(self, function, X, Y):
        self.ax.clear()
        self.X, self.Y = np.meshgrid(X, Y)
        self.ax.autoscale(enable=True)

        # Plot the surface.
        self.ax.plot_surface(self.X, self.Y, function.func, cmap=matplotlib.colormaps['viridis'],
                                    linewidth=0, alpha=0.65, rcount=200, ccount=200)

        # Add the FigureCanvasQTAgg object to the layout
        self.layout.addWidget(self.canvas)
        self.canvas.draw()

    def drawPoint(self, x, y, function):
        self.ax.scatter(x, y, function.compute(x, y), color='black', marker='o', s=10, zorder=10)
        self.canvas.draw()
