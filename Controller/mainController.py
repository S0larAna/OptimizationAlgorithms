from Model.functions import *
from Model.gradientDescent import *
import numpy as np

class mainWindowController():
    def __init__(self, w):
        self._window = w
        self.X = np.arange(-5, 5, 0.25)
        self.Y = np.arange(-5, 5, 0.25)
        self.func = Himmelblau(self.X, self.Y)

    def change_function(self):
        function = self._window.functionBox.currentText()

        if function == 'Химмельблау':
            self.func = Himmelblau(self.X, self.Y)
        if function == 'Функция Бута':
            self.func = Booth(self.X, self.Y)
        if function == 'Функция сферы':
            self.func = Sphere(self.X, self.Y)
        if function == 'Для симплекс-метода':
            self.func = FunctionLab2(self.X, self.Y)
        if function == 'Функция Розенброка':
            self.func = Rosenbrock(self.X, self.Y)
        if function == 'Функция Швефеля':
            self.X = np.arange(-500, 500, 0.25)
            self.Y = np.arange(-500, 500, 0.25)
            self.func = Schwefeles(self.X, self.Y)
        self._window.drawGraph(function=self.func, X=self.X, Y=self.Y)
        return self.func


    def run(self):
        self._window.resultsTextEdit.clear()
        x = float(self._window.x_start.text())
        y = float(self._window.y_start.text())
        iterations = int(self._window.iterations.text())
        step = float(self._window.step.text())
        try:
            self._window.drawPoint(x, y, self.func)
            computer = Algorithms(self.func)
            grad = computer.gradientDescent(x, y, iterations, step)
            for i, el in enumerate(grad):
                self._window.drawPoint(el[0], el[1], self.func)
                self._window.resultsTextEdit.append(f"итерация: {i}. f({round(el[0], 4)},{round(el[1], 4)})={round(self.func.compute(el[0], el[1]), 4)} \n")
            self._window.drawPoint()
        except Exception as ex:
            # QMessageBox.warning(self.window, "Warning", "Wrong Data")
            print(ex)
