import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import LinearLocator
from PyQt5 import uic


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('ui\main_window.ui', self)

        # Find the appropriate widget in the UI file
        widget = self.findChild(QWidget, 'widget')  # Replace 'widget_name' with the actual name of the widget

        # Create a layout for the widget
        layout = QVBoxLayout(widget)

        # Create a Matplotlib figure and plot
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})
        X = np.arange(-5, 5, 0.25)
        Y = np.arange(-5, 5, 0.25)
        X, Y = np.meshgrid(X, Y)
        R = np.sqrt(X ** 2 + Y ** 2)
        Z = np.sin(R)

        # Plot the surface.
        self.ax.plot_surface(X, Y, Z, cmap=matplotlib.colormaps['viridis'],
                                    linewidth=0, antialiased=False, rcount=200, ccount=200)

        # Customize the z axis.
        self.ax.set_zlim(-1.01, 1.01)
        self.ax.zaxis.set_major_locator(LinearLocator(10))
        # A StrMethodFormatter is used automatically
        self.ax.zaxis.set_major_formatter('{x:.02f}')

        # Create a FigureCanvasQTAgg object
        self.canvas = FigureCanvas(self.fig)

        # Add the FigureCanvasQTAgg object to the layout
        layout.addWidget(self.canvas)
