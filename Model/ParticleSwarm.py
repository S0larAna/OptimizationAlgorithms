import numpy as np

class Swarm:
    def __init__(self, num_particles, weight, iterations, function, phi1=1.49, phi2=1.49):
        self.num_particles = num_particles
        self.weight = weight
        self.best_global_point = []
        self.best_global_value = float('inf')
        self.particles = []
        self.iterations = iterations
        self.function = function
        self.phi1 = phi1
        self.phi2 = phi2

    def initialize_particles(self):
        return [Particle() for _ in range(self.num_particles)]

    def run(self):
        eps = 0.00001
        prev_best_global_value = float('inf')
        self.particles = self.initialize_particles()
        for i in range(self.iterations):
            for particle in self.particles:
                value = self.function.compute(*particle.position)
                if value < particle.best_value:
                    particle.best_value = value
                    particle.best_point = particle.position.copy()
                if value < self.best_global_value:
                    prev_best_global_value = self.best_global_value
                    self.best_global_value = value
                    self.best_global_point = particle.position.copy()
            for particle in self.particles:
                particle.update_velocity(self.best_global_point, self.weight, self.phi1, self.phi2)
                particle.update_position(-5, 5)
            if abs(self.best_global_value-prev_best_global_value) < eps:
                break
            positions = [[p.position[0], p.position[1], self.function.compute(*p.position)] for p in self.particles]
            best_positions = [[p.best_point[0], p.best_point[1], p.best_value] for p in self.particles]

            yield positions, best_positions, self.best_global_point, self.best_global_value

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


