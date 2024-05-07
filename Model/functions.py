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

class Booth(Function):
    def __init__(self, x, y):
        x, y = np.meshgrid(x, y)
        self.func = np.array((x + 2*y - 7)**2 + (2*x +y -5)**2)

    @staticmethod
    def compute(x, y):
        return ((x + 2*y - 7)**2 + (2*x +y -5)**2)

    def findGradient(self, x, y):
        return ((2 * (x + 2 * y - 7) + 2 * (2 * x + y - 5) * 2), (2 * (x + 2 * y - 7) * 2 + 2 * (2 * x + y - 5)))

class FunctionLab2(Function):
    def __init__(self, x, y):
        x, y = np.meshgrid(x, y)
        self.func = np.array(2 * x ** 2 + 3 * y ** 2 + 4 * x * y - 6 * x - 3 * y)
    def findGradient(self):
        pass

    @staticmethod
    def compute(x, y):
        return 2 * x ** 2 + 3 * y ** 2 + 4 * x * y - 6 * x - 3 * y

class Rosenbrock(Function):
    def __init__(self, x, y):
        x, y = np.meshgrid(x, y)
        self.func = np.array((1-x)**2 + 100*(y-x**2)**2)

    @staticmethod
    def compute(x, y):
        return (1-x)**2 + 100*(y-x**2)**2

    def get_function_point(self, x, y):
        return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

class Schwefeles(Function):
    def __init__(self, x, y):
        x, y = np.meshgrid(x, y)
        self.func = np.array(-x * np.sin(np.sqrt(np.abs(x))) - y * np.sin(np.sqrt(np.abs(y))))

    @staticmethod
    def compute(x, y):
        return -x * np.sin(np.sqrt(np.abs(x))) - y * np.sin(np.sqrt(np.abs(y)))

    def get_function_point(self, x, y):
        return -x * np.sin(np.sqrt(np.abs(x))) - y * np.sin(np.sqrt(np.abs(y)))


