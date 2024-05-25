import traceback

from Model.beesAlgorithm import BeeAlgorithm
from Model.functions import Rosenbrock
import numpy as np


class Lab5Controller:
    def __init__(self, window):
        # self.X = np.arange(-5, 5, 0.25)
        # self.Y = np.arange(-5, 5, 0.25)
        self.window = window
        self.function = window.controller.func
        self.iter_count = None
        self.scout_count = None
        self.bee_in_pers_count = None
        self.bee_in_best_count = None
        self.pers_count = None
        self.elite_count = None
        self.dist_size = None
        self.result = None


    def iter_count_getter(self):
        self.iter_count = self.window.num_iter_5.text()
        return self.iter_count

    def scout_count_getter(self):
        self.scout_count = self.window.num_scouts.text()
        return self.scout_count

    def bee_in_pers_count_getter(self):
        self.bee_in_pers_count = self.window.bees_in_perspective.text()
        return self.bee_in_pers_count

    def bee_in_best_count_getter(self):
        self.bee_in_best_count = self.window.bees_in_best.text()
        return self.bee_in_best_count

    def pers_count_getter(self):
        self.pers_count = self.window.num_perspective.text()
        return self.pers_count

    def elite_count_getter(self):
        self.elite_count = self.window.num_best.text()
        return self.elite_count

    def dist_size_getter(self):
        self.dist_size = self.window.area.text()
        return self.dist_size

    def onStartButtonClicked(self):
        self.run()

    def set_function(self, function):
        self.function = function

    def delay_getter(self):
        delay = self.window.lab5_delay.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def run(self):
        self.window.clear_points_dynamic()
        self.start_calc()
        self.window.drawPoint(self.result[0], self.result[1], self.function, mycolor='red')


    def start_calc(self):
        self.iter_count_getter()
        self.scout_count_getter()
        self.bee_in_pers_count_getter()
        self.bee_in_best_count_getter()
        self.pers_count_getter()
        self.elite_count_getter()
        self.dist_size_getter()
        self.delay_getter()
        try:
            self.iter_count = int(self.iter_count)
            self.scout_count = int(self.scout_count)
            self.bee_in_pers_count = int(self.bee_in_pers_count)
            self.bee_in_best_count = int(self.bee_in_best_count)
            self.pers_count = int(self.pers_count)
            self.elite_count = int(self.elite_count)
            self.dist_size = float(self.dist_size)
            delay = float(self.delay_getter())

            self.window.resultsTextEdit.clear()
            bees = BeeAlgorithm(self.function, self.scout_count, self.elite_count, self.bee_in_best_count, self.pers_count, self.dist_size, self.bee_in_pers_count, 5, 5)

            all_points = []
            best_x, best_y, best_fitness = 0, 0, 0

            for i, (bees_data, selected_data, best_bee) in enumerate(bees.run(self.iter_count)):
                points = []
                for mielpops in bees_data:
                    x, y, z = mielpops
                    points.append([x, y, z])

                all_points.append(points)

                best_x, best_y, best_fitness = best_bee
                self.window.updateText(f"Итерация {i}: лучшие координаты пчелы: x={best_x: .4f}, y={best_y: .4f}, z={best_fitness: .4f}", delay=delay)

            # print(allPoints)
            self.window.updateListPoint(all_points, marker='.', delay=delay)
            self.result = best_bee

        except TypeError or ValueError as _:
            print(traceback.format_exc())