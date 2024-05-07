import numpy
import numpy as np
import random

class Particle:
    def __init__(self):
        self.position = np.random.uniform(-5, 5, 2)
        self.velocity = np.zeros(2)
        self.best_point = self.position.copy()
        self.best_value = float('inf')

    def update_velocity(self, global_best_position, w, c1, c2):
        r1 = np.random.rand(len(self.position))
        r2 = np.random.rand(len(self.position))
        cognitive_velocity = c1 * r1 * (self.best_point - self.position)
        social_velocity = c2 * r2 * (global_best_position - self.position)
        self.velocity = w * self.velocity + cognitive_velocity + social_velocity

    def update_position(self, min_bound, max_bound):
        self.position = self.position + self.velocity
        self.position = np.clip(self.position, min_bound, max_bound)


class Swarm:
    def __init__(self, num_particles, weight, iterations, function, c1=1.49, c2=1.49):
        self.position = np.random.uniform(-5, 5, 2)
        self.num_particles = num_particles
        self.weight = weight
        self.best_global_point = []
        self.best_global_value = float('inf')
        self.particles = []
        self.iterations = iterations
        self.function = function
        self.c1 = c1
        self.c2 = c2

    def initialize_particles(self):
        return [Particle() for _ in range(self.num_particles)]

    def run(self):
        self.particles = self.initialize_particles()




    def run(self):
        pass