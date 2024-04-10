from Model.SimplexMethod import Simplex
from Model.functions import FunctionLab2
import numpy as np


class Lab2Controller:
    def __init__(self, window):
        self.window = window
        self.X = np.arange(-5, 5, 0.25)
        self.Y = np.arange(-5, 5, 0.25)
        self.function = FunctionLab2(self.X, self.Y)
        self.x_start = -5
        self.y_start = -5

    def set_function(self, function):
        pass


    def startDescent(self):
        try:

            self.window.resultsTextEdit.clear()
            simplex = Simplex()
            for i, el in enumerate(simplex.startUp()):
                self.window.drawPoint(el[0], el[1], self.function)

                text = f'{i}:  (x, y, function) = ({round(el[0], 5)}, {round(el[1], 5)}, {round(el[2], 5)})'
                self.window.resultsTextEdit.append(text)
                point = el[:3]

            self.window.drawPoint(point[0], point[1], self.function, mycolor='red')

        except Exception as ex:
            print(ex)