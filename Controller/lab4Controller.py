import traceback
import numpy as np

from Model.ParticleSwarm import Swarm, Particle
from Model.functions import Schwefeles, Sphere


class Lab4Controller:
    def __init__(self, window):
        self.X = np.arange(-5, 5, 0.25)
        self.Y = np.arange(-5, 5, 0.25)
        self.window = window
        self.function = Sphere(self.X, self.Y)
        self.num_particles = None
        self.num_iter = None
        self.phi1 = None
        self.phi2 = None
        self.weight = None

    def num_particles_getter(self):
        self.num_particles = self.window.num_particles.text()
        return self.num_particles

    def num_iter_getter(self):
        self.num_iter = self.window.num_iter.text()
        return self.num_iter

    def phi1_getter(self):
        self.phi1 = self.window.phi1.text()
        return self.phi1

    def phi2_getter(self):
        self.phi2 = self.window.phi2.text()
        return self.phi2

    def weight_getter(self):
        self.weight = self.window.weight.text()
        return self.weight

    def run(self):
        self.star_swarm()

    def delay_getter(self):
        delay = self.window.delay_2.text()
        if delay.replace(' ', '') != '' or float(delay) in range(0, 10):
            return float(delay)
        return 0.1

    def star_swarm(self):
        self.num_particles_getter()
        self.num_iter_getter()
        self.phi1_getter()
        self.phi2_getter()
        self.weight_getter()
        try:
            self.num_particles = int(self.num_particles_getter())
            self.num_iter = int(self.num_iter_getter())
            self.phi1 = float(self.phi1_getter())
            self.phi2 = float(self.phi2_getter())
            self.weight = float(self.weight_getter())
            delay = float(self.delay_getter())

            self.window.resultsTextEdit.clear()
            particleSwarm = Swarm(self.num_particles, self.weight, self.num_iter, self.function, self.phi1, self.phi2)

            allPoints = []
            allBestPoints = []

            for i, (positions, best_positions, global_best_position, global_best_fitness) in enumerate(particleSwarm.run()):
                allPoints.append(positions)
                allBestPoints.append(best_positions)

                self.window.updateText(
                    f'{i}: func({global_best_position[0]:.2f}, {global_best_position[1]:.2f}) = {global_best_fitness:.2f}',
                    delay=delay)

            self.window.updateListPoint(allPoints, marker='.', delay=delay)
            self.window.updateListPoint(allBestPoints, marker='o', delay=delay)

        except TypeError or ValueError:
            print(traceback.format_exc())