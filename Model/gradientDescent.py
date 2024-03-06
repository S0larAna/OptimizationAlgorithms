from __future__ import annotations
from Model.functions import Function
import numpy as np

class Algorithms():
    def __init__(self, strategy: Function) -> None:
        self._strategy = strategy

    def strategy(self, strategy: Function) -> None:
        self._strategy = strategy

    def gradientDescent(self, x, y, M, t, eps=0.0001):
        k = 0
        while (k<=M):
            grad = self._strategy.findGradient(x, y)
            if (abs(grad[0])<eps or abs(grad[1])<eps):
                break
            x_next = x - t * grad[0]
            y_next = y - t * grad[1]
            func_next = self._strategy.compute(x_next, y_next)
            func_prev = self._strategy.compute(x, y)
            while not (func_next - func_prev < 0):
                t/=2
                x_next = x - t * grad[0]
                y_next = y - t * grad[1]
                func_next = self._strategy.compute(x_next, y_next)
                func_prev = self._strategy.compute(x, y)
            if ((np.linalg.norm(np.array([x_next, y_next]) - np.array([x, y])) < eps) and abs(func_next - func_prev) < eps):
                break
            k += 1
            x, y = x_next, y_next
            print(x_next, y_next)
            yield (x, y)