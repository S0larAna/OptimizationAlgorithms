from Model.functions import Function
from __future__ import annotations
import numpy as np

class Algorithms():
    def __init__(self, strategy: Function) -> None:
        self._strategy = strategy

    def strategy(self, strategy: Function) -> None:
        self._strategy = strategy

    def gradientDescent(self, eps, x, y, M, t):
        k = 0
        grad = self._strategy.findGradient(x, y)
        while (grad[0]>eps or grad[1]>eps):
            if (k>=M):
                return (x, y)
            else:
                x_next = x - t * grad[0]
                y_next = y - t * grad[1]
            func_next = self._strategy.compute(x_next, y_next)
            func_prev = self._strategy.compute(x, y)
            if (func_next - func_prev < 0):
                if (np.linalg.norm(np.array([y_next, x_next]) - np.array([y, x])) < eps) and abs(func_next - func_prev) < eps:
                    return (x, y)
                else:
                    k+=1
            else:
                t/=2
        return (x, y)