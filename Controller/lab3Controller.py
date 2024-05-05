import traceback
import numpy as np

from Model.GeneticAlgorithm import GeneticAlgorithm
from Model.functions import Rosenbrock

class Lab3Controller:
    def __init__(self, window):
        self.X = np.arange(-5, 5, 0.25)
        self.Y = np.arange(-5, 5, 0.25)
        self.window = window
        self.function = Rosenbrock(self.X, self.Y)
        self.popul_size = None
        self.iter_num = None
        self.surv = 0.5
        self.mut_chance = 0.3

    def get_population_size(self):
        self.popul_size = self.window.popul_size.text()
        return self.popul_size

    def iter_count_getter(self):
        self.iter_num = self.window.iter_num.text()
        return self.iter_num

    def surv_getter(self):
        self.surv = self.window.surv.text()
        return self.surv

    def mut_chance_getter(self):
        self.mut_chance = self.window.mut_chance.text()
        return self.mut_chance

    def run(self):
        self.start_calc()

    def delay_getter(self):
        delay = self.window.delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def start_calc(self):
        self.get_population_size()
        self.iter_count_getter()
        # self.surv_getter()
        # self.mut_chance_getter()
        try:
            self.popul_size = int(self.popul_size)
            self.iter_num = int(self.iter_num)
            # self.surv = float(self.surv_getter())
            # self.mut_chance = float(self.mut_chance_getter())
            delay = float(self.delay_getter())

            self.window.resultsTextEdit.clear()
            genetic_algorithm = GeneticAlgorithm(self.function.get_function_point, self.popul_size, self.iter_num, self.mut_chance,
                                                 self.surv)

            x_bounds = (-5, 5)
            y_bounds = (-5, 5)

            allPoints = []

            for i, population in enumerate(genetic_algorithm.run(x_bounds, y_bounds)):
                points = []
                for individual in population:
                    x, y, _ = individual
                    points.append([x, y, self.function.get_function_point(x, y)])

                allPoints.append(points)

                min_point = [round(i, 3) for i in min(points, key=lambda x: x[2])]
                self.window.updateText(f'Поколение {i}: {min_point[0], min_point[1]}, f: {min_point[2]}', delay=delay)

            # print(allPoints)
            self.window.updateListPoint(allPoints, marker='.', delay=delay)


        except TypeError or ValueError as ex:
            print(traceback.format_exc())