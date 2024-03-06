from abc import ABC, abstractmethod
import numpy as np

class Function(ABC):

    def compute(self, **kwargs):
        pass
    def findGradient(self):
        pass

class Himmelblau(Function):
    def __init__(self, x, y):
        x, y = np.meshgrid(x, y)
        self.func = np.array(((x**2+y-11)**2 + (x+y**2-7)**2))

    @staticmethod
    def compute(x, y):
        return ((x**2+y-11)**2 + (x+y**2-7)**2)

    @staticmethod
    def findGradient(x, y):
        return (4*x*(x**2 + y -11) + 2*(x + y**2 -7), 2*(x**2 + y - 11) + 4*y*(x + y**2 - 7))

class Sphere(Function):
    def __init__(self, x, y):
        x, y = np.meshgrid(x, y)
        self.func = np.array(x**2 + y**2)

    @staticmethod
    def compute(x, y):
        return (x**2 + y**2)

    def findGradient(self, x, y):
        return (2*x, 2*y)


