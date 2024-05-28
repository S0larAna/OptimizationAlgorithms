from operator import itemgetter
import numpy as np
import random

class BeeAlgorithm:
    def __init__(self, objective_function, num_scouts, num_elites, bees_per_elite, num_perspectives, search_radius,
                 bees_per_perspective, x_bound, y_bound, search_area='square'):
        self.best_bee = None
        self.objective_function = objective_function
        self.x_bound = float(x_bound)
        self.y_bound = float(y_bound)
        self.search_area = search_area

        # разведчики
        self.scouts = [[random.uniform(-self.x_bound, self.x_bound),
                        random.uniform(-self.y_bound, self.y_bound),
                        float(0.0)] for _ in range(num_scouts)]

        for scout in self.scouts:
            scout[2] = self.objective_function.get_function_point(scout[0], scout[1])

        self.total_workers = num_elites * bees_per_elite + num_perspectives * bees_per_perspective
        self.num_elites = num_elites
        self.num_perspectives = num_perspectives
        self.bees_per_elite = bees_per_elite
        self.bees_per_perspective = bees_per_perspective

        max_scout = max(self.scouts, key=itemgetter(2))
        self.workers = [[self.x_bound, self.y_bound, max_scout[2]] for _ in range(self.total_workers)]

        self.all_bees = []
        self.selected_bees = []
        self.search_radius = search_radius

    def deploy_scouts(self):
        for scout in self.scouts:
            scout[0] = random.uniform(-self.x_bound, self.x_bound)
            scout[1] = random.uniform(-self.y_bound, self.y_bound)
            scout[2] = self.objective_function.get_function_point(scout[0], scout[1])

    def analyze_reports(self):
        self.all_bees = self.scouts + self.workers
        self.all_bees.sort(key=itemgetter(2))
        self.selected_bees = self.all_bees[:self.num_elites + self.num_perspectives]

    def get_optimal_bee(self):
        return self.all_bees[0]

    def deploy_workers(self, worker_group, target_sector, radius):
        for worker in worker_group:
            worker[0] = random.uniform(target_sector[0] - radius, target_sector[0] + radius)
            worker[1] = random.uniform(target_sector[1] - radius, target_sector[1] + radius)
            worker[2] = self.objective_function.get_function_point(worker[0], worker[1])

    def search_selected_areas(self, param):
        for i in range(self.num_elites):
            start = i * self.bees_per_elite
            end = start + self.bees_per_elite
            self.deploy_workers(self.workers[start:end], self.selected_bees[i], self.search_radius * param)

        for i in range(self.num_perspectives):
            start = self.num_elites * self.bees_per_elite + i * self.bees_per_perspective
            end = start + self.bees_per_perspective
            self.deploy_workers(self.workers[start:end], self.selected_bees[self.num_elites + i], self.search_radius * param)

    def run(self, max_iterations):
        previous_optimal = [1000000000000, 1000000000000, 1000000000000]
        for iteration in range(max_iterations):
            self.deploy_scouts()
            self.analyze_reports()
            self.search_selected_areas(1 / (iteration + 1))
            self.best_bee = self.get_optimal_bee()
            if abs(self.best_bee[0] - previous_optimal[0]) < 0.00001 and abs(self.best_bee[1] - previous_optimal[1]) < 0.00001 and abs(self.best_bee[2] - previous_optimal[2]) < 0.00001:
                break
            previous_optimal = self.best_bee
            yield self.all_bees, self.selected_bees, self.best_bee